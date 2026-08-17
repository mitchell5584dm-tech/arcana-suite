# backend/app.py
import importlib.util
import os

from pain_point_resolver import PainPointResolver
from reliability_shield import ReliabilityShield

# 'qol layer.py' has a space in the filename  Python can't import it directly
# Using importlib to load it safely
_spec = importlib.util.spec_from_file_location(
        "qol_layer",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "qol layer.py")
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
QOLLayer = _mod.QOLLayer

resolver = PainPointResolver()
shield = ReliabilityShield()
qol = QOLLayer()

def run_command(cmd):
        return shield.safe_execute(resolver.validate_command, cmd)

def install(config):
        return shield.safe_execute(resolver.safe_install, config)

def subscription(plan):
        return shield.safe_execute(resolver.subscription_clarity, plan)

def backup(data):
        return shield.safe_execute(qol.save_backup, data)
