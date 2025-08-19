from behave import given, then, when


@given("the calculator app is launched")
def step_calculator_launched(context):
    """Verify calculator app is launched."""
    # App is already launched in environment.py
    pass


@given("all input fields are cleared")
def step_clear_inputs(context):
    """Clear all input fields."""
    context.calculator.clear_inputs()


@when("I view the {field_name} field")
def step_view_field(context, field_name):
    """View a specific field."""
    field_mapping = {"first number": "first_number", "second number": "second_number"}
    context.current_field = field_mapping[field_name]


@when('I enter "{value}" in the first number field')
def step_enter_first_number(context, value):
    """Enter value in first number field."""
    context.calculator.input_value(field_name="first_number", value=value)


@when('I enter "{value}" in the second number field')
def step_enter_second_number(context, value):
    """Enter value in second number field."""
    context.calculator.input_value(field_name="second_number", value=value)


@when("I tap the addition button")
def step_tap_addition(context):
    """Tap the addition button."""
    context.calculator.tap_button("+")


@when("I tap the subtraction button")
def step_tap_subtraction(context):
    """Tap the subtraction button."""
    context.calculator.tap_button("-")


@when("I tap the multiplication button")
def step_tap_multiplication(context):
    """Tap the multiplication button."""
    context.calculator.tap_button("*")


@when("I tap the division button")
def step_tap_division(context):
    """Tap the division button."""
    context.calculator.tap_button("/")


@when('I perform the operation "{first}" "{operation}" "{second}"')
def step_perform_operation(context, operation, first, second):
    """Perform a complete calculation operation."""
    context.calculator.clear_inputs()

    if first != "None":
        context.calculator.input_value(field_name="first_number", value=first)

    if second != "None":
        context.calculator.input_value(field_name="second_number", value=second)

    context.calculator.tap_button(operation)


@then('I should see "{expected_text}"')
def step_verify_field_text(context, expected_text):
    """Verify text in current field."""
    actual_text = context.calculator.get_display_result(context.current_field)
    assert (
        actual_text == expected_text
    ), f"Expected '{expected_text}' but got '{actual_text}'"


@then('the first number field should display "{expected_value}"')
def step_verify_first_number_display(context, expected_value):
    """Verify first number field displays expected value."""
    actual_value = context.calculator.get_display_result("first_number")
    assert (
        actual_value == expected_value
    ), f"First number field expected '{expected_value}' but got '{actual_value}'"


@then('the second number field should display "{expected_value}"')
def step_verify_second_number_display(context, expected_value):
    """Verify second number field displays expected value."""
    actual_value = context.calculator.get_display_result("second_number")
    assert (
        actual_value == expected_value
    ), f"Second number field expected '{expected_value}' but got '{actual_value}'"


@then('the result should be "{expected_result}"')
def step_verify_result(context, expected_result):
    """Verify calculation result."""
    actual_result = context.calculator.get_display_result()
    assert (
        actual_result == expected_result
    ), f"Expected result '{expected_result}' but got '{actual_result}'"
