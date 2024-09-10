# User Guide for Custom Language Interpreter

This guide will help you run the interpreter for your custom language using the provided main script.

## Prerequisites

Before you begin, ensure you have Python installed on your system. The interpreter is written in Python, so you'll need Python to run it.

## Running the Interpreter

To start the interpreter:

1. Open a terminal or command prompt.
2. Navigate to the directory containing your interpreter files (`main.py` and `ProjectPartA.py`).
3. Run the following command:

```
python PartA_Main.py
```

4. You will see a menu with three options:

```
Choose an option:
1. Run automated tests
2. Enter interactive mode
3. Exit
```

### Option 1: Run Automated Tests

This option runs a series of predefined tests to check the functionality of your interpreter.

1. Select option 1 by entering '1' when prompted.
2. The script will run through a series of test cases, displaying the expression, expected result, and actual result for each test.
3. It will indicate whether each test passed or failed.

This is useful for verifying that your interpreter is working correctly after making changes.

### Option 2: Interactive Mode

In interactive mode, you can enter and execute code line by line.

1. Select option 2 by entering '2' when prompted.
2. You will see a prompt where you can start entering code:

```
Enter an expression (or type 'exit' to quit):
```

3. Enter your code at the prompt. The interpreter will execute each line as you enter it and display the result.
4. To exit the interactive mode, type `exit` and press Enter.

Example session:

```
Enter an expression (or type 'exit' to quit): 2 + 3
5

Enter an expression (or type 'exit' to quit): DEFUN add(a, b): a + b
Function 'add' defined successfully

Enter an expression (or type 'exit' to quit): add(10, 20)
30

Enter an expression (or type 'exit' to quit): exit
```

### Option 3: Exit

Select this option to quit the program.

## Language Features

Your custom language supports various features, including:

- Basic arithmetic operations: +, -, *, /, %
- Comparison operators: ==, !=, >, <, >=, <=
- Logical operators: AND, OR, NOT
- Conditional statements: IF-THEN-ELSE
- Loops: FOR
- Function definitions: DEFUN
- Lambda functions

For detailed syntax and usage of these features, refer to the test cases in the automated tests.

## Error Handling

If there are syntax errors or runtime errors in your code, the interpreter will display an error message indicating the type of error and where it occurred.

## Tips

- Use the automated tests to understand the syntax and capabilities of the language.
- In interactive mode, you can define functions and use them in subsequent lines.
- Remember that division (/) performs integer division.
- Lambda functions can be used for quick, anonymous function definitions.

For more detailed information about specific language features, review the test cases in the `run_automated_tests()` function or consult additional language documentation if available.
