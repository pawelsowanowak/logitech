from pathlib import Path

import pytest

from logitech.buggy_calc.helpers.exceptions import (
    InvalidAppFieldError,
    ResultNotFoundError,
)
from logitech.buggy_calc.helpers.parser import UIParser

XML_TEST_PATH = Path(__file__).parent / "resources" / "xml_dump.txt"


@pytest.fixture(scope="class")
def xml_test_dump():
    with open(XML_TEST_PATH, "r") as file:
        return file.read()


class TestUIParser:

    @pytest.fixture(autouse=True)
    def setup(self, xml_test_dump):
        self.parser = UIParser(package_name="com.admsqa.buggycalc")
        self.xml_test_dump = xml_test_dump

    @pytest.mark.parametrize(
        "text, expected_bounds",
        [
            (r"=", (44, 127, 1036, 303)),
            (r"+", (44, 551, 1036, 683)),
            (r"-", (44, 683, 1036, 815)),
            (r"/", (44, 815, 1036, 947)),
            (r"*", (44, 947, 1036, 1079)),
            (r"first_number", (44, 303, 1036, 427)),
            (r"second_number", (44, 427, 1036, 551)),
        ],
    )
    def test_parse_element_bounds__matches_bounds(self, text, expected_bounds):
        bound = self.parser.parse_element_bounds(xml_dump=self.xml_test_dump, text=text)
        assert bound
        assert bound == expected_bounds

    def test_parse_element_bounds__match_not(self):
        bound = self.parser.parse_element_bounds(xml_dump="", text="+")
        assert not bound

    def test_parse_element_bounds__raises_InvalidAppFieldError(self):
        with pytest.raises(InvalidAppFieldError):
            self.parser.parse_element_bounds(xml_dump="", text="^")

    @pytest.mark.parametrize(
        "text, expected_value",
        [
            (r"=", r"102.0"),
            (r"+", r"+"),
            (r"-", r"-"),
            (r"/", r"/"),
            (r"*", r"*"),
            (r"first_number", "100"),
            (r"second_number", "2"),
        ],
    )
    def test_parse_result_text__matches_result(self, text, expected_value):
        result = self.parser.parse_result_text(xml_dump=self.xml_test_dump, text=text)
        assert result == expected_value

    def test_parse_result_text__raises_ResultNotFoundError_when_not_match(self):
        with pytest.raises(ResultNotFoundError):
            self.parser.parse_result_text(xml_dump="", text="+")

    def test_parse_result_text__raises_InvalidAppFieldError(self):
        with pytest.raises(InvalidAppFieldError):
            self.parser.parse_result_text(xml_dump="", text="^")
