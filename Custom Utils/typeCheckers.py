device_models = [
    "iPad11,1", "iPad11,2", "iPad11,3", "iPad11,4", "iPad11,6", "iPad11,7",
    "iPad12,1", "iPad12,2", "iPad13,1", "iPad13,10", "iPad13,11", "iPad13,16", "iPad13,17",
    "iPad13,18", "iPad13,19", "iPad13,2", "iPad13,4", "iPad13,5", "iPad13,6", "iPad13,7",
    "iPad13,8", "iPad13,9", "iPad14,1", "iPad14,2", "iPad14,3", "iPad14,4", "iPad14,5",
    "iPad14,6", "iPad7,11", "iPad7,12", "iPad7,5", "iPad7,6", "iPad8,1", "iPad8,10",
    "iPad8,11", "iPad8,12", "iPad8,2", "iPad8,3", "iPad8,4", "iPad8,5", "iPad8,6",
    "iPad8,7", "iPad8,8", "iPad8,9", "iPhone10,1", "iPhone10,2", "iPhone10,3",
    "iPhone10,4", "iPhone10,5", "iPhone10,6", "iPhone11,2", "iPhone11,4", "iPhone11,6",
    "iPhone11,8", "iPhone12,1", "iPhone12,3", "iPhone12,5", "iPhone12,8", "iPhone13,1",
    "iPhone13,2", "iPhone13,3", "iPhone13,4", "iPhone14,2", "iPhone14,3", "iPhone14,4",
    "iPhone14,5", "iPhone14,6", "iPhone14,7", "iPhone14,8", "iPhone15,2", "iPhone15,3",
    "iPhone15,4", "iPhone15,5", "iPhone16,1", "iPhone16,2", "iPhone8,1", "iPhone8,4",
    "iPod9,1"
]


def can_be_float(input_to_check: str) -> bool:
    """
    Checks if the input string can be converted to a float.
    :param input_to_check: string
    :return: true if it can be converted, false otherwise
    """
    try:
        float(input_to_check)
        return True
    except TypeError:
        return False


def can_be_int(input_to_check: str) -> bool:
    """
    Checks if the input string can be converted to an integer.
    :param input_to_check: string
    :return: true if it can be converted, false otherwise
    """
    try:
        int(input_to_check)
        if len(str(int(input_to_check))) != len(input_to_check):
            print("Your input was not a whole number. You will loose precision by converting to an int.")
        return True
    except TypeError:
        return False


def is_valid_model(input_to_check: str) -> bool:
    """
    Checks if the input string is a valid iOS device model identifier
    :param input_to_check: stirng
    :return: true if it is a valid iOS device model identifier, false otherwise
    """
    return input_to_check in device_models
