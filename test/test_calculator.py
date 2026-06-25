import pytest

from src import calculator


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (2, 3, 5),
        (-2, 3, 1),
        (1.5, 2.25, 3.75),
    ],
)
def test_add(left, right, expected):
    assert calculator.add(left, right) == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (5, 3, 2),
        (-2, 3, -5),
        (1.5, 0.5, 1.0),
    ],
)
def test_subtract(left, right, expected):
    assert calculator.subtract(left, right) == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (2, 3, 6),
        (-2, 3, -6),
        (1.5, 2, 3.0),
    ],
)
def test_multiply(left, right, expected):
    assert calculator.multiply(left, right) == expected


def test_divide_returns_quotient():
    assert calculator.divide(7, 2) == 3.5


def test_divide_rejects_zero_divisor():
    with pytest.raises(ValueError, match="Cannot divide by zero\\."):
        calculator.divide(7, 0)


@pytest.mark.parametrize(
    ("left", "operator", "right", "expected"),
    [
        (8, "+", 2, 10),
        (8, "-", 2, 6),
        (8, "*", 2, 16),
        (8, "/", 2, 4),
    ],
)
def test_calculate_dispatches_supported_operators(left, operator, right, expected):
    assert calculator.calculate(left, operator, right) == expected


def test_calculate_rejects_unsupported_operator():
    with pytest.raises(ValueError) as error:
        calculator.calculate(1, "%", 2)

    message = str(error.value)
    assert "Unsupported operator '%'" in message
    for operator in calculator.OPERATIONS:
        assert operator in message


def test_read_number_retries_until_float(monkeypatch, capsys):
    values = iter(["not-a-number", "3.25"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(values))

    assert calculator.read_number("Number: ") == 3.25
    assert "Please enter a valid number." in capsys.readouterr().out


def test_read_operator_retries_until_supported_operator(monkeypatch, capsys):
    values = iter(["%", " * "])
    monkeypatch.setattr("builtins.input", lambda prompt: next(values))

    assert calculator.read_operator() == "*"
    assert "Please choose one of: +, -, *, /." in capsys.readouterr().out


def test_main_prints_result_then_exits_on_eof(monkeypatch, capsys):
    values = iter(["6", "/", "2"])

    def fake_input(prompt):
        try:
            return next(values)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)

    calculator.main()

    output = capsys.readouterr().out
    assert "Simple Python Calculator" in output
    assert "Result: 3.0" in output
    assert "Goodbye." in output


def test_main_prints_calculation_errors_and_continues(monkeypatch, capsys):
    values = iter(["1", "/", "0"])

    def fake_input(prompt):
        try:
            return next(values)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)

    calculator.main()

    output = capsys.readouterr().out
    assert "Error: Cannot divide by zero." in output
    assert "Goodbye." in output
