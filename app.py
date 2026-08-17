# backend/app.py

from pain_point_resolver import PainPointResolver
from triage import Triage
from opsec import OpsecValidator
from auditors import Auditors
from override_panel import OverridePanel


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

