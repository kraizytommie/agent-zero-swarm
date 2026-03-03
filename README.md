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

## 📦 Quick Start

### Try the Demo First! 🎮

```bash
git clone https://github.com/kraizytommie/agent-zero-swarm.git
cd agent-zero-swarm
python3 swarm_demo.py
```

The demo shows how swarms work without needing to install anything!

---

## 🚀 Installation

### Option 1: Automatic Install
```bash
./install.sh
```

### Option 2: Manual Install

```bash
# Copy to your Agent Zero installation
cp swarm.py /path/to/agent-zero/python/tools/
cp call_subordinates_parallel.py /path/to/agent-zero/python/tools/
cp swarm_analytics_tool.py /path/to/agent-zero/python/tools/
cp swarm_analytics.py /path/to/agent-zero/python/helpers/
cp agent.system.tool.swarm.md /path/to/agent-zero/prompts/
cp agent.system.tool.swarm_analytics.md /path/to/agent-zero/prompts/
```

### Update Agent Configuration

Add to your `agent.yaml`:
```yaml
tools:
  - swarm
  - call_subordinates_parallel
  - swarm_analytics
```

---

## 🎯 Usage

Just tell Agent Zero:
```
"Create a swarm to analyze this codebase for security issues"
```

Or use the tool:
```json
{
  "tool_name": "swarm",
  "tool_args": {
    "mission": "Analyze this codebase",
    "swarm_size": 5,
    "strategy": "review"
  }
}
```

---

## 🎉 Success Stories

- 🌍 **Fantasy RPG World** - 5 continents, 10 kingdoms, full game mechanics
- 🚀 **Sci-Fi Universe** - 100k+ word bible with worlds, tech, factions
- 🔍 **Code Analysis** - Parallel security audits
- 📝 **Documentation** - Multi-angle comprehensive docs

---

**Happy Swarming! 🐝🐝🐝**