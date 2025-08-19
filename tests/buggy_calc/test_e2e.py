from __future__ import annotations

import pytest

from logitech.buggy_calc.pages.calculator import Calculator

PACKAGE_NAME = "com.admsqa.buggycalc"
ACTIVITY_NAME = ".MainActivity"


@pytest.fixture(scope="session")
def calculator_app():
    calculator = Calculator(PACKAGE_NAME, ACTIVITY_NAME)
    calculator.launch_app()
    yield calculator
    calculator.close_app()


class CalculatorTestCase:
    """
    Base test case class for calculator E2E tests.

    Provides common setup/teardown and utility methods for calculator testing.
    """

    @pytest.fixture(autouse=True)
    def setUp(self, calculator_app) -> None:
        """Set up test environment before each test."""
        self.calculator = calculator_app

    def input_first_value(self, value: str) -> None:
        """
        Input a value into the first input field of the calculator.

        This method sends the provided value to the calculator's first input field.

        :param value: The value to input into the first number field.
        :type value: str
        :returns: None
        """
        self.calculator.input_value(field_name="first_number", value=value)

    def input_second_value(self, value: str) -> None:
        """
        Input a value into the second input field of the calculator.

        This method sends the provided value to the calculator's second input field.

        :param value: The value to input into the second number field.
        :type value: str
        :returns: None
        """
        self.calculator.input_value(field_name="second_number", value=value)

    def clear_inputs(self) -> None:
        """
        Clear the values in all input fields of the calculator.

        This method calls the calculator's `clear_inputs` method to remove any values
        present in the input fields, ensuring a clean state before further actions.

        :returns: None
        """
        self.calculator.clear_inputs()

    def get_display_result(self, field_name: str) -> str:
        """
        Retrieve the displayed value from the specified field in the calculator UI.

        This method calls the calculator's `get_display_result` method to obtain the current
        value shown in the given field (e.g., "first_number", "second_number", or "=").

        :param field_name: The symbolic name of the field to extract the displayed value from.
        :type value: str
        :returns: The text value currently displayed in the specified field.
        :rtype: int
        """
        return self.calculator.get_display_result(field_name)

    def perform_calculation(
        self,
        operation: str,
        input1: str | None = None,
        input2: str | None = None,
    ) -> str | None:
        """
        Perform a calculator operation with the given inputs.

        This method clears all input fields, enters the provided input values (if any),
        taps the specified operation button, and returns the displayed result.

        :param operation: The symbolic name of the operation button to tap (e.g., "+", "-", "*", "/").
        :type operation: str
        :param input1: The value to input into the first input field.
        :type input1: str or None, optional
        :param input2: The value to input into the second input field.
        :type input2: str or None, optional
        :returns: The result displayed by the calculator after performing the operation.
        :rtype: str or None
        """
        self.clear_inputs()

        if input1:
            self.input_first_value(input1)
        if input2:
            self.input_second_value(input2)
        self.calculator.tap_button(operation)

        return self.calculator.get_display_result()


class TestBasicOperations(CalculatorTestCase):
    """Test cases for basic operations."""

    def test_first_number_default_message(self):
        self.clear_inputs()
        displayed_value = self.get_display_result("first_number")
        assert displayed_value == "Enter the first number"

    def test_second_number_default_message(self):
        self.clear_inputs()
        displayed_value = self.get_display_result("second_number")
        assert displayed_value == "Enter the second number"

    @pytest.mark.parametrize(
        "input_value, expected_value",
        [
            ("-1", "-1"),
            ("0", "0"),
            ("0.0", "0.0"),
            ("999999999", "999999999"),
            ("1000000000", "1000000000"),
            ("0.0000001", "0.0000001"),
            ("-0.001", "-0.001"),
            ("00.5", "00.5"),
            ("005.00", "005.00"),
        ],
    )
    def test_first_number_receive_value(self, input_value, expected_value):
        self.clear_inputs()
        self.input_first_value(input_value)
        displayed_value = self.get_display_result("first_number")
        assert (
            displayed_value == expected_value
        ), f"Input validation failed: input '{input_value}' expected '{expected_value}' but got '{displayed_value}'"

    @pytest.mark.parametrize(
        "input_value, expected_value",
        [
            ("-1", "-1"),
            ("0", "0"),
            ("0.0", "0.0"),
            ("999999999", "999999999"),
            ("1000000000", "1000000000"),
            ("0.0000001", "0.0000001"),
            ("-0.001", "-0.001"),
            ("00.5", "00.5"),
            ("005.00", "005.00"),
        ],
    )
    def test_second_number_receive_value(self, input_value, expected_value):
        self.clear_inputs()
        self.input_second_value(input_value)
        displayed_value = self.get_display_result("second_number")
        assert (
            displayed_value == expected_value
        ), f"Input validation failed: input '{input_value}' expected '{expected_value}' but got '{displayed_value}'"


class TestMathOperations(CalculatorTestCase):

    @pytest.mark.parametrize(
        "input1, input2, expected_value",
        [
            # Basic positive addition
            ("1", "2", "3.0"),
            ("5", "3", "8.0"),
            ("10", "15", "25.0"),
            ("100", "200", "300.0"),
            # Addition with zero
            ("0", "5", "5.0"),
            ("5", "0", "5.0"),
            ("0", "0", "0.0"),
            ("-0", "5", "5.0"),
            ("5", "-0", "5.0"),
            # Negative numbers
            ("-1", "2", "1.0"),
            ("1", "-2", "-1.0"),
            ("-1", "-2", "-3.0"),
            ("-5", "5", "0.0"),
            # Decimal numbers
            ("1.5", "2.5", "4.0"),
            ("0.1", "0.2", "0.3"),
            ("3.14", "2.86", "6.0"),
            ("0.999", "0.001", "1.0"),
            # Very small decimals
            ("0.0001", "0.0002", "0.0003"),
            ("0.000000001", "0.000000002", "0.000000003"),
            # Large numbers
            ("999999", "1", "1000000.0"),
            ("123456789", "987654321", "1111111110.0"),
            ("1000000000", "1", "1000000001.0"),
            # Mixed integer and decimal
            ("5", "2.5", "7.5"),
            ("10.0", "5", "15.0"),
            ("1.", "2", "3.0"),
            # Numbers with formatting
            ("01", "02", "3.0"),  # Leading zeros
            ("1.", "2.", "3.0"),  # Trailing decimal point
            ("005.00", "002.50", "7.5"),
            # Precision cases
            ("3.14159", "2.71828", "5.85987"),
            ("0.333333", "0.666667", "1.0"),
            ("1.23456789", "2.98765432", "4.22222221"),
            # Error cases - missing inputs
            ("5", None, "Error: provide numbers"),
            (None, "3", "Error: provide numbers"),
            (None, None, "Error: provide numbers"),
            # Boundary values
            ("0.0000001", "0.9999999", "1.0"),
            ("999999999", "0.000001", "999999999.000001"),
        ],
    )
    def test_simple_addition(self, input1, input2, expected_value) -> None:
        result = self.perform_calculation(operation="+", input1=input1, input2=input2)
        assert (
            result == expected_value
        ), f"Input validation failed: input {input1} + {input2} expected '{expected_value}' but got '{result}'"

    @pytest.mark.parametrize(
        "input1, input2, expected_value",
        [
            # Basic positive subtraction
            ("5", "3", "2.0"),
            ("10", "4", "6.0"),
            ("100", "25", "75.0"),
            # Negative numbers
            ("-5", "3", "-8.0"),
            ("5", "-3", "8.0"),
            ("-5", "-3", "-2.0"),
            ("-3", "-5", "2.0"),
            # Zero operations
            ("0", "0", "0.0"),
            ("5", "0", "5.0"),
            ("0", "5", "-5.0"),
            ("-0", "0", "0.0"),
            # Decimal numbers
            ("5.5", "2.2", "3.3"),
            ("10.0", "3.5", "6.5"),
            ("1.1", "1.1", "0.0"),
            ("0.9", "0.1", "0.8"),
            ("3.14159", "2.71828", "0.42331"),
            # Very small decimals
            ("0.001", "0.0001", "0.0009"),
            ("0.000000002", "0.000000001", "0.000000001"),
            # Large numbers
            ("999999999", "1", "999999998.0"),
            ("1000000000", "999999999", "1.0"),
            ("123456789", "987654321", "-864197532.0"),
            # Mixed integer and decimal
            ("10", "2.5", "7.5"),
            ("5.0", "2", "3.0"),
            ("1.", "0.5", "0.5"),
            # Numbers with formatting
            ("01", "02", "-1.0"),  # Leading zeros
            ("1.", "2.", "-1.0"),  # Trailing decimal point
            ("005.00", "002.50", "2.5"),
            # Same numbers (should result in zero)
            ("123", "123", "0.0"),
            ("45.67", "45.67", "0.0"),
            ("-99", "-99", "0.0"),
            # Error cases - missing inputs
            ("1", None, "Error: provide numbers"),
            (None, "1", "Error: provide numbers"),
            (None, None, "Error: provide numbers"),
        ],
    )
    def test_simple_subtraction(self, input1, input2, expected_value) -> None:
        result = self.perform_calculation(operation="-", input1=input1, input2=input2)
        assert (
            result == expected_value
        ), f"Substraction failed: input '{input1}' - '{input2}' expected '{expected_value}' but got '{result}'"

    @pytest.mark.parametrize(
        "input1, input2, expected_value",
        [
            # Basic positive multiplication
            ("2", "3", "6.0"),
            ("5", "4", "20.0"),
            ("10", "10", "100.0"),
            ("7", "8", "56.0"),
            # Multiplication with zero
            ("0", "5", "0.0"),
            ("5", "0", "0.0"),
            ("0", "0", "0.0"),
            ("-0", "5", "0.0"),
            ("5", "-0", "0.0"),
            # Multiplication with one
            ("1", "5", "5.0"),
            ("5", "1", "5.0"),
            ("1", "1", "1.0"),
            ("-1", "5", "-5.0"),
            ("5", "-1", "-5.0"),
            # Negative numbers
            ("-2", "3", "-6.0"),
            ("2", "-3", "-6.0"),
            ("-2", "-3", "6.0"),
            ("-5", "-4", "20.0"),
            # Decimal numbers
            ("2.5", "4", "10.0"),
            ("3", "2.5", "7.5"),
            ("2.5", "2.5", "6.25"),
            ("0.5", "0.5", "0.25"),
            ("1.5", "2.0", "3.0"),
            # Very small decimals
            ("0.1", "0.1", "0.01"),
            ("0.01", "0.01", "0.0001"),
            ("0.001", "0.002", "0.000002"),
            ("0.0000001", "0.0000002", "0.00000000000002"),
            # Large numbers
            ("1000", "1000", "1000000.0"),
            ("999", "999", "998001.0"),
            ("123456", "2", "246912.0"),
            ("1000000", "10", "10000000.0"),
            # Mixed integer and decimal
            ("10", "2.5", "25.0"),
            ("5.0", "2", "10.0"),
            ("1.", "5", "5.0"),
            ("3", "1.5", "4.5"),
            # Numbers with formatting
            ("01", "02", "2.0"),  # Leading zeros
            ("1.", "2.", "2.0"),  # Trailing decimal point
            ("005.00", "002.00", "10.0"),
            # Precision cases
            ("3.14159", "2", "6.28318"),
            ("2.5", "3.14159", "7.853975"),
            ("0.333333", "3", "0.999999"),
            # Fractions that result in repeating decimals
            ("1.33333", "3", "3.99999"),  # Approximate 1/3 * 3
            ("0.66667", "1.5", "1.000005"),  # Approximate 2/3 * 1.5
            # Powers of 10
            ("10", "10", "100.0"),
            ("100", "10", "1000.0"),
            ("0.1", "10", "1.0"),
            ("0.01", "100", "1.0"),
            # Error cases - missing inputs
            ("1", None, "Error: provide numbers"),
            (None, "1", "Error: provide numbers"),
            (None, None, "Error: provide numbers"),
            # Edge cases with very large results
            ("999999", "999999", "999998000001.0"),
            ("1000000", "1000", "1000000000.0"),
        ],
    )
    def test_simple_multiplication(self, input1, input2, expected_value) -> None:
        result = self.perform_calculation(operation="*", input1=input1, input2=input2)
        assert (
            result == expected_value
        ), f"Multiplication failed: input '{input1}' * '{input2}' expected '{expected_value}' but got '{result}'"

    @pytest.mark.parametrize(
        "input1, input2, expected_value",
        [
            # Basic positive division
            ("6", "2", "3.0"),
            ("10", "5", "2.0"),
            ("20", "4", "5.0"),
            ("100", "10", "10.0"),
            # Division with one
            ("5", "1", "5.0"),
            ("1", "1", "1.0"),
            ("-5", "1", "-5.0"),
            ("0", "1", "0.0"),
            # Division resulting in decimals
            ("1", "2", "0.5"),
            ("3", "4", "0.75"),
            ("1", "3", "0.3333333333333333"),  # Repeating decimal
            ("2", "3", "0.6666666666666666"),  # Repeating decimal
            ("5", "8", "0.625"),
            ("7", "8", "0.875"),
            # Negative numbers
            ("-6", "2", "-3.0"),
            ("6", "-2", "-3.0"),
            ("-6", "-2", "3.0"),
            ("-10", "5", "-2.0"),
            ("10", "-5", "-2.0"),
            ("-10", "-5", "2.0"),
            # Decimal numbers
            ("5.0", "2.0", "2.5"),
            ("7.5", "2.5", "3.0"),
            ("10.5", "3.5", "3.0"),
            ("1.5", "0.5", "3.0"),
            ("0.8", "0.4", "2.0"),
            # Very small decimals
            ("0.001", "0.01", "0.1"),
            ("0.000006", "0.000002", "3.0"),
            ("0.1", "0.01", "10.0"),
            # Large numbers
            ("1000000", "1000", "1000.0"),
            ("999999999", "999999", "1000.001"),
            ("123456789", "123", "1003713.731707317"),
            # Division by larger number (result < 1)
            ("1", "10", "0.1"),
            ("5", "50", "0.1"),
            ("100", "1000", "0.1"),
            # Same numbers (should result in 1)
            ("5", "5", "1.0"),
            ("123", "123", "1.0"),
            ("0.5", "0.5", "1.0"),
            ("-7", "-7", "1.0"),
            # Numbers with formatting
            ("01", "02", "0.5"),  # Leading zeros
            ("1.", "2.", "0.5"),  # Trailing decimal point
            ("005.00", "002.50", "2.0"),
            # Precision cases
            ("1", "7", "0.142857"),  # 1/7 repeating decimal
            # Powers of 10
            ("100", "10", "10.0"),
            ("1000", "100", "10.0"),
            ("1", "10", "0.1"),
            ("1", "100", "0.01"),
            # Zero dividend
            ("0", "5", "0.0"),
            ("0", "1", "0.0"),
            ("0", "-5", "0.0"),
            ("-0", "5", "0.0"),
            # Division by zero - error cases
            ("5", "0", "Error: invalid operation"),
            ("1", "0", "Error: invalid operation"),
            ("-5", "0", "Error: invalid operation"),
            ("0", "0", "Error: invalid operation"),
            # Error cases - missing inputs
            ("1", None, "Error: provide numbers"),
            (None, "1", "Error: provide numbers"),
            (None, None, "Error: provide numbers"),
            # Very large division results
            ("999999999", "0.001", "9.99999999E11"),
            ("1000000", "0.0001", "1.0E10"),
            # Division that should yield exact results
            ("8", "2", "4.0"),
            ("27", "3", "9.0"),
            ("64", "8", "8.0"),
            # Fractions that create long decimals
            ("10", "3", "3.3333333333333333"),
            ("100", "3", "33.333333333333333"),
            ("1", "6", "0.16666666666666666"),
            ("5", "6", "0.8333333333333334"),
            # Mixed integer and decimal
            ("10", "2.5", "4.0"),
            ("7.5", "3", "2.5"),
            ("1.", "0.5", "2.0"),
            ("15", "1.5", "10.0"),
        ],
    )
    def test_simple_division(self, input1, input2, expected_value) -> None:
        result = self.perform_calculation(operation="/", input1=input1, input2=input2)
        assert (
            result == expected_value
        ), f"Division failed: input '{input1}' / '{input2}' expected '{expected_value}' but got '{result}'"
