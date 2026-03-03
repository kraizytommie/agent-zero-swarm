"""
Parallel Subordinate Spawner - Spawn multiple subagents concurrently
"""
import asyncio
from agent import Agent, UserMessage
from python.helpers.tool import Tool, Response
from initialize import initialize_agent


class ParallelDelegation(Tool):
    """
    Spawn multiple subordinate agents in parallel.
    
    Args:
        tasks: List of task definitions with 'profile' and 'message'
        max_parallel: Maximum concurrent subordinates (default: 5)
    """

    async def execute(self, tasks: list = None, max_parallel: int = 5, **kwargs):
        if not tasks or not isinstance(tasks, list):
            return Response(
                message="Error: 'tasks' must be a non-empty list",
                break_loop=False
            )
        
        max_parallel = max(1, min(max_parallel, 20))
        semaphore = asyncio.Semaphore(max_parallel)
        
        async def run_subordinate(task_def: dict, index: int) -> dict:
            async with semaphore:
                profile = task_def.get("profile", "")
                message = task_def.get("message", "")
                
                config = initialize_agent()
                if profile:
                    config.profile = profile
                
                # Inherit MCP tools
                if hasattr(self.agent.config, 'mcp_servers'):
                    config.mcp_servers = self.agent.config.mcp_servers
                if hasattr(self.agent.config, 'mcp_tools'):
                    config.mcp_tools = self.agent.config.mcp_tools
                
                agent_number = self.agent.number * 100 + index + 1
                sub = Agent(agent_number, config, self.agent.context)
                sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
                sub.hist_add_user_message(UserMessage(message=message, attachments=[]))
                
                try:
                    result = await sub.monologue()
                    sub.history.new_topic()
                    return {
                        "index": index,
                        "agent": f"A{agent_number}",
                        "profile": profile or "default",
                        "success": True,
                        "result": result,
                    }
                except Exception as e:
                    return {
                        "index": index,
                        "agent": f"A{agent_number}",
                        "profile": profile or "default",
                        "success": False,
                        "error": str(e),
                    }
        
        coroutines = [run_subordinate(task, i) for i, task in enumerate(tasks)]
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        formatted = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                formatted.append({
                    "index": i,
                    "agent": f"A{self.agent.number * 100 + i + 1}",
                    "profile": tasks[i].get("profile", "default"),
                    "success": False,
                    "error": str(result),
                })
            else:
                formatted.append(result)
        
        successful = sum(1 for r in formatted if r.get("success"))
        
        response = [
            f"## Parallel Execution Complete",
            f"**Summary:** {successful}/{len(tasks)} successful",
            f"",
            f"### Results:",
            f"",
        ]
        
        for r in formatted:
            status = "✅ SUCCESS" if r.get("success") else "❌ FAILED"
            response.append(f"#### {r.get('agent')} ({r.get('profile')}) - {status}")
            if r.get("success"):
                response.append(f"```\n{r.get('result', '')[:500]}...\n```")
            else:
                response.append(f"```\nError: {r.get('error', 'Unknown')}\n```")
            response.append("")
        
        return Response(message="\n".join(response), break_loop=False)
