# ARCANA OPSEC Policy

ARCANA is designed with strict OPSEC principles:

## Network Safety
- Default mode: **offline**
- Allowed modes: offline, local-only, restricted
- External calls disabled unless explicitly enabled

## Command Safety
ARCANA blocks:
- `rm -rf /`
- `curl | sh`
- Forced privileged commands

ARCANA auto-corrects:
- instal → install
- subscrption → subscription
- updte → update

## Installation Safety
ARCANA validates:
- path
- permissions
- network_mode

Invalid or unsafe configurations are rejected.

## Logging
Audit logs enabled by default:
- Stored at `audit.log`
- No external transmission
- No analytics tracking

## Privacy
ARCANA does not:
- Sell data  
- Track users  
- Store unnecessary logs  
- Use hidden fine print  

