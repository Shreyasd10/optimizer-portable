#!/usr/bin/env python3
"""Analyzes session history and extracts successful patterns for learning."""
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

OPTIMIZER_HOME = Path.home() / ".factory" / "optimizer"
HISTORY_FILE = Path.home() / ".factory" / "history.json"
MEMORIES_FILE = Path.home() / ".factory" / "memories.md"


def load_history():
    """Load history file."""
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text())
    except:
        return []


def extract_tool_chains(entries):
    """Extract successful tool usage patterns."""
    tool_chains = []
    
    for entry in entries:
        if entry.get("type") == "tool_use":
            tool_chain = entry.get("tool", "")
            if tool_chain:
                tool_chains.append(tool_chain)
    
    return tool_chains


def extract_skill_invocations(entries):
    """Extract skill usage patterns."""
    skills = []
    
    for entry in entries:
        if entry.get("type") == "skill_invocation":
            skill_name = entry.get("skill", "")
            if skill_name:
                skills.append(skill_name)
    
    return skills


def detect_patterns(entries):
    """Detect recurring patterns in session history."""
    patterns = {
        "tool_chains": [],
        "skills_used": [],
        "success_indicators": [],
    }
    
    # Track consecutive tool uses
    recent_tools = []
    recent = entries[-20:] if len(entries) > 20 else entries
    
    for entry in recent:
        if entry.get("type") == "tool_use":
            tool = entry.get("tool", "")
            recent_tools.append(tool)
            
            if len(recent_tools) >= 3:
                chain = " -> ".join(recent_tools[-3:])
                patterns["tool_chains"].append(chain)
        
        elif entry.get("type") == "skill_invocation":
            skill = entry.get("skill", "")
            patterns["skills_used"].append(skill)
    
    return patterns


def store_pattern(key, value, namespace="patterns"):
    """Store pattern in optimizer memory."""
    memory_file = OPTIMIZER_HOME / "memory" / f"{namespace}.json"
    memory_file.parent.mkdir(exist_ok=True)
    
    if memory_file.exists():
        data = json.loads(memory_file.read_text())
    else:
        data = {}
    
    # Don't overwrite existing keys
    if key not in data:
        data[key] = {
            "value": value,
            "metadata": {
                "source": "session-analyzer",
                "analyzed_at": datetime.now().isoformat()
            },
            "stored_at": datetime.now().isoformat() + "Z"
        }
        memory_file.write_text(json.dumps(data, indent=2))
        return True
    return False


def append_to_memories(content):
    """Append insight to memories.md."""
    MEMORIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if not MEMORIES_FILE.exists():
        MEMORIES_FILE.write_text("# Memory\n\n## Auto-Captured Insights\n\n")
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    with open(MEMORIES_FILE, "a") as f:
        f.write(f"- [{timestamp}] {content}\n")


def main():
    try:
        # Load recent history
        history = load_history()
        
        if not history:
            return
        
        # Analyze patterns
        patterns = detect_patterns(history)
        
        # Extract and store tool chains
        if patterns["tool_chains"]:
            chain_counter = Counter(patterns["tool_chains"])
            for chain, count in chain_counter.most_common(3):
                if count >= 2:
                    key = f"tool-chain-{chain[:30].lower().replace(' ', '-').replace('-', '')}"
                    store_pattern(key, f"{chain} (seen {count}x)")
        
        # Extract and store skill usage
        if patterns["skills_used"]:
            skill_counter = Counter(patterns["skills_used"])
            for skill, count in skill_counter.most_common(5):
                if count >= 2:
                    key = f"skill-usage-{skill.lower().replace(' ', '-')}"
                    store_pattern(key, f"{skill} used {count}x")
        
        # Capture session summary
        if len(history) > 10:
            summary = f"Session with {len(history)} interactions"
            append_to_memories(summary)
        
        print(json.dumps({
            "systemMessage": "Session analyzed and patterns stored"
        }))
        
    except Exception as e:
        pass


if __name__ == "__main__":
    main()
