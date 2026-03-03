#!/bin/bash
# Swarm Mode Installation Script for Agent Zero

echo "🐝 Agent Zero Swarm Mode Installer 🐝"
echo "========================================"
echo ""

# Detect Agent Zero installation
if [ -d "$HOME/Agent-Zero/a0-0" ]; then
    A0_PATH="$HOME/Agent-Zero/a0-0"
elif [ -d "$HOME/agent-zero/a0-0" ]; then
    A0_PATH="$HOME/agent-zero/a0-0"
elif [ -d "/opt/Agent-Zero/a0-0" ]; then
    A0_PATH="/opt/Agent-Zero/a0-0"
else
    echo "❌ Could not find Agent Zero installation!"
    echo "Please enter the path to your Agent Zero a0-0 directory:"
    read A0_PATH
fi

if [ ! -d "$A0_PATH" ]; then
    echo "❌ Invalid path: $A0_PATH"
    exit 1
fi

echo "✅ Found Agent Zero at: $A0_PATH"
echo ""

# Install tool files
echo "📦 Installing tool files..."
cp swarm.py "$A0_PATH/python/tools/"
cp call_subordinates_parallel.py "$A0_PATH/python/tools/"
cp swarm_analytics_tool.py "$A0_PATH/python/tools/"
cp swarm_analytics.py "$A0_PATH/python/helpers/"

# Install prompt files
echo "📝 Installing prompt files..."
cp agent.system.tool.swarm.md "$A0_PATH/prompts/"
cp agent.system.tool.swarm_analytics.md "$A0_PATH/prompts/"

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Restart Agent Zero"
echo "   2. Try: 'Create a swarm to analyze this codebase'"
echo ""
echo "Happy Swarming! 🐝🐝🐝"