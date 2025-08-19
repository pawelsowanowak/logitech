Feature: Calculator regression tests
    Basic functionality checks after builds
    Ensure new changes don't break existing features

    Background:
        Given the calculator app is launched
        And all input fields are cleared

    Scenario: Default messages are displayed
        When I view the first number field
        Then I should see "Enter the first number"
        When I view the second number field  
        Then I should see "Enter the second number"

    Scenario Outline: Input validation for first number
        When I enter "<input_value>" in the first number field
        Then the first number field should display "<expected_value>"

        Examples:
            | input_value | expected_value |
            | -1          | -1             |
            | 0           | 0              |
            | 0.0         | 0.0            |
            | 999999999   | 999999999      |
            | 0.0000001   | 0.0000001      |
            | -0.001      | -0.001         |
            | 00.5        | 00.5           |
            | 005.00      | 005.00         |

    Scenario Outline: Input validation for second number
        When I enter "<input_value>" in the second number field
        Then the second number field should display "<expected_value>"

        Examples:
            | input_value | expected_value |
            | -1          | -1             |
            | 0           | 0              |
            | 0.0         | 0.0            |
            | 999999999   | 999999999      |
            | 0.0000001   | 0.0000001      |
            | -0.001      | -0.001         |
            | 00.5        | 00.5           |
            | 005.00      | 005.00         |

    Scenario Outline: Missing first number input validation in operation
        When I enter "<first_number>" in the first number field
        And I tap the <operation> button
        Then the result should be "<expected_result>"

        Examples:
            | first_number | operation      | expected_result          |
            | 1            | addition       | "Error: provide numbers" |
            | 1            | subtraction    | "Error: provide numbers" |
            | 1            | multiplication | "Error: provide numbers" |
            | 1            | division       | "Error: provide numbers" |

    Scenario Outline: Missing second number input validation in operation
        When I enter "<second_number>" in the first number field
        And I tap the <operation> button
        Then the result should be "<expected_result>"

        Examples:
            | second_number | operation     | expected_result          |
            | 1            | addition       | "Error: provide numbers" |
            | 1            | subtraction    | "Error: provide numbers" |
            | 1            | multiplication | "Error: provide numbers" |
            | 1            | division       | "Error: provide numbers" |

    Scenario Outline: Addition operations
        When I enter "<first_number>" in the first number field
        And I enter "<second_number>" in the second number field
        And I tap the addition button
        Then the result should be "<expected_result>"

        Examples:
            | first_number | second_number | expected_result |
            | 1            | 2             | 3.0             |
            | 10.          | 15            | 25.0            |
            | 0            | 5.            | 5.0             |
            | -1           | 2             | 1.0             |
            | 1.5          | 2.5           | 4.0             |
            | 999999999    | 999999999     | 1999999998.0    |

    Scenario Outline: Subtraction operations
        When I enter "<first_number>" in the first number field
        And I enter "<second_number>" in the second number field
        And I tap the subtraction button
        Then the result should be "<expected_result>"

        Examples:
            | first_number | second_number | expected_result |
            | 5            | 3             | 2.0             |
            | 3            | 5             | -2.0            |
            | 10           | 4             | 6.0             |
            | 0            | 5             | -5.0            |

    Scenario Outline: Division operations
        When I enter "<first_number>" in the first number field
        And I enter "<second_number>" in the second number field
        And I tap the subtraction button
        Then the result should be "<expected_result>"

        Examples:
            | first_number | second_number | expected_result |
            | 5            | 3             | 2.0             |
            | 3            | 5             | -2.0            |
            | 10           | 4             | 6.0             |
            | 0            | 5             | -5.0            |
            | 1.5          | 2.5           | 4.0             |

    Scenario Outline: Division by zero handling
        When I enter "<first_number>" in the first number field
        And I enter "<second_number>" in the second number field
        And I tap the division button
        Then the result should be "<expected_result>"

        Examples:
            | first_number | second_number | expected_result          |
            | 1            | 0             | Error: invalid operation |
            | 0            | 0             | Error: invalid operation |
