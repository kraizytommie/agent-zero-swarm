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
        
        # Parse swarm size
        try:
            if str(swarm_size).lower() == "auto":
                size = recommendations.get('recommended_swarm_size', 4)
            else:
                size = int(swarm_size)
                size = max(2, min(size, 12))
        except:
            size = 4
        
        # Use recommended strategy if auto
        if strategy == "auto" and recommendations.get('recommended_strategy'):
            strategy = recommendations.get('recommended_strategy')
        
        # Validate strategy
        valid_strategies = ["auto", "divide", "research", "review", "implement"]
        if strategy not in valid_strategies:
            strategy = "auto"
        
        # Create mission record
        mission_record = SwarmMission(
            mission_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            strategy=strategy,
            swarm_size=size,
            max_parallel=min(size, 6),
            task_description=mission,
            agent_profiles=[],
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
            },
        )
        
        # Generate subtasks
        subtasks = await self._generate_subtasks(mission, size, strategy)
        
        if not subtasks:
            return Response(
                message="❌ **Swarm Error:** Could not generate subtasks for this mission.",
                break_loop=False
            )
        
        mission_record.agent_profiles = [t.get('profile', 'default') for t in subtasks]
        
        # Execute swarm
        results = await self._execute_swarm(subtasks, mission)
        
        # Complete and save
        mission_record.complete(results)
        analytics.record_mission(mission_record)
        
        # Synthesize
        synthesis = await self._synthesize_results(results, mission, mission_record, recommendations)
        
        return Response(message=synthesis, break_loop=False)
    
    async def _generate_subtasks(self, mission: str, size: int, strategy: str) -> list:
        """Generate subtasks for the swarm."""
        
        strategy_profiles = {
            "divide": [
                ("architect", "Design overall structure"),
                ("coder", "Implement core functionality"),
                ("tester", "Create tests"),
                ("documenter", "Write documentation"),
            ],
            "research": [
                ("researcher", "Deep technical research"),
                ("analyst", "Analyze requirements"),
                ("investigator", "Research best practices"),
            ],
            "review": [
                ("security", "Security audit"),
                ("performance", "Performance review"),
                ("maintainer", "Code maintainability"),
                ("architect", "Architecture review"),
            ],
            "implement": [
                ("coder", "Implement module A"),
                ("coder", "Implement module B"),
                ("engineer", "Integration layer"),
                ("tester", "Unit tests"),
            ],
        }
        
        # Auto-detect strategy
        if strategy == "auto":
            mission_lower = mission.lower()
            if any(kw in mission_lower for kw in ["review", "audit", "check"]):
                strategy = "review"
            elif any(kw in mission_lower for kw in ["research", "investigate"]):
                strategy = "research"
            elif any(kw in mission_lower for kw in ["build", "create", "implement"]):
                strategy = "implement"
            else:
                strategy = "divide"
        
        base_profiles = strategy_profiles.get(strategy, strategy_profiles["divide"])
        
        subtasks = []
        for i in range(min(size, len(base_profiles))):
            profile, focus = base_profiles[i % len(base_profiles)]
            subtask = {
                "profile": profile,
                "message": f"SWARM MISSION - Agent {i+1} of {size}\n\nMission: {mission}\n\nYour Role: {profile}\nFocus: {focus}",
            }
            subtasks.append(subtask)
        
        return subtasks
    
    async def _execute_swarm(self, subtasks: list, mission: str) -> list:
        """Execute the swarm in parallel."""
        
        max_parallel = min(len(subtasks), 6)
        semaphore = asyncio.Semaphore(max_parallel)
        
        async def run_swarm_agent(task_def: dict, index: int) -> dict:
            async with semaphore:
                profile = task_def.get("profile", "")
                message = task_def.get("message", "")
                
                # Initialize config with MCP inheritance
                config = initialize_agent()
                if profile:
                    config.profile = profile
                
                # Inherit MCP tools
                if hasattr(self.agent.config, 'mcp_servers'):
                    config.mcp_servers = self.agent.config.mcp_servers
                if hasattr(self.agent.config, 'mcp_tools'):
                    config.mcp_tools = self.agent.config.mcp_tools
                
                agent_number = self.agent.number * 1000 + index + 1
                
                sub = Agent(agent_number, config, self.agent.context)
                sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
                sub.hist_add_user_message(UserMessage(message=message, attachments=[]))
                
                self.agent.context.log.log(
                    type="swarm",
                    heading=f"🐝 Swarm Agent A{agent_number} ({profile}) launched",
                    content=f"Focus: {message[:100]}...",
                )
                
                try:
                    result = await sub.monologue()
                    sub.history.new_topic()
                    
                    return {
                        "index": index,
                        "agent": f"A{agent_number}",
                        "profile": profile,
                        "success": True,
                        "result": result,
                    }
                except Exception as e:
                    return {
                        "index": index,
                        "agent": f"A{agent_number}",
                        "profile": profile,
                        "success": False,
                        "error": str(e),
                    }
        
        coroutines = [run_swarm_agent(task, i) for i, task in enumerate(subtasks)]
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
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
    
    async def _synthesize_results(self, results: list, mission: str, mission_record, recommendations) -> str:
        """Synthesize swarm results."""
        
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]
        
        lines = [
            "# 🐝 SWARM MISSION COMPLETE 🐝",
            "",
            f"**Mission:** {mission}",
            f"**Swarm Size:** {len(results)} agents",
            f"**Success Rate:** {len(successful)}/{len(results)} agents completed",
        ]
        
        if mission_record:
            lines.extend([
                f"**Duration:** {mission_record.total_duration:.1f} seconds",
            ])
        
        lines.extend(["", "---", "", "## Detailed Findings", ""])
        
        for r in successful:
            agent = r.get("agent", "Unknown")
            profile = r.get("profile", "unknown")
            result = r.get("result", "")
            
            lines.append(f"### {agent} ({profile})")
            lines.append(f"```\n{result[:1000]}...\n```" if len(result) > 1000 else f"```\n{result}\n```")
            lines.append("")
        
        return "\n".join(lines)
