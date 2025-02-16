from typing import Dict, Optional, Tuple


class FloatRange:
    def __init__(self, start: float, end: float, start_inclusive: bool = True, end_inclusive: bool = False):
        """
        Initialize the DecimalRange.

        :param start: The lower bound of the range (inclusive).
        :param end: The upper bound of the range (exclusive).
        :param start_inclusive: Whether the start of the range is inclusive.
        :param end_inclusive: Whether the end of the range is inclusive.
        """
        if start > end:
            raise ValueError("Start of range must be less than end of range.")
        self.start = start
        self.end = end
        self.start_inclusive = start_inclusive
        self.end_inclusive = end_inclusive

    def contains(self, value: float) -> bool:
        """
        Check if a value falls within the range.

        :param value: The value to check.
        :return: True if the value is within [start, end), False otherwise.
        """
        if self.start_inclusive and self.start == value or self.end_inclusive and self.end == value:
            return True
        else:
            return self.start < value < self.end

    def __repr__(self) -> str:
        """
        String representation of the range.

        :return: A string in the format [start, end).
        """
        prefix = "[" if self.start_inclusive else "("
        suffix = "]" if self.end_inclusive else ")"
        return f"{prefix}{self.start} - {self.end}{suffix}"

    def __eq__(self, other) -> bool:
        """
        Equality check for FloatRange instances.
        """
        if not isinstance(other, FloatRange):
            return False
        return (self.start == other.start and
                self.end == other.end and
                self.start_inclusive == other.start_inclusive and
                self.end_inclusive == other.end_inclusive)

    def __hash__(self) -> int:
        """
        Generate a hash for the FloatRange instance.
        Combines the range properties into a unique hash.
        """
        return hash((self.start, self.end, self.start_inclusive, self.end_inclusive))

def generate_buy_ranges(input_dict):
    """
    Generates buy ranges based on the input dictionary of risk levels and associated values.

    This function constructs ranges from sorted keys of the input dictionary where the
    keys represent risk levels (e.g., "key_1.0", "key_2.5") and their values indicate
    a numerical value corresponding to each risk level. The ranges are mapped to their
    respective values if the numerical value is greater than zero. The result is a dictionary
    that maps floating-point intervals (instances of FloatRange) to their associated values.
    If subsequent keys have the same value, they are grouped into a continuous range.

    :param input_dict: Dictionary where keys are strings including risk level information
        (e.g., "key_<risk_level>") and values are strings representing numeric values.
    :type input_dict: dict[str, str]

    :return: A dictionary where keys are FloatRange objects representing intervals of
        risk levels and values are the corresponding numerical values from the input.
        Each interval is inclusive or exclusive based on changes in values.
    :rtype: dict[FloatRange, float]
    """
    ranges = {}

    relevant_keys = [key for key, value in input_dict.items() if value.isnumeric()]
    sorted_keys = sorted(relevant_keys, key=lambda x: float(x.split('_')[1]), reverse=True)

    end_point = None
    end_value = None
    end_inclusive = False

    for index, key in enumerate(sorted_keys):
        # Parse risk level and value
        risk_level = float(key.split('_')[1])
        value = float(input_dict[key])
        if value > 0.:
            if end_point is None:
                end_point = risk_level
                end_value = value
                end_inclusive = True
            elif value != end_value:
                ranges[FloatRange(risk_level, end_point, end_inclusive=end_inclusive)] = end_value
                end_point = risk_level
                end_value = value
                end_inclusive = False
            elif index == len(sorted_keys) - 1:
                ranges[FloatRange(risk_level, end_point, end_inclusive=end_inclusive)] = end_value
    return ranges


def generate_sell_ranges(input_dict):
    """
    Generates a dictionary of sell ranges mapped to corresponding values by parsing
    and processing the numeric sections of the input dictionary keys. The ranges
    are constructed based on the numeric values extracted from the keys, while the
    mapping retains the relationship between ranges and values from the input.

    :param input_dict: Dictionary with keys in the format of "string_numeric" and
        numeric values as strings.
    :type input_dict: dict(str, str)

    :return: A dictionary where keys are FloatRange objects representing specific
        ranges of risk levels, and values are float values derived from the
        input dictionary.
    :rtype: dict(FloatRange, float)
    """
    ranges = {}
    relevant_keys = [key for key, value in input_dict.items() if value.isnumeric()]
    sorted_keys = sorted(relevant_keys, key=lambda x: float(x.split('_')[1]))

    start_point = None
    start_value = None

    for key in sorted_keys:
        # Parse risk level and value
        risk_level = float(key.split('_')[1])
        value = float(input_dict[key])
        if start_point is None:
            start_point = risk_level
            start_value = value
        else:
            ranges[FloatRange(start_point, risk_level)] = start_value
            start_point = risk_level
            start_value = value
    if start_point is not None:
        ranges[FloatRange(start_point, 100.0, end_inclusive=True)] = start_value

    return ranges

def find_range_item(value: float, ranges: Dict[FloatRange, float]) -> Optional[Tuple[FloatRange, float]]:
    """
    Get the float value associated with the range that contains the given value.

    :param value: Float value to check against the ranges.
    :param ranges: Dictionary mapping FloatRange instances to float values.
    :return: The float value for the range that contains value, or 0 if none.
    """
    for range_obj, range_value in ranges.items():
        if range_obj.contains(value):
            return range_obj, range_value
    return None
