from unittest.mock import call

import pytest

from logitech.buggy_calc.pages.calculator import Calculator


class TestCalculator:

    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        mocker.patch("time.sleep")
        self.package_name = "com.admsqa.buggycalc"
        self.activity_name = ".MainActivity"
        self.calculator = Calculator(
            package_name=self.package_name, activity_name=self.activity_name
        )

    def test_launch_app(self, mocker):
        mock_adb = mocker.Mock()
        self.calculator.adb = mock_adb

        self.calculator.launch_app()

        mock_adb.launch_app.assert_called_once_with(
            app_name=self.package_name, activity_name=self.activity_name
        )

    def test_close_app(self, mocker):
        mock_adb = mocker.Mock()
        self.calculator.adb = mock_adb

        self.calculator.close_app()

        mock_adb.close_app.assert_called_once_with(app_name=self.package_name)

    def test_tab_button(self, mocker):
        mock_adb = mocker.Mock()
        mock_adb.get_ui_dump.return_value = ""
        mock_parser = mocker.Mock()
        mock_parser.parse_element_bounds.return_value = 1, 2, 3, 4
        self.calculator.adb = mock_adb
        self.calculator.parser = mock_parser

        self.calculator.tap_button("+")

        mock_parser.parse_element_bounds.assert_called_once_with("", "+")
        mock_adb.tap_coordinates.assert_called_once_with(2, 3)

    @pytest.mark.parametrize(
        "bounds",
        [(1, 2, 3), None],
    )
    def test_tab_button__raises_ButtonNotFoundError(self, mocker, bounds):
        mock_adb = mocker.Mock()
        mock_adb.get_ui_dump.return_value = ""
        mock_parser = mocker.Mock()
        mock_parser.parse_element_bounds.return_value = bounds
        self.calculator.adb = mock_adb
        self.calculator.parser = mock_parser

        with pytest.raises(ValueError):
            self.calculator.tap_button("+")

    def test_get_display_results_default(self, mocker):
        mock_adb = mocker.Mock()
        mock_adb.get_ui_dump.return_value = ""
        mock_parsed_result = mocker.Mock()
        mock_parser = mocker.Mock()
        mock_parser.parse_result_text.return_value = mock_parsed_result
        self.calculator.adb = mock_adb
        self.calculator.parser = mock_parser

        result = self.calculator.get_display_result()

        mock_adb.get_ui_dump.assert_called_once_with()
        mock_parser.parse_result_text.assert_called_once_with("", text="=")
        assert result == mock_parsed_result

    @pytest.mark.parametrize(
        "display_result, expected_length",
        [
            ("1", 1),
            ("1.0", 3),
            ("Enter the first number", 0),
            ("Enter the second number", 0),
        ],
    )
    def test_get_input_value_len(self, display_result, expected_length, mocker):
        mock_field_name = mocker.Mock()
        mocker.patch.object(
            self.calculator, "get_display_result", return_value=display_result
        )

        result = self.calculator._get_input_value_length(mock_field_name)

        assert result == expected_length

    def test_clear_input_field__deletes_input_value(self, mocker):
        mock_field_name = mocker.Mock()
        mock_adb = mocker.Mock()
        mock_tap_button = mocker.Mock()
        self.calculator.adb = mock_adb
        self.calculator.tap_button = mock_tap_button
        mocker.patch.object(self.calculator, "_get_input_value_length", return_value=1)

        self.calculator.clear_input_field(mock_field_name)

        mock_tap_button.assert_called_once_with(button_text=mock_field_name)
        mock_adb.del_value.assert_called_once_with()

    def test_clear_inputs(self, mocker):
        mock_clear_input_field = mocker.Mock()
        self.calculator.clear_input_field = mock_clear_input_field

        self.calculator.clear_inputs()

        mock_clear_input_field.assert_has_calls(
            [call("first_number"), call("second_number")], any_order=False
        )

    def test_input_value(self, mocker):
        mock_field_name = mocker.Mock()
        mock_value = mocker.Mock()
        mock_tap_button = mocker.Mock()
        mock_adb = mocker.Mock()
        self.calculator.adb = mock_adb
        self.calculator.tap_button = mock_tap_button

        self.calculator.input_value(mock_field_name, mock_value)

        mock_tap_button.assert_called_once_with(button_text=mock_field_name)
        mock_adb.input_value.assert_called_once_with(mock_value)
