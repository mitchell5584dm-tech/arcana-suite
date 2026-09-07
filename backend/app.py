# backend/app.py

from engine.pain_point_resolver import PainPointResolver
from engine.reliability_shield import ReliabilityShield
from engine.qol_layer import QOLLayer

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

