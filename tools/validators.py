# =========================================================
# SHARED VALIDATION UTILITIES
# =========================================================
#
# This file contains reusable validation functions.
#
# Instead of writing the same validation logic inside every
# tool, we define common validators here and reuse them.
#
# Example:
#
# from tools.validators import (
#     validate_required_fields,
#     validate_string,
#     validate_number_range,
#     validate_enum
# )
#
# =========================================================


# =========================================================
# VALIDATE REQUIRED FIELDS
# =========================================================
#
# Checks whether all required fields exist in the input data.
#
# Example:
#
# data = {
#     "name": "Vijay",
#     "age": 35
# }
#
# required_fields = [
#     "name",
#     "age",
#     "weight"
# ]
#
# Result:
#
# {
#     "error": "Missing required fields",
#     "missing_fields": ["weight"]
# }
#
# If everything exists:
#
# None
#
# =========================================================

def validate_required_fields(data, required_fields):

    # Make sure the input itself is a dictionary.
    if not isinstance(data, dict):

        return {
            "error": "arguments must be a JSON object"
        }

    # Check every required field.
    for field in required_fields:

        if field not in data or data[field] is None:

            return {
                "error": f"Missing required field: {field}"
            }

    # None means validation passed.
    return None


# =========================================================
# VALIDATE STRING
# =========================================================
#
# Checks that a value:
#
# 1. Is a string
# 2. Is not empty
# 3. Is not only spaces
#
# Example:
#
# validate_string("", "name")
#
# Returns:
#
# {
#     "error": "name cannot be empty"
# }
#
# =========================================================

def validate_string(value, field_name):

    # Check that the value is actually a string.
    if not isinstance(value, str):

        return {
            "error": f"{field_name} must be a string"
        }


    # Remove spaces and check if anything remains.
    if not value.strip():

        return {
            "error": f"{field_name} cannot be empty"
        }


    return None


# =========================================================
# VALIDATE NUMBER RANGE
# =========================================================
#
# Checks that a value:
#
# 1. Is a number
# 2. Is not True or False
# 3. Is greater than or equal to min_value
# 4. Is less than or equal to max_value
#
# Example:
#
# validate_number_range(
#     35,
#     "age",
#     1,
#     120
# )
#
# =========================================================

def validate_number_range(
    value,
    field_name,
    min_value,
    max_value
):

    # bool is technically a subclass of int in Python.
    #
    # So:
    #
    # isinstance(True, int)
    #
    # returns True.
    #
    # We explicitly reject boolean values.
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
    ):

        return {
            "error": f"{field_name} must be a number"
        }


    # Check minimum value.
    if value < min_value:

        return {
            "error": (
                f"{field_name} must be between "
                f"{min_value} and {max_value}"
            )
        }


    # Check maximum value.
    if value > max_value:

        return {
            "error": (
                f"{field_name} must be between "
                f"{min_value} and {max_value}"
            )
        }


    return None


# =========================================================
# VALIDATE POSITIVE NUMBER
# =========================================================
#
# Checks that a value is:
#
# 1. Numeric
# 2. Not boolean
# 3. Greater than zero
#
# This is useful for values such as:
#
# weight
# calories
# distance
# duration
#
# =========================================================

def validate_positive_number(
    value,
    field_name
):

    # Check type.
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
    ):

        return {
            "error": f"{field_name} must be a number"
        }


    # Check that the value is positive.
    if value <= 0:

        return {
            "error": f"{field_name} must be greater than zero"
        }


    return None


# =========================================================
# VALIDATE ENUM
# =========================================================
#
# An enum means a field is only allowed to contain one of
# a predefined set of values.
#
# Example:
#
# validate_enum(
#     "robot",
#     "gender",
#     ["male", "female"]
# )
#
# Returns:
#
# {
#     "error": "Invalid gender",
#     "allowed": ["male", "female"]
# }
#
# =========================================================

def validate_enum(
    value,
    field_name,
    allowed_values
):

    # Check whether the provided value exists
    # in the allowed values.
    if value not in allowed_values:

        return {
            "error": f"Invalid {field_name}",
            "allowed": allowed_values
        }


    return None