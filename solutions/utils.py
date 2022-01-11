import os


def read_file(input_path: str):
    """Generic function for reading input from right path."""
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", input_path
    )
    with open(input_path) as file:
        return file.readlines()
