from __future__ import annotations

import re
import time
from pathlib import Path

from ...logger import configure_logger
from ..helpers.adb_controller import ADBController
from ..helpers.parser import UIParser

LOGGER = configure_logger("calculator")


class Calculator:
    """
    Page Object Model class for calculator app UI interactions.

    This class encapsulates all UI operations for the calculator app,
    following the Page Object Model design pattern for maintainable test code.
    """

    def __init__(self, package_name: str, activity_name: str) -> None:
        """
        Initialize the Calculator page object.

        :param package_name: The package name of the calculator application.
        :type package_name: str
        :param activity_name: The activity name of the calculator application.
        :type activity_name: str
        """
        self.package_name = package_name
        self.activity_name = activity_name
        self.adb = ADBController()
        self.parser = UIParser(package_name)

    def launch_app(self) -> None:
        """
        Launch the calculator application on the connected Android device.

        This method starts the calculator app using its package and activity name,
        then waits briefly to ensure the app is fully loaded before further interactions.

        :returns: None
        """
        LOGGER.debug(f"Launching app: {self.package_name}")
        self.adb.launch_app(
            app_name=self.package_name, activity_name=self.activity_name
        )

        # Wait for app to fully load

        time.sleep(2)

    def close_app(self) -> None:
        """
        Close the calculator application on the connected Android device.

        This method stops the calculator app using its package name.

        :returns: None
        """
        LOGGER.debug(f"Closing app: {self.package_name}")
        self.adb.close_app(app_name=self.package_name)

    def tap_button(self, button_text: str) -> None:
        """
        Tap a calculator button identified by its text.

        This method locates the button in the UI using its text label, calculates its center coordinates,
        and simulates a tap action at that location on the connected Android device.

        :param button_text: The text displayed on the button to tap (e.g., "+", "-", "first_number").
        :type button_text: str
        :raises ValueError:
            If the button is not found in the UI.
        :returns: None
        """
        LOGGER.debug(f"Taping button: {button_text}")
        ui_dump = self.adb.get_ui_dump()
        bounds = self.parser.parse_element_bounds(ui_dump, button_text)
        LOGGER.debug(f"Button bounds: {bounds}")

        if not bounds or len(bounds) != 4:
            raise ValueError(f"Button '{button_text}' not found in UI")
        left, top, right, bottom = bounds
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        LOGGER.debug(f"Tapping in: x={center_x}, y={center_y}")
        self.adb.tap_coordinates(center_x, center_y)

        # Small delay to allow UI to respond

        time.sleep(0.5)

    def get_display_result(self, field_name: str = "=") -> str:
        """
        Retrieve the displayed result or value from the calculator UI.

        :param field_name: The symbolic name of the field to extract the result from (default is "=").
        :type field_name: str, optional
        :returns: The text value currently displayed in the specified field.
        :rtype: str
        """
        LOGGER.debug(f"Getting display value for '{field_name}'")
        ui_dump = self.adb.get_ui_dump()
        return self.parser.parse_result_text(ui_dump, text=field_name)

    def _get_input_value_length(self, field_name: str) -> int:
        """
        Get the length of the input value for a given field.

        This method retrieves the current value displayed in the specified input field.
        If the field contains a placeholder prompt (e.g., "Enter the first number"),
        it returns 0. Otherwise, it returns the length of the field's value.

        :param field_name: The symbolic name of the input field to check.
        :type field_name: str
        :returns: The length of the current value in the input field, or 0 if the field is empty or shows a prompt.
        :rtype: int
        """
        field_value = self.get_display_result(field_name)

        if re.match(r"Enter the (first|second) number", field_value):
            return 0
        return len(field_value)

    def clear_input_field(self, field_name: str) -> None:
        """
        Clear the value in the specified input field.

        This method checks the current value length of the input field. If the field is not empty,
        it taps the field to focus it and simulates delete key events to remove all characters.

        :param field_name: The symbolic name of the input field to clear.
        :type field_name: str
        :returns: None
        """
        LOGGER.debug(f"Clearing input from '{field_name}' field")
        field_value_len = self._get_input_value_length(field_name)

        if field_value_len:
            self.tap_button(button_text=field_name)

            for _ in range(field_value_len):
                self.adb.del_value()

    def clear_inputs(self):
        """
        Clear the values in all input fields of the calculator.

        This method iterates over all input fields (e.g., "first_number", "second_number")
        and clears their contents by calling :meth:`clear_input_field` for each.

        :returns: None
        """
        LOGGER.debug("Clearing input fields")
        for input in ("first_number", "second_number"):
            self.clear_input_field(input)

    def input_value(self, field_name: str, value: str | float) -> None:
        """
        Input a value into the specified calculator input field.

        This method taps the input field to focus it and then sends the provided value
        to the field using ADB input commands.

        :param field_name: The symbolic name of the input field to receive the value.
        :type field_name: str
        :param value: The value to input into the field.
        :type value: str or float
        :returns: None
        """
        LOGGER.debug(f"Input value '{value}' to '{field_name}' field")
        self.tap_button(button_text=field_name)
        self.adb.input_value(value)

    def save_screenshot(self, screenshot_name: str) -> None:
        main_project_path = Path(__file__).parents[4].resolve()
        log_dir = main_project_path / "logs" / "screenshots"
        log_dir.mkdir(parents=True, exist_ok=True)

        LOGGER.debug("Taking screenshot...")
        self.adb.take_screenshot(screenshot_name)

        LOGGER.debug(f"Pulling {screenshot_name}.png from device...")
        self.adb.pull_screenshot(screenshot_name, log_dir)

        LOGGER.debug(f"Removing {screenshot_name}.png from device...")
        self.adb.del_screenshot_from_device(screenshot_name)

        LOGGER.debug(f"Screenshot '{screenshot_name}.png' saved to: {log_dir}")
