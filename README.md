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

## 🎮 Quick Demo (No Install Required!)

Try the interactive demo to see how swarms work:

```bash
git clone https://github.com/kraizytommie/agent-zero-swarm.git
cd agent-zero-swarm
python3 swarm_demo.py
```

---

## 📦 Installation

### Option 1: Automatic Install

```bash
git clone https://github.com/kraizytommie/agent-zero-swarm.git
cd agent-zero-swarm
./install.sh
```

### Option 2: Manual Install

```bash
# Copy to your Agent Zero installation
cp swarm.py /path/to/agent-zero/python/tools/
cp call_subordinates_parallel.py /path/to/agent-zero/python/tools/
cp swarm_analytics_tool.py /path/to/agent-zero/python/tools/
cp swarm_analytics.py /path/to/agent-zero/python/helpers/

# Copy prompt files
cp agent.system.tool.swarm.md /path/to/agent-zero/prompts/
cp agent.system.tool.swarm_analytics.md /path/to/agent-zero/prompts/
```

### 3. Update Agent Configuration

Add to your `agent.yaml` or Agent configuration:

```yaml
# Add these tools to your agent configuration
tools:
  - swarm
  - call_subordinates_parallel
  - swarm_analytics
```

---

## 🚀 Usage

### Basic Swarm

Just tell Agent Zero:

```
"Create a swarm to analyze this codebase for security issues"
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
├── swarm.py                      # Main swarm tool
├── call_subordinates_parallel.py # Parallel subordinate spawning
├── swarm_analytics_tool.py       # Analytics tool
├── swarm_analytics.py            # Analytics helper module
├── swarm_demo.py                 # Interactive demo (try this first!)
├── agent.system.tool.swarm.md    # Swarm tool prompt
├── agent.system.tool.swarm_analytics.md  # Analytics prompt
├── install.sh                    # One-click installer
└── README.md                     # This file
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
- Check tool registration in agent config

### Swarm not spawning
- Check that `call_subordinates_parallel.py` is properly installed
- Verify MCP configuration is inherited

### Analytics not working
- Ensure `swarm_analytics.py` is in `python/helpers/`
- Check write permissions for analytics file

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

**Happy Swarming! 🐝🐝🐝**
