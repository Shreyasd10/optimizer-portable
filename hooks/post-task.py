#!/usr/bin/env python3
"""Records post-task outcomes for learning."""
import json
import sys
from datetime import datetime
from pathlib import Path

OPTIMIZER_HOME = Path.home() / ".factory" / "optimizer"
MEMORY_FILE = OPTIMIZER_HOME / "memory" / "patterns.json"


def store_outcome(task_id, success, details=None):
    """Store task outcome pattern."""
    MEMORY_FILE.parent.mkdir(exist_ok=True)
    
    data = {}
    if MEMORY_FILE.exists():
        try:
            data = json.loads(MEMORY_FILE.read_text())
        except:
            data = {}
    
    # Store in outcomes namespace or create outcomes section
    if "task_outcomes" not in data:
        data["task_outcomes"] = {}
    
    data["task_outcomes"][task_id] = {
        "success": success,
        "details": details,
        "completed_at": datetime.now().isoformat()
    }
    
    MEMORY_FILE.write_text(json.dumps(data, indent=2))
    return True


def main():
    try:
        data = json.load(sys.stdin)
        
        task_id = data.get("task_id", f"task-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        success = data.get("success", True)
        details = data.get("details", {})
        
        store_outcome(task_id, success, details)
        
        print(json.dumps({
            "systemMessage": f"Task outcome recorded: {'success' if success else 'failed'}"
        }))
        
    except Exception as e:
        pass


if __name__ == "__main__":
    main()
