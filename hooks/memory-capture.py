#!/usr/bin/env python3
"""Captures memories from prompts and appends to memories.md and optimizer memory."""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

OPTIMIZER_HOME = Path.home() / ".factory" / "optimizer"
sys.path.insert(0, str(OPTIMIZER_HOME))

try:
    from ruflo_bridge import RufloBridge
    BRIDGE = RufloBridge()
except ImportError:
    BRIDGE = None


def get_memory_file(personal=False, project_dir=None):
    """Get the appropriate markdown memory file path."""
    if personal:
        return Path.home() / ".factory" / "memories.md"
    
    if project_dir and Path(project_dir).exists():
        project_factory = Path(project_dir) / ".factory"
        project_factory.mkdir(exist_ok=True)
        mem_file = project_factory / "memories.md"
        if mem_file.exists() or os.access(Path(project_dir), os.W_OK):
            return mem_file
    
    return Path.home() / ".factory" / "memories.md"


def extract_content(prompt):
    """Extract memory content from prompt based on triggers."""
    prompt = prompt.strip()
    
    # # = project, ## = personal
    if prompt.startswith("##"):
        return prompt[2:].strip(), "personal"
    if prompt.startswith("#"):
        return prompt[1:].strip(), "project"
    
    # Phrase triggers
    triggers = ["remember this:", "remember:", "note:", "save this:"]
    prompt_lower = prompt.lower()
    for trigger in triggers:
        if trigger in prompt_lower:
            idx = prompt_lower.index(trigger)
            content = prompt[idx + len(trigger):].strip()
            personal = "personal" in prompt_lower[:idx]
            return content, "personal" if personal else "project"
    
    return None, None


def append_to_markdown(mem_file, content):
    """Append entry to markdown memory file."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Ensure directory exists
    mem_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create file with header if it doesn't exist
    if not mem_file.exists():
        mem_file.write_text("# Memory\n\n## Entries\n\n")
    
    # Append entry
    with open(mem_file, "a") as f:
        f.write(f"- [{timestamp}] {content}\n")
    
    return True


def store_in_optimizer(key, value, namespace="patterns"):
    """Store in optimizer's JSON memory via ruflo_bridge."""
    if BRIDGE is None:
        # Direct JSON fallback
        memory_file = OPTIMIZER_HOME / "memory" / f"{namespace}.json"
        memory_file.parent.mkdir(exist_ok=True)
        
        if memory_file.exists():
            data = json.loads(memory_file.read_text())
        else:
            data = {}
        
        data[key] = {
            "value": value,
            "metadata": {"source": "hook", "captured_at": datetime.now().isoformat()},
            "stored_at": datetime.now().isoformat() + "Z"
        }
        
        memory_file.write_text(json.dumps(data, indent=2))
        return True
    
    result = BRIDGE._memory_store_local(
        key=key,
        value=value,
        namespace=namespace,
        metadata={"source": "hook", "captured_at": datetime.now().isoformat()}
    )
    return result.success


def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")
        
        content, memory_type = extract_content(prompt)
        
        if not content:
            return
        
        personal = memory_type == "personal"
        project_dir = os.environ.get("FACTORY_PROJECT_DIR")
        
        # Get memory file
        mem_file = get_memory_file(personal=personal, project_dir=project_dir)
        
        # Append to markdown
        append_to_markdown(mem_file, content)
        
        # Store in optimizer memory
        key = content[:50].lower().replace(" ", "-").replace(",", "").replace(".", "")
        store_in_optimizer(key, content)
        
        # Output confirmation
        print(json.dumps({
            "systemMessage": f"Captured to {'personal' if personal else 'project'} memory"
        }))
        
    except Exception as e:
        # Fail silently to not disrupt workflow
        pass


if __name__ == "__main__":
    main()
