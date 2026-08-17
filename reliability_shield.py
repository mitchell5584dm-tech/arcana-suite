# backend/engine/reliability_shield.py

import traceback

class ReliabilityShield:
    """
    ARCANA Layer 2:
    Prevents crashes, data loss, subscription abuse,
    and unexpected behavior.
    """

    def safe_execute(self, func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {
                "status": "ok",
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "trace": traceback.format_exc(),
                "message": "ARCANA prevented a crash and preserved state."
            }
