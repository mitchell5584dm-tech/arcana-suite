# backend/config.py
"""
ARCANA Configuration File
Centralized settings for OPSEC, installation, subscription,
and environment behavior. Designed to be simple, predictable,
and worry-free for both developers and users.
"""

import os

class Config:
    # ---------------------------------------------------------
    # BASIC APP SETTINGS
    # ---------------------------------------------------------
    APP_NAME = "ARCANA Suite"
    VERSION = "1.0.0"
    DEBUG = False  # Set True only during development

    # ---------------------------------------------------------
    # OPSEC & SECURITY SETTINGS
    # ---------------------------------------------------------
    SAFE_NETWORK_MODES = ["offline", "local-only", "restricted"]
    DEFAULT_NETWORK_MODE = "offline"

    # Prevent accidental exposure
    ALLOW_EXTERNAL_CALLS = False

    # Logging behavior
    ENABLE_AUDIT_LOGS = True
    AUDIT_LOG_PATH = os.path.join(os.getcwd(), "audit.log")

    # ---------------------------------------------------------
    # INSTALLATION SETTINGS
    # ---------------------------------------------------------
    DEFAULT_INSTALL_PATH = "/usr/local/arcana"
    DEFAULT_PER
