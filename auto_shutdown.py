from mcrcon import MCRcon
import time
import os
import ctypes
import requests

from config import WEBHOOK_URL, HOST, PASSWORD

# =========================
# CONFIG
# =========================


IDLE_LIMIT = 20 * 60        # 20 minutes
WARNING_TIME = 2 * 60   # 2 minutes
CHECK_INTERVAL = 15         # 15 seconds
PC_IDLE_LIMIT = 10 * 60     # 10 minutes


def get_idle_duration():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [
            ('cbSize', ctypes.c_uint),
            ('dwTime', ctypes.c_uint),
        ]

    last_input_info = LASTINPUTINFO()
    last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)

    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info))

    millis = ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime

    return millis / 1000.0

def send_discord(message):
    try:
        response = requests.post(
            WEBHOOK_URL,
            json={"content": message},
            timeout=5
        )

        if response.status_code != 204:
            log(f"Discord webhook failed: {response.status_code}", "WARNING")

    except Exception as e:
        log(f"Discord error: {e}", "ERROR")

def log(message, level="INFO"):
    print(f"[{time.strftime('%H:%M:%S')}] [{level}] {message}")

# =========================
# STATE
# =========================
idle_time = 0
previous_players = set()
server_was_online = False


log("Waiting for Minecraft server to become available...")

while True:
    try:
        with MCRcon(HOST, PASSWORD) as mcr:
            mcr.command("list")

        log("Server detected!")
        send_discord(
            "## 🟢 Minecraft Server Online\n"
            "The world is ready!\n\n"
            "Have fun! ⛏️"
        )
        server_was_online = True

        break

    except Exception:
        log("Server not ready yet. Retrying in 5 seconds...")
        time.sleep(5)

log("Monitoring started.")

# =========================
# MAIN LOOP
# =========================
while True:
    try:
        with MCRcon(HOST, PASSWORD) as mcr:
            result = mcr.command("list")

        # ---- DEBUG / STATUS ----
        log(result)


        # ========================
        # PLAYER LIST
        # ========================
        if ":" in result:
            player_text = result.split(":", 1)[1].strip()

            if player_text:
                current_players = {p.strip() for p in player_text.split(",")}
            else:
                current_players = set()
        else:
            current_players = set()

        # ========================
        # Detect Joins
        # ========================
        joined = current_players - previous_players

        if joined:
            for player in joined:
                log(f"{player} joined the server.")

            player_list = "\n".join(f"- **{player}**" for player in sorted(joined))

            send_discord(
                "## 👋 Welcome!\n"
                "The following player(s) joined the server:\n\n"
                f"{player_list}\n\n"
                "Have fun! ⛏️"
            )

        # ========================
        # Detect Leaves
        # ========================
        left = previous_players - current_players

        if left:
            for player in left:
                log(f"{player} left the server.")

            player_list = "\n".join(f"- **{player}**" for player in sorted(left))

            send_discord(
                "## 🌙 Session Update\n"
                "The following player(s) left the server:\n\n"
                f"{player_list}\n\n"
                "See you next time! 👋"
            )

        previous_players = current_players

        # =========================
        # IDLE TIMER
        # =========================
        if not current_players:
            idle_time += CHECK_INTERVAL
            log(f"Server empty for {idle_time // 60} minutes ({idle_time} seconds)")
        else:
            if idle_time != 0:
                log("Players detected -> idle timer reset")
            idle_time = 0

        log(f"Idle timer: {idle_time} seconds")

        # =========================
        # SHUTDOWN CONDITION
        # =========================
        if idle_time >= IDLE_LIMIT:
            log("Idle timeout reached. Shutting down server...", "WARNING")

            with MCRcon(HOST, PASSWORD) as mcr:
                mcr.command("say Server is shutting down due to inactivity in 2 minutes.")


            send_discord(
                "## 🌙 Idle Shutdown\n"
                "No players have been online for **20 minutes**.\n\n"
                "The server will shut down in **2 minutes**."
            )

            time.sleep(WARNING_TIME)

            with MCRcon(HOST, PASSWORD) as mcr:
                mcr.command("stop")

            send_discord(
                "## 🔴 Minecraft Server Offline\n"
                "The world has gone to sleep.\n\n"
                "See you next session! 🌙"
            )

            log("Waiting for server to stop...")
            time.sleep(15)

            pc_idle = get_idle_duration()

            log(f"PC idle for {pc_idle / 60:.1f} minutes")

            if pc_idle >= PC_IDLE_LIMIT:
                log("PC idle timeout reached. Shutting down PC...", "WARNING")
                os.system("shutdown /s /t 0")
            else:
                log("PC is not idle. Aborting shutdown.")

            break

        time.sleep(CHECK_INTERVAL)


    except Exception as e:
        log(f"{e}", "ERROR")
        log("Entered exception block", "WARNING")
        log(f"server_was_online = {server_was_online}")

        if server_was_online:
            log("Sending offline notification...", "WARNING")
            send_discord(
                "## 🔴 Minecraft Server Offline\n"
                "The world has gone to sleep.\n\n"
                "See you next session! 🌙"
            )
            log("Server went offline.", "WARNING")
            server_was_online = False

        time.sleep(CHECK_INTERVAL)