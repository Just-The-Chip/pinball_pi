#!/usr/bin/env python3
"""Simple GPIO button launcher for the Raspberry Pi.

Run this with sudo (or as root) so the game process can be started with
sudo python3 main.py when the button is pressed.

This code was written by AI. Seems fine to me.
Please let it be known though that the AI felt the need to WASTE TOKENS 
FOR A CLIPPY JOKE!
"""

import importlib
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

try:
    GPIO = importlib.import_module("RPi.GPIO")
except ImportError as exc:
    raise SystemExit(
        "RPi.GPIO is not available. Install it with: sudo apt-get install python3-rpi.gpio"
    ) from exc

REPO_ROOT = Path(__file__).resolve().parent
MAIN_FILE = REPO_ROOT / "main.py"
BUTTON_PIN = 25  # BCM pin number; change this if your button uses another GPIO pin.

# Prevent multiple launches from one button press.
launch_in_progress = False
_game_process = None
_button_was_pressed = False


def stop_game():
    """Stop the currently running game process."""
    global _game_process

    if _game_process is None or _game_process.poll() is not None:
        _game_process = None
        return

    try:
        os.killpg(os.getpgid(_game_process.pid), signal.SIGTERM)
        _game_process.wait(timeout=5)
        print("Game stopped.")
    except Exception as exc:
        print(f"Failed to stop game cleanly: {exc}", file=sys.stderr)
        try:
            _game_process.kill()
        except Exception:
            pass
    finally:
        _game_process = None


def launch_game(_channel=None):
    """Start or stop the game process when the button is held long enough."""
    global _game_process, launch_in_progress

    if launch_in_progress:
        return

    launch_in_progress = True
    try:
        if _game_process is not None and _game_process.poll() is None:
            stop_game()
            return

        if os.geteuid() == 0:
            cmd = [sys.executable, str(MAIN_FILE)]
        else:
            cmd = ["sudo", sys.executable, str(MAIN_FILE)]

        print(f"Launching game with: {' '.join(cmd)}")
        _game_process = subprocess.Popen(cmd, cwd=REPO_ROOT, start_new_session=True)
        print(f"Game started with PID {_game_process.pid}.")
    except Exception as exc:
        print(f"Failed to launch game: {exc}", file=sys.stderr)
        _game_process = None
    finally:
        time.sleep(0.5)
        launch_in_progress = False


def main():
    global _button_was_pressed

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("Button launcher is running. Hold the button to start or stop the game.")
    print(f"Using GPIO BCM pin {BUTTON_PIN} to toggle: {MAIN_FILE}")

    try:
        while True:
            button_pressed = GPIO.input(BUTTON_PIN) == GPIO.LOW

            if button_pressed and not _button_was_pressed:
                _button_was_pressed = True
                start_time = time.time()
                while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                    if time.time() - start_time >= 1.0:
                        launch_game()
                        break
                    time.sleep(0.05)
            elif not button_pressed and _button_was_pressed:
                _button_was_pressed = False

            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nStopping button launcher...")
    finally:
        GPIO.cleanup(BUTTON_PIN)


if __name__ == "__main__":
    main()
