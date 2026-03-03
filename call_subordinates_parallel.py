"""
Parallel Subordinate Spawner - Spawn multiple subagents concurrently

This tool allows spawning multiple subordinates in parallel and gathering their results.
Useful for tasks that can be split into independent subtasks and executed simultaneously.
"""
import asyncio
from agent import Agent, UserMessage
from python.helpers.tool import Tool, Response
from initialize import initialize_agent
from python.extensions.hist_add_tool_result import _90_save_tool_call_file as save_tool_call_file


class ParallelDelegation(Tool):
    """
    Spawn multiple subordinate agents in parallel and gather their results.
    
    Args:
        tasks: List of task definitions, each containing:
            - profile: Agent profile to use (empty for default)
            - message: Task description for the subordinate
        max_parallel: Maximum number of subordinates to run concurrently (default: 5)
    
    Example usage:
    {
        "tool_name": "call_subordinates_parallel",
        "tool_args": {
            "tasks": [
                {"profile": "coder", "message": "Implement feature A"},
                {"profile": "coder", "message": "Implement feature B"},
                {"profile": "scientist", "message": "Analyze dataset X"}
            ],
            "max_parallel": 3
        }
    }
    """

    async def execute(self, tasks: list = None, max_parallel: int = 5, **kwargs):
        if not tasks or not isinstance(tasks, list):
            return Response(
                message="Error: 'tasks' must be a non-empty list of task definitions",
                break_loop=False
            )
        
        # Validate task definitions
        for i, task in enumerate(tasks):
            if not isinstance(task, dict):
                return Response(
                    message=f"Error: Task at index {i} must be a dictionary with 'message' field",
                    break_loop=False
                )
            if "message" not in task:
                return Response(
                    message=f"Error: Task at index {i} is missing required 'message' field",
                    break_loop=False
                )
        
        # Limit max_parallel to reasonable bounds
        max_parallel = max(1, min(max_parallel, 20))
        
        self.agent.context.log.log(
            type="info",
            heading=f"Spawning {len(tasks)} subordinates with max_parallel={max_parallel}",
            content="",
        )

        # Semaphore to control concurrency
        semaphore = asyncio.Semaphore(max_parallel)
        
        async def run_subordinate(task_def: dict, index: int) -> dict:
            """Run a single subordinate with semaphore-controlled concurrency."""
            async with semaphore:
                profile = task_def.get("profile", "")
                message = task_def.get("message", "")
                
                # Initialize config for this subordinate - inherit from parent
                config = initialize_agent()
                if profile:
                    config.profile = profile
                
                # Inherit MCP tools from parent agent if available
                if hasattr(self.agent.config, 'mcp_servers'):
                    config.mcp_servers = self.agent.config.mcp_servers
                if hasattr(self.agent.config, 'mcp_tools'):
                    config.mcp_tools = self.agent.config.mcp_tools
                
                # Create unique agent number based on parent number and index
                agent_number = self.agent.number * 100 + index + 1
                
                # Create the subordinate agent with inherited context (includes MCP)
                sub = Agent(agent_number, config, self.agent.context)
                sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
                
                # Add the task message
                sub.hist_add_user_message(UserMessage(message=message, attachments=[]))
                
                # Log start
                self.agent.context.log.log(
                    type="subagent",
                    heading=f"Subordinate A{agent_number} started",
                    content=message[:100] + "..." if len(message) > 100 else message,
                    kvps={"profile": profile or "default"},
                )
                
                try:
                    # Run the subordinate
                    result = await sub.monologue()
                    
                    # Seal the topic
                    sub.history.new_topic()
                    
                    # Log completion
                    self.agent.context.log.log(
                        type="subagent",
                        heading=f"Subordinate A{agent_number} completed",
                        content=f"Result length: {len(result)} chars",
                    )
                    
                    return {
                        "index": index,
                        "agent": f"A{agent_number}",
                        "profile": profile or "default",
                        "success": True,
                        "result": result,
                    }
                except Exception as e:
                    error_msg = str(e)
                    self.agent.context.log.log(
                        type="error",
                        heading=f"Subordinate A{agent_number} failed",
                        content=error_msg,
                    )
                    return {
                        "index": index,
                        "agent": f"A{agent_number}",
                        "profile": profile or "default",
                        "success": False,
                        "error": error_msg,
                    }
        
        # Create tasks for all subordinates
        coroutines = [run_subordinate(task, i) for i, task in enumerate(tasks)]
        
        # Run all subordinates concurrently with controlled parallelism
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # Process results
        formatted_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                formatted_results.append({
                    "index": i,
                    "agent": f"A{self.agent.number * 100 + i + 1}",
                    "profile": tasks[i].get("profile", "default"),
                    "success": False,
                    "error": str(result),
                })
            else:
                formatted_results.append(result)
        
        # Build response
        successful = sum(1 for r in formatted_results if r.get("success"))
        failed = len(formatted_results) - successful
        
        response_parts = [
            f"## Parallel Subordinate Execution Complete",
            f"",
            f"**Summary:** {successful}/{len(tasks)} successful, {failed} failed",
            f"**Max Parallelism:** {max_parallel}",
            f"",
            f"### Results:",
            f"",
        ]
        
        for r in formatted_results:
            agent_name = r.get("agent", "Unknown")
            profile = r.get("profile", "default")
            success = r.get("success", False)
            
            status = "✅ SUCCESS" if success else "❌ FAILED"
            response_parts.append(f"#### {agent_name} ({profile}) - {status}")
            
            if success:
                result_text = r.get("result", "")
                # Hint for long responses
                if len(result_text) >= save_tool_call_file.LEN_MIN:
                    response_parts.append(f"*Result is long ({len(result_text)} chars) - consider using §§include(<path>) to reference it*")
                response_parts.append(f"```\n{result_text}\n```")
            else:
                response_parts.append(f"```\nError: {r.get('error', 'Unknown error')}\n```")
            
            response_parts.append("")
        
        final_response = "\n".join(response_parts)
        
        # Check if any results are long enough to warrant a hint
        additional = None
        if any(len(r.get("result", "")) >= save_tool_call_file.LEN_MIN 
               for r in formatted_results if r.get("success")):
            hint = self.agent.read_prompt("fw.hint.call_sub.md")
            if hint:
                additional = hint
        
        return Response(
            message=final_response,
            break_loop=False,
            additional=additional,
        )
