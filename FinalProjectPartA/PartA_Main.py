import ProjectPartA


def run_automated_tests():
    tests = [
        ("1 + 1", 2),
        ("30 - 10", 20),
        ("(3 * 4)", 12),
        ("2 + 3 * 4", 20),
        ("2 + (3 * 4) ", 14),
        ("4 / 0", "Error - Division by Zero: Attempted to divide by zero\nFile <stdin>, line 1"),  # Changed from ** to ^ for exponentiation
        ("10 / 3", 3),  # Integer division
        ("8 % 3", 2),
        ("true OR false", True),
        ("3 > 4 OR 3 < 4", True),
        ("true AND false", False),
        ("5 > 4 AND 2 > 3", False),
        ("not false", True),
        ("3 > 4", False),
        ("5 == 5", True),
        ("5 != 5", False),
        ("5 >= 5", True),
        ("5 <= 4", False),
        ("if 1 == 1 then 3 else 4", 3),
        ("if 3 > 4 == false then 1 else 0", 1),
        ("if 5 > 3 then if 3 < 1 then 1 else 2 else 3", 2),
        ("for 1 to 5 do 3 * 4", 12),  # Will print 3 five times and return 3
        (
        "DEFUN factorial(n) : if n == 0 then 1 else n * factorial(n - 1)", "Function 'factorial' defined successfully"),
        ("factorial(5)", 120),
        ("DEFUN fibonacci(n) : if n <= 1 then n else fibonacci(n - 1) + fibonacci(n - 2)",
         "Function 'fibonacci' defined successfully"),
        ("fibonacci(7)", 13),
        ("DEFUN sum(n,m) : n + m",
         "Function 'sum' defined successfully"),
        ("sum(2,5)", 7),
        ("(lambda x, y: x + y)(3, 5)", 8),
        ("(lambda x: x + 1)(20)", 21),
        ("(lambda f: f(2))(lambda x: x + 3)", 5)

    ]

    for i, (expression, expected) in enumerate(tests, 1):
        print(f"Test {i}:")
        print(f"Expression: {expression}")
        print(f"Actual result: {expected}")

        result, error = ProjectPartA.run('<stdin>', expression)

        if error:
            print(f"Expected result: Error - {error.as_string()}")
            print("Test failed")
        else:
            print(f"Expected result: {result}")
            if result == expected:
                print("Test passed")
            else:
                print("Test failed")

        print()  # Empty line for better readability between tests


def interactive_mode():
    while True:
        text = input("Enter an expression (or type 'exit' to quit): ")

        if text.lower() == 'exit':
            break

        result, error = ProjectPartA.run('<stdin>', text)

        if error:
            print(error.as_string())
        else:
            print(result)
        print()


def main():
    while True:
        print("\nChoose an option:")
        print("1. Run automated tests")
        print("2. Enter interactive mode")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            run_automated_tests()
        elif choice == '2':
            interactive_mode()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()