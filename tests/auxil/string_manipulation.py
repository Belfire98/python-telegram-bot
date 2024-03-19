import re

def to_camel_case(snake_str: str) -> str:
    """Convert a snake_case string to camelCase.

    Examples:
        to_camel_case('hello_world') -> 'helloWorld'
        to_camel_case('HELLO_WORLD') -> 'helloWorld'
        to_camel_case('some-mixed_string') -> 'someMixedString'
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def to_snake_case(camel_str: str) -> str:
    """Convert a camelCase string to snake_case.

    Examples:
        to_snake_case('helloWorld') -> 'hello_world'
        to_snake_case('HELLO_WORLD') -> 'hello_world'
        to_snake_case('someMixedString') -> 'some_mixed_string'
    """
    # Convert camelCase to snake_case
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
    # Convert any remaining uppercase letters to lowercase
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()
    return name


# Error handling for invalid input strings
def convert_case(value: str, case_func: callable) -> str:
    try:
        return case_func(value)
    except ValueError as e:
        raise ValueError(f"Invalid input string: {value}") from e



