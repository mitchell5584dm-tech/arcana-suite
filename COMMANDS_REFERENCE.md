markdown
# ARCANA Commands & Project Structure

## Backend Commands

### Validate Command
POST `/command`
{"cmd": "install arcana"}

Code

### Validate Installation
POST `/install`
{
"path": "/usr/local/arcana",
"permissions": "user",
"network_mode": "offline"
}

Code

### Subscription Info
GET `/subscription/{plan}`

---

## Project Structure

