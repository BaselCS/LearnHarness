"""
Anki Bridge for LearnHarness:
- Direct AnkiConnect injection (if Anki is open with AnkiConnect addon)
- Fallback to TSV/APKG auto-export (if Anki is closed)
"""
import json
import os
import urllib.request
from typing import List, Dict, Any, Optional

ANKI_CONNECT_URL = "http://127.0.0.1:8765"

def is_anki_connect_available() -> bool:
    try:
        req = urllib.request.Request(
            ANKI_CONNECT_URL,
            data=json.dumps({"action": "version", "version": 6}).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=1) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("error") is None
    except Exception:
        return False

def add_anki_card(
    deck_name: str,
    front: str,
    back: str,
    tags: Optional[List[str]] = None,
    concept_id: Optional[str] = None
) -> Dict[str, Any]:
    tags = tags or ["learnharness"]
    if concept_id:
        tags.append(f"concept::{concept_id}")

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
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
    with urllib.request.urlopen(req, timeout=2) as resp:
        return json.loads(resp.read().decode("utf-8"))

def export_to_tsv(
    cards: List[Dict[str, str]],
    output_path: str
) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "a", encoding="utf-8") as f:
        for c in cards:
            front = c["front"].replace("\t", " ").replace("\n", "<br>")
            back = c["back"].replace("\t", " ").replace("\n", "<br>")
            tags = " ".join(c.get("tags", ["learnharness"]))
            f.write(f"{front}\t{back}\t{tags}\n")

def sync_cards(
    deck_name: str,
    cards: List[Dict[str, str]],
    tsv_fallback_path: str = "/home/basel/Work/LearnHarness/anki_cards_export.tsv"
) -> Dict[str, Any]:
    if is_anki_connect_available():
        results = []
        for c in cards:
            res = add_anki_card(
                deck_name=deck_name,
                front=c["front"],
                back=c["back"],
                tags=c.get("tags"),
                concept_id=c.get("concept_id")
            )
            results.append(res)
        return {"status": "synced_live", "results": results}
    else:
        export_to_tsv(cards, tsv_fallback_path)
        return {
            "status": "fallback_tsv",
            "file": tsv_fallback_path,
            "message": "Anki is not running or AnkiConnect not detected. Cards saved to TSV."
        }

if __name__ == "__main__":
    test_cards = [
        {
            "front": "What does a matrix determinant det(A) = 0 geometrically signify?",
            "back": "The linear transformation squashes space into a lower dimension (volume collapses to 0; no inverse exists).",
            "tags": ["linear-algebra", "determinant"],
            "concept_id": "linalg_det_zero"
        }
    ]
    res = sync_cards("LearnHarness::AI", test_cards)
    print("Sync Result:", res)
