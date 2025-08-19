from __future__ import annotations

import re

from ...logger import configure_logger
from .exceptions import InvalidAppFieldError, ResultNotFoundError

LOGGER = configure_logger("ui_parser")


class UIParser:
    """Parser class for extracting UI elements from UIAutomator XML dumps."""

    _APP_FIELDS = {
        r"=": "resultView",
        r"+": "addButton",
        r"-": "subtractButton",
        r"/": "divideButton",
        r"*": "multiplyButton",
        r"first_number": "input1",
        r"second_number": "input2",
    }

    def __init__(self, package_name: str):
        self.package_name = package_name

    def parse_element_bounds(
        self, xml_dump: str, text: str
    ) -> tuple[int, int, int, int] | None:
        """
        Parse the bounds of a UI element from a UIAutomator XML dump.

        :param xml_dump: The XML dump string obtained from the Android device UI.
        :type xml_dump: str
        :param text: The symbolic name or label of the UI element to locate (e.g., '=', '+', 'first_number').
        :type text: str
        :returns: A tuple of four integers representing the element's bounds (x1, y1, x2, y2), or None if not found.
        :rtype: tuple[int, int, int, int] | None
        :raises InvalidAppFieldError: If the provided text does not correspond to a valid app field.
        """
        if text not in self._APP_FIELDS:
            raise InvalidAppFieldError(
                f"Invalid app field: '{text}'. Valid fields are: {list(self._APP_FIELDS.keys())}"
            )
        field_name = self._APP_FIELDS[text]
        LOGGER.debug(f"Starting element parse operation for: {field_name}")
        LOGGER.debug(f"Processing XML content: {xml_dump}")
        pattern = rf'resource-id="{self.package_name}:id/{field_name}".*?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"'
        LOGGER.debug(f"Searching for pattern: '{pattern}'")

        match = re.search(pattern, xml_dump)
        if match:
            return (
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4)),
            )
        return None

    def parse_result_text(self, xml_dump: str, text: str = "=") -> str:
        """
        Parse the bounds of a UI element from a UIAutomator XML dump.

        :param xml_dump: The XML dump string obtained from the Android device UI.
        :type xml_dump: str
        :param text: The symbolic name or label of the UI element to locate (e.g., '=', '+', 'first_number').
        :type text: str
        :returns:
            A tuple of four integers representing the element's bounds (x1, y1, x2, y2), or None if not found.
        :rtype: tuple[int, int, int, int] or None
        :raises InvalidAppFieldError:
            If the provided text does not correspond to a valid app field.
        """
        if text not in self._APP_FIELDS:
            raise InvalidAppFieldError(
                f"Invalid app field: '{text}'. Valid fields are: {list(self._APP_FIELDS.keys())}"
            )
        field_name = self._APP_FIELDS[text]
        LOGGER.debug(f"Starting result parse operation for: {field_name}")
        LOGGER.debug(f"Processing XML content: {xml_dump}")
        pattern = rf'text="([^"]*)" resource-id="{self.package_name}:id/{field_name}"'
        LOGGER.debug(f"Searching for pattern: '{pattern}'")

        match = re.search(pattern, xml_dump)
        if match:
            return match.group(1)
        raise ResultNotFoundError(
            f"Result text not found for element with text '{text}'"
        )
