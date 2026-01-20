#!/bin/bash

# Ops Skill Installer for Claude Code

set -e

echo "Installing ops Claude skill..."

# Determine Claude Code skills directory
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Both macOS and Linux use ~/.claude/skills/
    SKILLS_DIR="$HOME/.claude/skills/ops"
else
    echo "Unsupported operating system. Please install manually."
    exit 1
fi

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Check if we're running from the git repo or via curl
if [ -f "skills/ops/SKILL.md" ]; then
    # Running from local repository
    cp skills/ops/SKILL.md "$SKILLS_DIR/SKILL.md"
    echo "✓ Ops skill installed from local repository to: $SKILLS_DIR"
else
    # Download from GitHub
    SKILL_URL="https://raw.githubusercontent.com/friday-james/ops-skill/main/skills/ops/SKILL.md"
    SKILL_PATH="$SKILLS_DIR/SKILL.md"

    if command -v curl &> /dev/null; then
        curl -fsSL "$SKILL_URL" -o "$SKILL_PATH"
    elif command -v wget &> /dev/null; then
        wget -q "$SKILL_URL" -O "$SKILL_PATH"
    else
        echo "Error: Neither curl nor wget found. Please install one of them."
        exit 1
    fi

    echo "✓ Ops skill installed to: $SKILL_PATH"
fi

echo ""
echo "Usage: Type '/ops' in Claude Code to activate"
echo ""
echo "The skill will help you:"
echo "  - Run commands in the background"
echo "  - Monitor logs or task output periodically"
echo "  - Loop continuously for ongoing monitoring"
echo ""
echo "Restart Claude Code to load the skill."
