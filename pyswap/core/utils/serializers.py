"""Field serializers"""
from pandas import DataFrame
import re


def serialize_table(table: DataFrame):
    table.columns = [header.upper() for header in table.columns]
    return f'{table.to_string(index=False)}\n'


def serialize_arrays(table: DataFrame):
    return f'\n{table.to_string(index=False, header=False)}\n'


def serialize_csv_table(table: DataFrame):
    table.Station = table.Station.apply(
        lambda x: f"'{x}'" if not str(x).startswith("'") else x)
    return table.to_csv(index=False)


def is_scientific_notation(s):
    """Check if a string represents a number in scientific notation."""
    # This pattern matches strings in scientific notation, e.g., '1.23e-4', '2E+2'
    pattern = r'^[+-]?(\d+(\.\d*)?|\.\d+)[eE][+-]?\d+$'
    return re.match(pattern, s) is not None


def quote_string(string):
    """Quote the string if it contains alphabetic characters or './', except for scientific notation."""
    # Convert to string to ensure compatibility with re.search
    string = str(string)

    # Check for scientific notation first
    if is_scientific_notation(string):
        return string.upper()  # Return unchanged if it's scientific notation

    # Apply original quoting logic (simplified here for demonstration)
    if re.search("[a-zA-Z/]", string):
        return f"'{string}'"
    else:
        return string
