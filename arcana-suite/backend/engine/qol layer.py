# backend/engine/qol_layer.py

import json
import os

class QOLLayer:
    """
    ARCANA Layer 3:
    Quality-of-life features that make the program
    feel effortless and worry-free.
    """

    def save_backup(self, data: dict, path="backup.json"):
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            return {"status": "ok", "message": "Backup saved."}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def load_backup(self, path="backup.json"):
        if not os.path.exists(path):
            return {"status": "error", "reason": "Backup not found."}

        try:
            with open(path, "r") as f:
                return {"status": "ok", "data": json.load(f)}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def offline_mode(self):
        return {
            "status": "ok",
            "message": "ARCANA is running in offline mode. No external calls."
        }

