import random

# Load a list of words from a dictionary file (assuming one word per line)
with open('words_alpha.txt', 'r') as file:
    words = [word.strip() for word in file.readlines()
             if 3 <= len(word.strip()) <= 9]

# Check if we have enough words
if len(words) < 100000:
    raise ValueError("Need at least 100,000 unique words")

# Select 100,000 unique words
selected_words = words[:100000]


def dms_to_decimal(degrees, minutes, seconds):
    """Convert DMS (Degrees, Minutes, Seconds) to decimal degrees."""
    return degrees + minutes / 60 + seconds / 3600


def coordinates_to_words(lat_d, lat_m, lat_s, lon_d, lon_m, lon_s):
    # Convert DMS to decimal
    lat = dms_to_decimal(lat_d, lat_m, lat_s)
    lon = dms_to_decimal(lon_d, lon_m, lon_s)

    # Normalize the coordinates to positive integers
    # Latitude: -90 to 90 converted to 0 to 180
    lat_index = int((lat + 90) * 3600)
    # Longitude: -180 to 180 converted to 0 to 360
    lon_index = int((lon + 180) * 3600)

    # Compute a unique index
    unique_index = lat_index * 648000 + lon_index * 1296000
    print(unique_index)

    # Map the unique index to a 3-word combination
    word1 = selected_words[unique_index % 100000]
    word2 = selected_words[(unique_index // 100000) % 100000]
    word3 = selected_words[(unique_index // 100000**2) % 100000]

    return f"{word1}-{word2}-{word3}"


def words_to_coordinates(three_word_address):
    # Split the 3-word address into individual words
    word1, word2, word3 = three_word_address.split('-')

    # Retrieve the indices of the words from the selected_words list
    index1 = selected_words.index(word1)
    index2 = selected_words.index(word2)
    index3 = selected_words.index(word3)

    print(index1, index2, index3)

    # Compute the unique index from the word indices
    unique_index = index1 + index2 * 100000 + index3 * 100000**2

    # Compute latitude and longitude indices
    lon_index = unique_index // 1296000
    lat_index = (unique_index - lon_index * 1296000) // 648000

    # Convert indices to degrees, minutes, and seconds
    lat_seconds = (lat_index % 60)
    lat_minutes = ((lat_index // 60) % 60)
    lat_degrees = (lat_index // 3600) - 90

    lon_seconds = (lon_index % 60)
    lon_minutes = ((lon_index // 60) % 60)
    lon_degrees = (lon_index // 3600) - 180

    return (lat_degrees, lat_minutes, lat_seconds), (lon_degrees, lon_minutes, lon_seconds)


# Example coordinates for Bangalore: 12°58'18.98"N, 77°35'40.44"E
lat_d, lat_m, lat_s = 12, 58, 18.98
lon_d, lon_m, lon_s = 77, 35, 40.44

# Generate a 3-word address from the coordinates
three_word_address = coordinates_to_words(
    lat_d, lat_m, lat_s, lon_d, lon_m, lon_s)
print(f"The 3-word address for the coordinates is: {three_word_address}")
# -----------------------WORKS-----------------------

# Convert the 3-word address back into latitude and longitude
latitude, longitude = words_to_coordinates(three_word_address)
print(f"Latitude: {latitude[0]}° {latitude[1]}' {latitude[2]}''")
print(f"Longitude: {longitude[0]}° {longitude[1]}' {longitude[2]}''")
# -----------------------NOT WORKING------------------------------
