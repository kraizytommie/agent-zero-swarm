### swarm_analytics

📊 **SWARM ANALYTICS** - Track and optimize your swarm missions!

Query your swarm mission history to get insights, statistics, and recommendations.

**What it does:**
- Tracks all swarm missions and their performance
- Learns optimal swarm sizes for different task types
- Provides recommendations based on past missions
- Shows which strategies work best
- Ranks agent profile performance

**Parameters:**
- `query` (optional): Type of analytics to retrieve
  - `"stats"`: Mission statistics and performance metrics (default)
  - `"insights"`: AI-generated insights from mission history
  - `"leaderboard"`: Top performing agent profiles
- `days` (optional): Number of days to look back (default: 30)

**When to use SWARM ANALYTICS:**
- After running several swarms to check performance
- To optimize swarm configuration for your use case
- To see which strategies work best for your tasks
- To identify your most effective agent profiles

**Example - View Statistics:**
~~~json
{
    "thoughts": [
        "I want to see how my swarms have been performing...",
        "I'll check the analytics for the last 30 days"
    ],
    "tool_name": "swarm_analytics",
    "tool_args": {
        "query": "stats",
        "days": 30
    }
}
~~~

**Example - Get Insights:**
~~~json
{
    "thoughts": [
        "I want to understand what makes my swarms successful...",
        "I'll get AI insights from the analytics"
    ],
    "tool_name": "swarm_analytics",
    "tool_args": {
        "query": "insights"
    }
}
~~~

**Example - View Leaderboard:**
~~~json
{
    "thoughts": [
        "I want to see which agent profiles perform best...",
        "I'll check the leaderboard"
    ],
    "tool_name": "swarm_analytics",
    "tool_args": {
        "query": "leaderboard"
    }
}
~~~

**Analytics Include:**
- Total missions and success rates
- Average mission duration
- Strategy performance comparison
- Task category breakdown
- Optimal swarm size recommendations
- Agent profile effectiveness rankings

**Note:** Analytics are stored locally and improve over time as you run more swarms!
