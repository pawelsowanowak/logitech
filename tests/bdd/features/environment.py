from logitech.buggy_calc.pages.calculator import Calculator

PACKAGE_NAME = "com.admsqa.buggycalc"
ACTIVITY_NAME = ".MainActivity"


def before_all(context):
    """Set up test environment before all scenarios."""
    context.calculator = Calculator(PACKAGE_NAME, ACTIVITY_NAME)
    context.calculator.launch_app()


def before_scenario(context, scenario):
    """Set up before each scenario."""
    context.calculator.clear_inputs()


def after_scenario(context, scenario):
    """Save screenshot after each scenario"""
    scenario_name = "_".join(scenario.name.split(' ')).lower()
    context.calculator.save_screenshot(scenario_name)


def after_all(context):
    """Clean up after all scenarios."""
    if hasattr(context, "calculator"):
        context.calculator.close_app()
