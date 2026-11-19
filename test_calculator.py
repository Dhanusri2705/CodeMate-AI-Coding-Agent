"""Tests for the calculator module."""

import calculator

def test_calculator():
    print("Running calculator tests...")
    
    # 1. Addition
    res_add = calculator.add(10, 5)
    print(f"10 + 5 = {res_add}")
    assert res_add == 15

    # 2. Subtraction
    res_sub = calculator.subtract(10, 5)
    print(f"10 - 5 = {res_sub}")
    assert res_sub == 5

    # 3. Multiplication
    res_mul = calculator.multiply(10, 5)
    print(f"10 * 5 = {res_mul}")
    assert res_mul == 50

    # 4. Division
    res_div = calculator.divide(10, 5)
    print(f"10 / 5 = {res_div}")
    assert res_div == 2.0

    # 5. Division by zero handling (ensures test fails if ValueError is not raised)
    division_by_zero_raised = False
    try:
        calculator.divide(10, 0)
    except ValueError as e:
        division_by_zero_raised = True
        print(f"Division by zero caught successfully: {e}")
    
    assert division_by_zero_raised, "Expected ValueError when dividing by zero, but none was raised."

    print("All tests passed successfully!")

if __name__ == "__main__":
    test_calculator()
