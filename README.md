# Minecraft Server Automation

A Python-based automation tool that works alongside an existing self-hosted Minecraft server. The project launches your existing `run.bat`, monitors server activity through RCON, sends Discord notifications, and automatically shuts down the server after extended inactivity. It can also optionally shut down the host PC when both the server and computer have been idle.

---

## Features

- 🟢 Detects when the Minecraft server comes online
- 📢 Sends Discord webhook notifications for server status
- 👥 Detects player joins and leaves
- ⏱️ Tracks server idle time
- ⚠️ Announces an automatic shutdown before stopping the server
- 🔴 Gracefully stops the Minecraft server after inactivity
- 💻 Optionally shuts down the host PC if it is also idle
- 📝 Timestamped console logging
- 🚀 One-click launcher for starting both the Minecraft server and monitoring script

---

## Screenshots

> _Coming soon_

Planned screenshots include:

- Console output while monitoring the server
- Discord "Server Online" notification
- Discord "Idle Shutdown" notification
- Discord "Server Offline" notification

## Requirements

This project assumes you already have:

- A working Minecraft Java server
- A `run.bat` file that starts the server
- RCON enabled in `server.properties`
- Python 3.10 or newer

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Configuration

1. Rename:

```
config.example.py
```

to

```
config.py
```

2. Edit `config.py`:

```python
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK"
HOST = "localhost"
PASSWORD = "YOUR_RCON_PASSWORD"
```

3. Save the file.

---

## Usage

Before using this project:

1. Set up a working Minecraft Java server.
2. Ensure RCON is enabled in `server.properties`.
3. Verify that your existing `run.bat` starts the server correctly.
4. Edit `Launch Minecraft Server.bat` so that the `SERVER_PATH` variable points to your Minecraft server folder.

Run:

```text
Launch Minecraft Server.bat
```

The launcher will:

- Start your existing Minecraft server using `run.bat`
- Launch `auto_shutdown.py`
- Wait for the server to become available through RCON
- Monitor player activity
- Gracefully shut down the server after prolonged inactivity
- Optionally shut down the host PC if it is also idle

--

## How It Works

1. Launches your existing Minecraft server.
2. Waits for the server to become available through RCON.
3. Monitors player activity at regular intervals.
4. Resets the idle timer whenever players are online.
5. Warns players before an automatic shutdown.
6. Gracefully stops the server after the warning period.
7. Optionally shuts down the host PC if it has also been idle.

---

## Project Structure

```
minecraft-server-automation/
│
├── Launch Minecraft Server.bat
├── auto_shutdown.py
├── shutdown_monitor.bat
├── config.example.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Future Improvements

- Rich Discord embed notifications
- Automatic backups before shutdown
- Configurable settings through a JSON or YAML file
- Scheduled automatic server startup
- Improved detection of unexpected server crashes

---

## License

This project is licensed under the MIT License.
