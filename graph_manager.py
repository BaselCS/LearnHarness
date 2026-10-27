"""
State and Knowledge Graph Manager for LearnHarness in AGY.
Maintains:
- Active session state (state.json)
- Knowledge propositions & mastery levels (knowledge_graph.json)
- Markdown Mermaid visual rendering (KNOWLEDGE_GRAPH.md)
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

WORKSPACE_DIR = "/home/basel/Work/LearnHarness"
STATE_FILE = os.path.join(WORKSPACE_DIR, "state.json")
GRAPH_FILE = os.path.join(WORKSPACE_DIR, "knowledge_graph.json")
MERMAID_FILE = os.path.join(WORKSPACE_DIR, "KNOWLEDGE_GRAPH.md")

def load_json(path: str, default: Any) -> Any:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_state() -> Dict[str, Any]:
    return load_json(STATE_FILE, {
        "active_topic": None,
        "mode": "idle", # "probe", "plan", "teach", "drill"
        "current_strand": None,
        "history": [],
        "last_updated": None
    })

def update_state(**kwargs) -> Dict[str, Any]:
    state = get_state()
    state.update(kwargs)
    state["last_updated"] = datetime.now().isoformat()
    save_json(STATE_FILE, state)
    return state

def get_knowledge_graph() -> Dict[str, Any]:
    return load_json(GRAPH_FILE, {
        "nodes": {},
        "edges": []
    })

def upsert_concept(
    node_id: str,
    label: str,
    status: str, # "mastered", "learning", "gap", "planned"
    prerequisites: Optional[List[str]] = None,
    notes: str = ""
) -> None:
    graph = get_knowledge_graph()
    graph["nodes"][node_id] = {
        "label": label,
        "status": status,
        "prerequisites": prerequisites or [],
        "notes": notes,
        "updated_at": datetime.now().isoformat()
    }
    
    # Update edges
    if prerequisites:
        for pre in prerequisites:
            edge = {"from": pre, "to": node_id}
            if edge not in graph["edges"]:
                graph["edges"].append(edge)
                
    save_json(GRAPH_FILE, graph)
    render_mermaid_graph(graph)

def render_mermaid_graph(graph: Dict[str, Any]) -> None:
    lines = [
        "# Knowledge Graph — Live Representation",
        f"*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "```mermaid",
        "flowchart TD"
    ]
    
    # Node styles
    status_classes = {
        "mastered": "fill:#2e7d32,stroke:#1b5e20,color:#fff",
        "learning": "fill:#f57c00,stroke:#e65100,color:#fff",
        "gap": "fill:#c62828,stroke:#b71c1c,color:#fff",
        "planned": "fill:#37474f,stroke:#263238,color:#fff"
    }
    
    for node_id, data in graph["nodes"].items():
        clean_id = node_id.replace("-", "_").replace(" ", "_")
        label = data.get("label", node_id).replace('"', "'")
        lines.append(f'    {clean_id}["{label}"]')
    
    for edge in graph["edges"]:
        from_id = edge["from"].replace("-", "_").replace(" ", "_")
        to_id = edge["to"].replace("-", "_").replace(" ", "_")
        lines.append(f"    {from_id} --> {to_id}")
        
    for node_id, data in graph["nodes"].items():
        clean_id = node_id.replace("-", "_").replace(" ", "_")
        st = data.get("status", "planned")
        style = status_classes.get(st, status_classes["planned"])
        lines.append(f"    style {clean_id} {style}")
        
    lines.extend([
        "```",
        "",
        "### Legend",
        "- 🟢 **Green (Mastered):** Confirmed understanding via active recall.",
        "- 🟠 **Orange (Learning):** Active in-progress topic.",
        "- 🔴 **Red (Gap / Misconception):** Diagnosed misconception to repair.",
        "- ⚪ **Gray (Planned):** Next dependency path."
    ])
    
    with open(MERMAID_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    upsert_concept("linalg_vec", "Vector as Displacement", "mastered")
    upsert_concept("linalg_span", "Linear Combinations & Span", "mastered", ["linalg_vec"])
    upsert_concept("linalg_trans", "Matrices as Linear Transforms", "learning", ["linalg_span"])
    upsert_concept("linalg_det", "Determinant (Area/Volume Scaling)", "planned", ["linalg_trans"])
    print("Graph initialized and rendered to:", MERMAID_FILE)
