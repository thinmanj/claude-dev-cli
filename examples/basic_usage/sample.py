"""Sample Python module for testing Claude Dev CLI."""


def calculate_average(numbers: list) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def find_max(numbers: list) -> int:
    """Find the maximum number in a list."""
    if not numbers:
        raise ValueError("List is empty")
    
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num


class Calculator:
    """Simple calculator class."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def get_history(self) -> list:
        """Get calculation history."""
        return self.history.copy()


if __name__ == "__main__":
    # Example usage
    print(f"Average: {calculate_average([1, 2, 3, 4, 5])}")
    print(f"Max: {find_max([1, 5, 3, 9, 2])}")
    
    calc = Calculator()
    calc.add(10, 5)
    calc.subtract(20, 8)
    print(f"History: {calc.get_history()}")
