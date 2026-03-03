"""
SWARM MODE - Unleash a swarm of agents on a task!

Usage: Just tell Agent Zero "create a swarm to <do something>"
The swarm will automatically:
1. Analyze the task and break it into subtasks
2. Spawn specialized subordinates for each subtask
3. Execute all subtasks in parallel
4. Synthesize the results into a cohesive response
"""
import asyncio
import uuid
import time
from datetime import datetime
from agent import Agent, UserMessage
from python.helpers.tool import Tool, Response
from python.helpers.swarm_analytics import SwarmMission, get_analytics
from initialize import initialize_agent
from python.extensions.hist_add_tool_result import _90_save_tool_call_file as save_tool_call_file


class Swarm(Tool):
    """
    SWARM MODE: Spawn a coordinated swarm of agents to tackle complex tasks.
    
    This tool automatically breaks down a mission into subtasks and delegates
    them to a swarm of specialized subordinates working in parallel.
    
    Args:
        mission: The overall mission/task for the swarm to accomplish
        swarm_size: Number of agents in the swarm (default: auto, 3-10)
        strategy: How to break down the task:
            - "auto": Let the swarm decide (default)
            - "divide": Divide by components/features
            - "research": Multiple angles on research/analysis
            - "review": Multiple reviewers with different expertise
            - "implement": Divide implementation into modules
    
    Example usage:
    {
        "tool_name": "swarm",
        "tool_args": {
            "mission": "Analyze this codebase for security vulnerabilities",
            "swarm_size": 5,
            "strategy": "review"
        }
    }
    """

    async def execute(self, mission="", swarm_size="auto", strategy="auto", **kwargs):
        if not mission or not isinstance(mission, str):
            return Response(
                message="❌ **Swarm Error:** I need a mission to unleash the swarm! Provide a clear task description.",
                break_loop=False
            )
        
        # Get analytics and recommendations
        analytics = get_analytics()
        recommendations = analytics.get_recommendations(mission, strategy if strategy != "auto" else None)
        
        # Parse swarm size - use recommendation if auto
        try:
            if str(swarm_size).lower() == "auto":
                size = recommendations.get('recommended_swarm_size', 4)
                self.agent.context.log.log(
                    type="swarm",
                    heading=f"🧠 Analytics Recommendation",
                    content=f"Based on {recommendations.get('based_on_n_missions', 0)} past missions, optimal size is {size} agents",
                )
            else:
                size = int(swarm_size)
                size = max(2, min(size, 12))  # Clamp between 2-12
        except:
            size = 4
        
        # Use recommended strategy if auto
        if strategy == "auto" and recommendations.get('recommended_strategy'):
            strategy = recommendations.get('recommended_strategy')
        
        # Validate strategy
        valid_strategies = ["auto", "divide", "research", "review", "implement"]
        if strategy not in valid_strategies:
            strategy = "auto"
        
        # Create mission record for analytics
        mission_record = SwarmMission(
            mission_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            strategy=strategy,
            swarm_size=size,
            max_parallel=min(size, 6),
            task_description=mission,
            agent_profiles=[],  # Will be populated after subtask generation
            start_time=time.time(),
        )
        
        # Log swarm activation
        self.agent.context.log.log(
            type="swarm",
            heading=f"🐝 SWARM ACTIVATED 🐝",
            content=f"Mission: {mission[:80]}...",
            kvps={
                "swarm_size": size,
                "strategy": strategy,
                "expected_duration": f"{recommendations.get('expected_duration_minutes', 5)} min",
            },
        )
        
        # Phase 1: Generate subtasks based on strategy
        subtasks = await self._generate_subtasks(mission, size, strategy)
        
        if not subtasks:
            return Response(
                message="❌ **Swarm Error:** Could not generate subtasks for this mission. Try being more specific!",
                break_loop=False
            )
        
        # Record agent profiles for analytics
        mission_record.agent_profiles = [t.get('profile', 'default') for t in subtasks]
        
        # Phase 2: Execute swarm (parallel subordinates)
        results = await self._execute_swarm(subtasks, mission)
        
        # Complete mission record and save
        mission_record.complete(results)
        analytics.record_mission(mission_record)
        
        # Phase 3: Synthesize results
        synthesis = await self._synthesize_results(results, mission, mission_record, recommendations)
        
        return Response(
            message=synthesis,
            break_loop=False
        )
    
    async def _generate_subtasks(self, mission: str, size: int, strategy: str) -> list:
        """Generate subtasks for the swarm based on strategy."""
        
        strategy_profiles = {
            "divide": [
                ("architect", "Design the overall structure and interfaces"),
                ("coder", "Implement core functionality"),
                ("engineer", "Build supporting utilities"),
                ("tester", "Create comprehensive tests"),
                ("documenter", "Write documentation and examples"),
            ],
            "research": [
                ("researcher", "Deep dive into technical background"),
                ("analyst", "Analyze current state and requirements"),
                ("investigator", "Research best practices and patterns"),
                ("evaluator", "Assess trade-offs and options"),
                ("synthesizer", "Connect findings across domains"),
            ],
            "review": [
                ("security", "Security audit and vulnerability scan"),
                ("performance", "Performance and optimization review"),
                ("maintainer", "Code maintainability and readability"),
                ("architect", "Architecture and design patterns"),
                ("tester", "Test coverage and edge cases"),
            ],
            "implement": [
                ("coder", "Implement main module A"),
                ("coder", "Implement main module B"),
                ("engineer", "Implement integration layer"),
                ("tester", "Unit tests for all modules"),
                ("devops", "Deployment and configuration"),
            ],
        }
        
        # For auto strategy, infer from mission keywords
        if strategy == "auto":
            mission_lower = mission.lower()
            if any(kw in mission_lower for kw in ["review", "audit", "check", "analyze", "security"]):
                strategy = "review"
            elif any(kw in mission_lower for kw in ["research", "investigate", "study", "learn"]):
                strategy = "research"
            elif any(kw in mission_lower for kw in ["build", "create", "implement", "develop", "write"]):
                strategy = "implement"
            else:
                strategy = "divide"
        
        # Get base profiles for this strategy
        base_profiles = strategy_profiles.get(strategy, strategy_profiles["divide"])
        
        # Generate subtasks
        subtasks = []
        for i in range(min(size, len(base_profiles))):
            profile, focus = base_profiles[i % len(base_profiles)]
            
            # Vary the focus for repeated profiles
            if i >= len(base_profiles):
                focus = f"{focus} (Part {i // len(base_profiles) + 1})"
            
            subtask = {
                "profile": profile,
                "message": self._build_subtask_prompt(mission, profile, focus, strategy, i+1, size),
            }
            subtasks.append(subtask)
        
        return subtasks
    
    def _build_subtask_prompt(self, mission: str, profile: str, focus: str, strategy: str, index: int, total: int) -> str:
        """Build a detailed prompt for a subordinate."""
        
        base_prompt = f"""## 🐝 SWARM MISSION - Agent {index} of {total}

### OVERALL MISSION:
{mission}

### YOUR SPECIALIZED ROLE:
Profile: **{profile}**
Focus: **{focus}**
Strategy Mode: **{strategy}**

### YOUR TASK:
You are part of a swarm of {total} specialized agents working in parallel on this mission. 
Your specific focus is: {focus}

### IMPORTANT GUIDELINES:
1. **Work independently** - Don't wait for other swarm members
2. **Be thorough** - Do excellent work on your specific focus area
3. **Be specific** - Provide concrete findings, code, or recommendations
4. **Consider integration** - Think about how your work fits with others
5. **Report fully** - Give a complete response; your output will be synthesized with others

### OUTPUT FORMAT:
Provide a comprehensive response covering your specialized focus area. Include:
- Key findings or implementations
- Specific details and examples
- Any concerns or recommendations
- Ready-to-use outputs (code, analysis, etc.)

Begin your work now!
"""
        return base_prompt
    
    async def _execute_swarm(self, subtasks: list, mission: str) -> list:
        """Execute the swarm in parallel."""
        
        max_parallel = min(len(subtasks), 6)  # Cap at 6 concurrent
        semaphore = asyncio.Semaphore(max_parallel)
        
        async def run_swarm_agent(task_def: dict, index: int) -> dict:
            """Run a single swarm agent."""
            async with semaphore:
                profile = task_def.get("profile", "")
                message = task_def.get("message", "")
                
                # Initialize config - inherit from parent agent to get MCP tools
                config = initialize_agent()
                if profile:
                    config.profile = profile
                
                # Inherit MCP tools from parent agent if available
                if hasattr(self.agent.config, 'mcp_servers'):
                    config.mcp_servers = self.agent.config.mcp_servers
                if hasattr(self.agent.config, 'mcp_tools'):
                    config.mcp_tools = self.agent.config.mcp_tools
                
                # Create unique agent number
                agent_number = self.agent.number * 1000 + index + 1
                
                # Create the agent with inherited context (includes MCP)
                sub = Agent(agent_number, config, self.agent.context)
                sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
                
                # Add message
                sub.hist_add_user_message(UserMessage(message=message, attachments=[]))
                
                # Log
                self.agent.context.log.log(
                    type="swarm",
                    heading=f"🐝 Swarm Agent A{agent_number} ({profile}) launched",
                    content=f"Focus: {message.split('Focus: **')[1].split('**')[0] if 'Focus: **' in message else 'Swarm task'}",
                )
                
                try:
                    result = await sub.monologue()
                    sub.history.new_topic()
                    
                    self.agent.context.log.log(
                        type="swarm",
                        heading=f"✅ Swarm Agent A{agent_number} completed",
                        content=f"Output: {len(result)} chars",
                    )
                    
                    return {
                        "index": index,
                        "agent": f"A{agent_number}",
                        "profile": profile,
                        "success": True,
                        "result": result,
                    }
                except Exception as e:
                    self.agent.context.log.log(
                        type="swarm_error",
                        heading=f"❌ Swarm Agent A{agent_number} failed",
                        content=str(e),
                    )
                    return {
                        "index": index,
                        "agent": f"A{agent_number}",
                        "profile": profile,
                        "success": False,
                        "error": str(e),
                    }
        
        # Launch all swarm agents
        coroutines = [run_swarm_agent(task, i) for i, task in enumerate(subtasks)]
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # Process results
        processed = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed.append({
                    "index": i,
                    "agent": f"A{self.agent.number * 1000 + i + 1}",
                    "profile": subtasks[i].get("profile", "unknown"),
                    "success": False,
                    "error": str(result),
                })
            else:
                processed.append(result)
        
        return processed
    
    async def _synthesize_results(self, results: list, mission: str, mission_record: SwarmMission = None, recommendations: dict = None) -> str:
        """Synthesize swarm results into a cohesive response with analytics."""
        
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]
        
        # Calculate actual duration
        actual_duration = mission_record.total_duration if mission_record else 0
        
        # Get analytics insights
        analytics = get_analytics()
        insights = analytics.generate_insights()
        leaderboard = analytics.get_leaderboard()
        
        # Build synthesis
        lines = [
            "# 🐝 SWARM MISSION COMPLETE 🐝",
            "",
            f"**Mission:** {mission}",
            f"**Swarm Size:** {len(results)} agents",
            f"**Success Rate:** {len(successful)}/{len(results)} agents completed",
        ]
        
        # Add analytics section
        if mission_record:
            lines.extend([
                f"**Duration:** {actual_duration:.1f} seconds",
                f"**Effectiveness Score:** {mission_record.effectiveness_score:.1f}/100",
                f"**Task Category:** {mission_record.task_category or 'general'}",
            ])
        
        lines.extend([
            "",
            "---",
            "",
        ])
        
        # Analytics Insights
        if insights:
            lines.append("## 📊 Swarm Analytics Insights")
            lines.append("")
            for insight in insights[:3]:  # Show top 3 insights
                lines.append(f"- {insight}")
            lines.append("")
        
        # Leaderboard
        if leaderboard.get('top_performers'):
            lines.append("## 🏆 Top Performing Agent Profiles")
            lines.append("")
            for i, performer in enumerate(leaderboard['top_performers'][:3], 1):
                lines.append(f"{i}. **{performer['profile']}** - {performer['success_rate']}% success rate ({performer['missions']} missions)")
            lines.append("")
        
        # Recommendations comparison
        if recommendations and mission_record:
            lines.append("## 🎯 Learning & Optimization")
            lines.append("")
            expected = recommendations.get('expected_duration_minutes', 0) * 60
            if expected > 0:
                time_diff = actual_duration - expected
                if abs(time_diff) < 30:
                    lines.append(f"✅ **On Track**: Mission completed close to expected time ({actual_duration/60:.1f} min vs {expected/60:.1f} min expected)")
                elif time_diff < 0:
                    lines.append(f"🚀 **Efficient**: Mission completed {abs(time_diff)/60:.1f} minutes faster than expected!")
                else:
                    lines.append(f"⏱️ **Slower**: Mission took {time_diff/60:.1f} minutes longer than expected. Consider adjusting swarm size.")
            lines.append("")
            lines.append(f"📈 **Based on**: {recommendations.get('based_on_n_missions', 0)} similar past missions")
            lines.append("")
        
        # Summary by profile
        lines.append("## Swarm Composition")
        lines.append("")
        profile_counts = {}
        for r in results:
            profile = r.get("profile", "unknown")
            profile_counts[profile] = profile_counts.get(profile, 0) + 1
        
        for profile, count in sorted(profile_counts.items()):
            success_count = sum(1 for r in successful if r.get("profile") == profile)
            lines.append(f"- **{profile}** ({success_count}/{count} succeeded)")
        lines.append("")
        
        # Individual results
        lines.append("## Detailed Findings")
        lines.append("")
        
        for r in successful:
            agent = r.get("agent", "Unknown")
            profile = r.get("profile", "unknown")
            result = r.get("result", "")
            
            lines.append(f"### {agent} ({profile})")
            lines.append("")
            if len(result) > 500:
                lines.append(f"*{len(result)} character response - showing first/last portions:*")
                lines.append("")
                lines.append("```")
                lines.append(result[:500])
                lines.append("\n... [truncated] ...\n")
                lines.append(result[-300:] if len(result) > 800 else "")
                lines.append("```")
            else:
                lines.append("```")
                lines.append(result)
                lines.append("```")
            lines.append("")
        
        # Failed agents
        if failed:
            lines.append("## ⚠️ Failed Agents")
            lines.append("")
            for r in failed:
                lines.append(f"- **{r.get('agent', 'Unknown')}** ({r.get('profile', 'unknown')}): {r.get('error', 'Unknown error')}")
            lines.append("")
        
        # Synthesis footer
        lines.append("---")
        lines.append("")
        lines.append("### 🎯 Next Steps")
        lines.append("")
        lines.append("The swarm has completed its mission. Review the findings above and let me know if you need:")
        lines.append("- Deeper analysis on any specific area")
        lines.append("- Integration of the findings into a deliverable")
        lines.append("- Another swarm with adjusted parameters")
        lines.append("- Sequential refinement using specific subordinates")
        lines.append("")
        lines.append("💡 **Pro Tip**: The swarm learns from every mission! Future swarms will be optimized based on these results.")
        
        return "\n".join(lines)

    def get_log_object(self):
        return self.agent.context.log.log(
            type="swarm",
            heading=f"🐝 {self.agent.agent_name}: SWARM MODE",
            content="",
            kvps=self.args,
        )
