# backend/engine/pain_point_resolver.py

import re
import json

class PainPointResolver:
    """
    ARCANA Layer 1:
    Removes user pain, confusion, OPSEC mistakes, command typos,
    install errors, subscription ambiguity, and fine‑print traps.
    """

    def __init__(self):
        # Common command corrections
        self.command_aliases = {
            "instal": "install",
            "instaall": "install",
            "subscrption": "subscription",
            "subscrip": "subscription",
            "updte": "update",
            "updat": "update",
            "confige": "config",
        }

        # Dangerous patterns to block
        self.blocklist = [
            r"rm\s+-rf\s+/",          # catastrophic delete
            r"curl\s+.*\|\s+sh",      # blind pipe-to-shell
            r"sudo\s+.*--force",      # forced privileged actions
        ]

    # ---------------------------------------------------------
    # COMMAND SAFETY + AUTO‑CORRECTION
    # ---------------------------------------------------------
    def validate_command(self, raw_input: str) -> dict:
        cleaned = raw_input.strip().lower()

        # Auto-correct common mistakes
        for wrong, correct in self.command_aliases.items():
            if wrong in cleaned:
                cleaned = cleaned.replace(wrong, correct)

        # Block dangerous patterns
        for pattern in self.blocklist:
            if re.search(pattern, cleaned):
                return {
                    "status": "blocked",
                    "reason": "Command contains unsafe or destructive patterns.",
                    "input": raw_input,
                    "suggestion": None
                }

        return {
            "status": "ok",
            "input": raw_input,
            "normalized": cleaned
        }

    # ---------------------------------------------------------
    # INSTALLATION SAFETY CHECKS
    # ---------------------------------------------------------
    def safe_install(self, config: dict) -> dict:
        required_keys = ["path", "permissions", "network_mode"]

        missing = [k for k in required_keys if k not in config]
        if missing:
            return {
                "status": "error",
                "reason": f"Missing required install fields: {missing}",
                "fix": "Provide all required installation parameters."
            }

        if config["permissions"] not in ["user", "admin"]:
            return {
                "status": "error",
                "reason": "Invalid permission level.",
                "fix": "Use 'user' or 'admin'."
            }

        if config["network_mode"] not in ["offline", "local-only", "restricted"]:
            return {
                "status": "error",
                "reason": "Unsafe network mode.",
                "fix": "Use offline/local-only/restricted for OPSEC safety."
            }

        return {
            "status": "ok",
            "message": "Installation configuration validated and safe."
        }

    # ---------------------------------------------------------
    # SUBSCRIPTION CLARITY ENGINE
    # ---------------------------------------------------------
    def subscription_clarity(self, plan_id: str) -> dict:
        plans = {
            "basic": {
                "price": "$4/mo",
                "limits": "Light usage, no data retention.",
                "renewal": "Monthly, no hidden fees.",
                "fine_print": "No tracking. No upsells."
            },
            "pro": {
                "price": "$9/mo",
                "limits": "Full usage, priority processing.",
                "renewal": "Monthly, cancel anytime.",
                "fine_print": "No ads. No data selling."
            },
            "lifetime": {
                "price": "$199 one-time",
                "limits": "Unlimited usage forever.",
                "renewal": "None.",
                "fine_print": "No subscription. No renewal traps."
            }
        }

        if plan_id not in plans:
            return {
                "status": "error",
                "reason": "Unknown plan.",
                "fix": "Use basic / pro / lifetime."
            }

        return {
            "status": "ok",
            "plan": plan_id,
            "details": plans[plan_id]
        }

