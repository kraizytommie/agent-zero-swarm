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

# Create backup directory
BACKUP_DIR="$A0_PATH/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "📁 Backup directory: $BACKUP_DIR"

# Install tool files
echo ""
echo "📦 Installing tool files..."
cp -v swarm.py "$A0_PATH/python/tools/" 2>/dev/null || echo "  swarm.py -> python/tools/"
cp -v call_subordinates_parallel.py "$A0_PATH/python/tools/" 2>/dev/null || echo "  call_subordinates_parallel.py -> python/tools/"
cp -v swarm_analytics_tool.py "$A0_PATH/python/tools/" 2>/dev/null || echo "  swarm_analytics_tool.py -> python/tools/"
cp -v swarm_analytics.py "$A0_PATH/python/helpers/" 2>/dev/null || echo "  swarm_analytics.py -> python/helpers/"

# Install prompt files
echo ""
echo "📝 Installing prompt files..."
cp -v agent.system.tool.swarm.md "$A0_PATH/prompts/" 2>/dev/null || echo "  agent.system.tool.swarm.md -> prompts/"
cp -v agent.system.tool.swarm_analytics.md "$A0_PATH/prompts/" 2>/dev/null || echo "  agent.system.tool.swarm_analytics.md -> prompts/"

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Restart Agent Zero"
echo "   2. Try: 'Create a swarm to analyze this codebase'"
echo "   3. Or: 'Swarm help me build a website'"
echo ""
echo "📚 Documentation: ./README.md"
echo ""
echo "Happy Swarming! 🐝🐝🐝"
