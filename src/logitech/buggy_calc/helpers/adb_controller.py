from __future__ import annotations

import subprocess
from pathlib import Path

from ...logger import configure_logger

LOGGER = configure_logger("adb_controller")


class ADBController:
    """Controller class for ADB operations and device communication."""

    @staticmethod
    def execute_command(
        command: list[str], capture_output: bool = True
    ) -> subprocess.CompletedProcess:
        """
        Execute a shell command using subprocess.

        :param command: List of command arguments to execute.
        :type command: list[str]
        :param capture_output: Whether to capture the command's output. Defaults to True.
        :type capture_output: bool, optional
        :returns: The completed process object containing execution results.
        :rtype: subprocess.CompletedProcess
        :raises RuntimeError: If the command times out or fails to execute.
        """
        try:
            LOGGER.debug(f"Executing command: {command}")
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                check=True,
                timeout=30,
            )
            LOGGER.debug("Finished succesfully")
            return result
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Command timed out: {' '.join(command)}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ADB command failed: {e}")

    def launch_app(self, app_name: str, activity_name: str) -> None:
        """
        Launch an Android application by specifying its package and activity name.

        :param app_name: The package name of the application to launch.
        :type app_name: str
        :param activity_name: The name of the activity to start within the application.
        :type activity_name: str
        :returns: None
        """
        self.execute_command(
            [
                "adb",
                "shell",
                "am",
                "start",
                "-n",
                f"{app_name}/{activity_name}",
            ],
            capture_output=False,
        )

    def close_app(self, app_name: str) -> None:
        """
        Close an Android application by its package name.

        :param app_name: The package name of the application to close.
        :type app_name: str
        :returns: None
        """
        self.execute_command(
            ["adb", "shell", "am", "force-stop", app_name],
            capture_output=False,
        )

    def get_ui_dump(self) -> str:
        """
        Retrieve the current UI hierarchy dump from the connected Android device.

        :returns: The UI hierarchy XML as a string.
        :rtype: str
        :raises RuntimeError: If the ADB command fails or times out.
        """
        result = self.execute_command(
            ["adb", "exec-out", "uiautomator", "dump", "/dev/tty"]
        )
        return result.stdout

    def tap_coordinates(self, x: int, y: int) -> None:
        """
        Simulate a tap on the Android device at the specified screen coordinates.

        :param x: The x-coordinate where the tap should occur.
        :type x: int
        :param y: The y-coordinate where the tap should occur.
        :type y: int
        :returns: None
        """
        self.execute_command(
            ["adb", "shell", "input", "tap", str(x), str(y)], capture_output=False
        )

    def input_value(self, value: str | float) -> None:
        """
        Input a value (text or number) into the currently focused field on the Android device.

        :param value: The value to input.
        :type value: str | float
        :returns: None
        """
        self.execute_command(
            ["adb", "shell", "input", "text", str(value)], capture_output=False
        )

    def del_value(self) -> None:
        """
        Delete the current value in the focused input field on the Android device by simulating a delete key event.

        :returns: None
        """
        self.execute_command(
            ["adb", "shell", "input", "keyevent", "67"], capture_output=False
        )

    def take_screenshot(self, screenshot_name: str) -> None:
        """
        Captures a screenshot on the connected Android device.

        This method uses the `adb` command to take a screenshot on the connected
        Android device and saves it to the device's internal storage at the path
        `/sdcard/screenshot.png`.

        :return: None
        """
        self.execute_command(
            ["adb", "shell", "screencap", "-p", f"/sdcard/{screenshot_name}.png"],
            capture_output=False,
        )

    def pull_screenshot(self, screenshot_name: str, log_dir: Path) -> None:
        """
        Pulls a screenshot file from the connected Android device to the local machine.

        This method uses the `adb` command to transfer a screenshot file from the
        device's internal storage to a specified directory on the local machine.

        :param screenshot_name: The name of the screenshot file (without extension) to pull from the device.
        :type screenshot_name: str
        :param log_dir: The local directory where the screenshot will be saved.
        :type log_dir: pathlib.Path
        :returns: None
        """
        self.execute_command(
            [
                "adb",
                "pull",
                f"/sdcard/{screenshot_name}.png",
                f"{log_dir}/{screenshot_name}.png",
            ],
            capture_output=False,
        )

    def del_screenshot_from_device(self, screenshot_name: str) -> None:
        """
        Delete a screenshot from the connected Android device.

        :param screenshot_name: Filename **without** the ``.png`` extension.
                                The file is assumed to reside in ``/sdcard``.
        :type screenshot_name: str
        :returns: None
        """
        self.execute_command(
            ["adb", "shell", "rm", f"/sdcard/{screenshot_name}.png"],
            capture_output=False,
        )
