# 🐝 Agent Zero - SWARM MODE

> **Unleash a coordinated swarm of AI agents on any task!**

Swarm Mode enables Agent Zero to spawn multiple specialized subordinate agents that work in parallel to accomplish complex tasks faster and more effectively than a single agent.

---

## ✨ Features

- 🚀 **Parallel Execution** - Spawn 2-12 agents working simultaneously
- 🎯 **Smart Task Decomposition** - Automatically breaks missions into subtasks
- 📊 **Swarm Analytics** - Track mission performance and get recommendations
- 🔄 **MCP Inheritance** - Sub-agents inherit parent's MCP configuration
- 🏗️ **Multiple Strategies**:
  - `divide` - Break into components/features
  - `research` - Multiple research angles
  - `review` - Multiple expert reviewers
  - `implement` - Parallel module implementation
  - `auto` - Let the swarm decide

---

## 🎮 Quick Setup

Clone, Copy, and Paste files, Thats it!



---

## 📦 Installation

### Prerequisits
**Must Have Agent Zero Installed**

```bash
git clone https://github.com/agent0ai/agent-zero.git
```
### 1: Clone Repo

```bash
git clone https://github.com/kraizytommie/agent-zero-swarm.git
cd agent-zero-swarm
```

### 2: Copy files to your Agent Zero Directories

```bash
# Copy to your /agent-zero/python/tools/ directory
cp swarm.py
cp call_subordinates_parallel.py
cp swarm_analytics_tool.py

# Copy to your /agent-zero/python/helpers/ directory 
cp swarm_analytics.py 

# Copy to your /agent-zero/prompts/ directory
cp agent.system.tool.swarm.md 
cp agent.system.tool.swarm_analytics.md 
cp agent.system.tool.call_subs_parallel.py #yes to the prompts folder
cp agent.system.tool.call_subs_parallel.md 
```


## 🚀 Usage

### Basic Swarm

Just tell Agent Zero:

```
"Use swarm mode to analyze this codebase for security issues"
```

Or use the tool directly:

```json
{
  "tool_name": "swarm",
  "tool_args": {
    "mission": "Analyze this codebase for security vulnerabilities",
    "swarm_size": 5,
    "strategy": "review"
  }
}
```

### Advanced Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `mission` | The task for the swarm | (required) |
| `swarm_size` | Number of agents (2-12, or "auto") | "auto" |
| `strategy` | Task decomposition strategy | "auto" |

### Strategies

- **`auto`** - Let the swarm analyze and pick the best approach
- **`divide`** - Break task into independent components
- **`research`** - Multiple angles on research/analysis
- **`review`** - Multiple expert reviewers with different focus areas
- **`implement`** - Parallel implementation of modules

---

## 📊 Swarm Analytics

Track your swarm missions and get recommendations:

```
"Show me swarm analytics"
```

Analytics include:
- Mission history and success rates
- Optimal swarm sizes for task types
- Strategy effectiveness
- Performance trends

---

## 🎯 Examples

### Code Analysis
```
"Swarm analyze my codebase for bugs with strategy=review"
```

### Research Task
```
"Create a swarm to research the latest AI frameworks"
```

### Creative Project
```
"Swarm create a complete fantasy RPG world"
```

### Implementation
```
"Swarm implement a web app with auth, database, and API"
```

---

## 🔧 File Structure

```
agent-zero-swarm/
├── swarm.py                                  # Main swarm tool
├── agent.system.tool.call_subs_parallel.py   # Parallel subordinate spawning
├── call_subordinates_parallel.py             # Parallel subordinate spawning
├── agent.system.tool.swarm.md                # Swarm tool prompt
├── agent.system.tool.call_subs_parallel.md   # Parallel subordinate spawning
├── swarm_analytics_tool.py                   # Analytics tool (optional)
├── swarm_analytics.py                        # Analytics helper module (optional)
├── agent.system.tool.swarm_analytics.md      # Analytics prompt (optional)
└── README.md                                 # This file
```

---

## ⚙️ How It Works

1. **Mission Analysis** - The swarm leader analyzes the mission
2. **Task Decomposition** - Breaks mission into subtasks based on strategy
3. **Agent Spawning** - Spawns specialized subordinates for each subtask
4. **Parallel Execution** - All subordinates work simultaneously
5. **Result Synthesis** - Combines all outputs into cohesive result
6. **Analytics Recording** - Records metrics for future optimization

---

## 🐛 Troubleshooting

### Tools not appearing
- Ensure files are in correct directories
- Restart Agent Zero

### Swarm not spawning
- Ensure files are in correct directories
- Restart Agent Zero


### Analytics not working
- Ensure `swarm_analytics.py` is in `python/helpers/`
- Check write permissions for analytics file
- Ensure files are in correct directories
- Restart Agent Zero
---

## 🎉 Success Stories

Users have used Swarm Mode to:
- 🌍 Build complete fantasy RPG worlds (5 continents, 10 kingdoms!)
- 🚀 Create sci-fi universes with 100k+ word bibles
- 🔍 Analyze large codebases in parallel
- 📝 Generate comprehensive documentation
- 🎨 Design complex systems and architectures

---

## 🤝 Credits

Swarm Mode created by collaborative development with Agent Zero users.

**Key Features:**
- Async parallel execution using asyncio
- Smart task decomposition
- Self-learning analytics
- MCP tool inheritance for sub-agents
- Nested swarm support (swarms within swarms!)

---

## 📄 License

Same as Agent Zero - use freely and share improvements!

---

**Anything's Possible! Happy Swarming! 🐝🐝🐝**
