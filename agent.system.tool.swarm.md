### swarm

🐝 **SWARM MODE** - Unleash a coordinated swarm of agents on complex tasks!

Say "create a swarm to..." and watch multiple specialized agents work in parallel.

**What it does:**
- Automatically breaks down your mission into subtasks
- Spawns specialized agents (security, performance, architect, coder, etc.)
- Executes all agents in parallel for maximum speed
- Synthesizes results into a cohesive report

**Parameters:**
- `mission` (required): The task/mission for the swarm to accomplish
- `swarm_size` (optional): Number of agents (2-12, default: "auto" = 4)
- `strategy` (optional): How to break down the task:
  - `"auto"`: Intelligently choose based on your mission (default)
  - `"divide"`: Divide by components/modules
  - `"research"`: Multiple research angles
  - `"review"`: Multiple reviewer perspectives
  - `"implement"`: Divide implementation work

**When to use SWARM MODE:**
- Code reviews (security + performance + maintainability + architecture)
- Research tasks (multiple angles simultaneously)
- Complex implementations (split across modules)
- Analysis tasks (different perspectives)
- Any task where parallel work beats sequential

**Example - Security Audit Swarm:**
~~~json
{
    "thoughts": [
        "I need a comprehensive security audit of this codebase...",
        "I'll deploy a swarm with different security expertise angles"
    ],
    "tool_name": "swarm",
    "tool_args": {
        "mission": "Perform a comprehensive security audit of the authentication system. Check for: SQL injection, XSS, CSRF, authentication bypasses, session management flaws, and insecure dependencies.",
        "swarm_size": 5,
        "strategy": "review"
    }
}
~~~

**Example - Research Swarm:**
~~~json
{
    "thoughts": [
        "I need to research the best approach for this problem...",
        "I'll swarm multiple research angles in parallel"
    ],
    "tool_name": "swarm",
    "tool_args": {
        "mission": "Research the best vector database options for our RAG system. Consider: Pinecone, Weaviate, Chroma, Qdrant, and Milvus. Evaluate on performance, cost, features, and ease of use.",
        "swarm_size": 6,
        "strategy": "research"
    }
}
~~~

**Example - Implementation Swarm:**
~~~json
{
    "thoughts": [
        "I need to build this feature end-to-end...",
        "I'll swarm the implementation across specialized agents"
    ],
    "tool_name": "swarm",
    "tool_args": {
        "mission": "Build a complete user authentication system with: login/logout, password reset, email verification, JWT tokens, and session management.",
        "swarm_size": 4,
        "strategy": "implement"
    }
}
~~~

**Pro Tips:**
- Start with `swarm_size: "auto"` and adjust based on results
- Be specific in your mission for better task distribution
- Use `"review"` strategy for audits and code reviews
- Use `"research"` strategy when exploring options
- Use `"implement"` strategy for building features
- The swarm automatically assigns appropriate agent profiles

**Note:** Each swarm agent operates independently. They don't share state but their results are synthesized at the end.
