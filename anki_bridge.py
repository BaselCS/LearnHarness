"""
Anki Bridge for LearnHarness:
- Direct AnkiConnect injection (if Anki is open with AnkiConnect addon)
- Auto-detects English & Arabic Anki models (Basic / Cloze / قالب البطاقات الأساسي / قالب بطاقات النص المخفي)
- Fallback to TSV auto-export (if Anki is closed)
"""
import json
import os
import urllib.request
from typing import List, Dict, Any, Optional

ANKI_CONNECT_URL = "http://127.0.0.1:8765"

def invoke_anki(action: str, params: Optional[Dict[str, Any]] = None) -> Any:
    payload = {"action": action, "version": 6}
    if params:
        payload["params"] = params
    req = urllib.request.Request(
        ANKI_CONNECT_URL,
        data=json.dumps(payload).encode("utf-8")
    )
    with urllib.request.urlopen(req, timeout=3) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if res.get("error"):
            raise RuntimeError(res["error"])
        return res.get("result")

def is_anki_connect_available() -> bool:
    try:
        ver = invoke_anki("version")
        return ver is not None
    except Exception:
        return False

def get_model_map() -> Dict[str, str]:
    """Resolve standard model names to available English or Arabic Anki models."""
    try:
        available = invoke_anki("modelNames") or []
    except Exception:
        available = []

    model_map = {"Basic": "Basic", "Cloze": "Cloze"}
    if "قالب البطاقات الأساسي" in available and "Basic" not in available:
        model_map["Basic"] = "قالب البطاقات الأساسي"
    if "قالب بطاقات النص المخفي" in available and "Cloze" not in available:
        model_map["Cloze"] = "قالب بطاقات النص المخفي"
    return model_map

def add_anki_card(
    deck_name: str,
    front: str = "",
    back: str = "",
    text: str = "",
    extra: str = "",
    model_type: str = "Basic",
    tags: Optional[List[str]] = None,
    concept_id: Optional[str] = None
) -> Dict[str, Any]:
    tags = list(tags or ["learnharness"])
    if concept_id:
        tags.append(f"concept::{concept_id}")

    models = get_model_map()
    actual_model = models.get(model_type, model_type)

    if model_type == "Cloze":
        fields = {
            "Text": text or front,
            "Extra": extra or back
        }
    else:
        fields = {
            "Front": front,
            "Back": back
        }

    # Ensure deck exists
    try:
        invoke_anki("createDeck", {"deck": deck_name})
    except Exception:
        pass

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": actual_model,
                "fields": fields,
                "tags": tags,
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "deck"
                }
            }
        }
    }
    req = urllib.request.Request(
        ANKI_CONNECT_URL,
        data=json.dumps(payload).encode("utf-8")
    )
    with urllib.request.urlopen(req, timeout=3) as resp:
        return json.loads(resp.read().decode("utf-8"))

def export_to_tsv(
    cards: List[Dict[str, Any]],
    output_path: str
) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "a", encoding="utf-8") as f:
        for c in cards:
            front = (c.get("front") or c.get("fields", {}).get("Text") or "").replace("\t", " ").replace("\n", "<br>")
            back = (c.get("back") or c.get("fields", {}).get("Extra") or "").replace("\t", " ").replace("\n", "<br>")
            tags = " ".join(c.get("tags", ["learnharness"]))
            f.write(f"{front}\t{back}\t{tags}\n")

def sync_pending_cards(
    pending_path: str = "/home/basel/Work/LearnHarness/desktop/pending_cards.json",
    default_deck: str = "تقنية::FastAPI"
) -> Dict[str, Any]:
    if not os.path.exists(pending_path):
        return {"status": "empty", "message": f"{pending_path} does not exist"}

    with open(pending_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    if not is_anki_connect_available():
        export_to_tsv(cards, "/home/basel/Work/LearnHarness/anki_cards_export.tsv")
        return {"status": "fallback_tsv", "count": len(cards)}

    synced = []
    for c in cards:
        deck = c.get("deckName") or default_deck
        model = c.get("modelName", "Cloze")
        fields = c.get("fields", {})
        res = add_anki_card(
            deck_name=deck,
            front=fields.get("Front", ""),
            back=fields.get("Back", ""),
            text=fields.get("Text", ""),
            extra=fields.get("Extra", ""),
            model_type=model,
            tags=c.get("tags"),
            concept_id=c.get("id")
        )
        synced.append({"id": c.get("id"), "res": res})

    return {"status": "synced_live", "count": len(synced), "results": synced}

if __name__ == "__main__":
    result = sync_pending_cards()
    print("Sync pending cards result:", json.dumps(result, ensure_ascii=False, indent=2))
