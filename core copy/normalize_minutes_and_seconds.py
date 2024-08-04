def normalize_minutes_and_seconds(minutes: int, seconds: int) -> int:
    """
    Normalize minutes and seconds to be within the range [0, 3600]
    Parameters:
    minutes (int): The minutes value to be converted. 
    seconds (int): The seconds value to be converted. 

    Returns:
    int: The converted minutes and seconds value based on the range.
    """
    return (minutes * 60 + seconds) % 3600


# Example usage:
minutes = 60  # Example minutes string
seconds = 60  # Example seconds string
normalized_minutes_and_seconds = normalize_minutes_and_seconds(
    minutes, seconds)
print(f"Original minutes: {minutes}")
print(f"Original seconds: {seconds}")
print(f"Converted minutes and seconds: {normalized_minutes_and_seconds}")
