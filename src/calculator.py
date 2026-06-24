"""A simple command-line calculator."""


def add(left, right):
    return left + right


def subtract(left, right):
    return left - right


def multiply(left, right):
    return left * right


def divide(left, right):
    if right == 0:
        raise ValueError("Cannot divide by zero.")
    return left / right


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(left, operator, right):
    if operator not in OPERATIONS:
        valid = ", ".join(OPERATIONS)
        raise ValueError(f"Unsupported operator '{operator}'. Use one of: {valid}.")
    return OPERATIONS[operator](left, right)


def read_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def read_operator():
    while True:
        operator = input("Choose an operator (+, -, *, /): ").strip()
        if operator in OPERATIONS:
            return operator
        print("Please choose one of: +, -, *, /.")


def main():
    print("Simple Python Calculator")
    print("Press Ctrl+C to exit.")

    while True:
        try:
            left = read_number("First number: ")
            operator = read_operator()
            right = read_number("Second number: ")
            result = calculate(left, operator, right)
            print(f"Result: {result}\n")
        except ValueError as error:
            print(f"Error: {error}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()
