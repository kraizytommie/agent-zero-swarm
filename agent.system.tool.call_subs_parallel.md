{{if agent_profiles}}
### call_subordinates_parallel

Spawn multiple subordinate agents in parallel to execute independent tasks concurrently.
This is much faster than calling subordinates sequentially when tasks don't depend on each other.

**Use this when:**
- You have multiple independent subtasks that can run simultaneously
- You need to analyze multiple files, run multiple tests, or gather data from different sources
- You want to speed up workflow by parallelizing work

**Parameters:**
- `tasks` (required): Array of task objects, each with:
  - `profile`: Agent profile to use (e.g., "coder", "scientist", "engineer"). Leave empty for default.
  - `message`: Detailed task description for the subordinate
- `max_parallel` (optional): Maximum number of subordinates to run at once (default: 5, max: 20)

**Example usage - Analyze multiple files:**
~~~json
{
    "thoughts": [
        "I need to analyze 3 different log files independently...",
        "These tasks don't depend on each other, so I'll run them in parallel"
    ],
    "tool_name": "call_subordinates_parallel",
    "tool_args": {
        "tasks": [
            {
                "profile": "analyst",
                "message": "Analyze /var/log/syslog for error patterns and summarize findings"
            },
            {
                "profile": "analyst",
                "message": "Analyze /var/log/auth.log for suspicious login attempts and summarize findings"
            },
            {
                "profile": "analyst",
                "message": "Analyze /var/log/nginx/access.log for traffic patterns and summarize findings"
            }
        ],
        "max_parallel": 3
    }
}
~~~

**Example usage - Code review multiple components:**
~~~json
{
    "thoughts": [
        "I need to review the authentication, database, and API layers...",
        "Each can be reviewed independently in parallel"
    ],
    "tool_name": "call_subordinates_parallel",
    "tool_args": {
        "tasks": [
            {
                "profile": "security",
                "message": "Review the authentication module for security vulnerabilities. Focus on: password handling, session management, and JWT implementation."
            },
            {
                "profile": "engineer",
                "message": "Review the database layer for performance issues. Focus on: query optimization, indexing, and connection pooling."
            },
            {
                "profile": "architect",
                "message": "Review the API layer for design patterns. Focus on: REST conventions, error handling, and response consistency."
            }
        ],
        "max_parallel": 3
    }
}
~~~

**response handling**
- Results are returned in a consolidated format with each subordinate's output labeled
- You might be part of long chain of subordinates, avoid slow and expensive rewriting subordinate responses, instead use `§§include(<path>)` alias to include the response as is
- Failed subordinates are indicated clearly but don't block other results

**available profiles:**
{{agent_profiles}}
{{endif}}
