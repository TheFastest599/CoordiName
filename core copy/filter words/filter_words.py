import json

words = []
words_180 = []
words_360 = []
# Load a list of words from a dictionary file (assuming one word per line)
with open('3600.txt', 'r') as file:
    words = [word.strip().lower() for word in file.readlines()
             if len(word.strip()) >= 3]
with open('180.txt', 'r') as file:
    words_180 = [word.strip().lower() for word in file.readlines()
                 if len(word.strip()) >= 3]
with open('360.txt', 'r') as file:
    words_360 = [word.strip().lower() for word in file.readlines()
                 if len(word.strip()) >= 3]


print("3600 180 360 : ", len(words), len(words_180), len(words_360))
filtered_words_3600 = sorted(list(set(words)))[:3600]
filtered_words_180 = sorted(list(set(words_180)))[:181]
filtered_words_360 = sorted(list(set(words_360)))[:360]
print("3600 180 360 : ", len(filtered_words_3600), len(
    filtered_words_180), len(filtered_words_360))
print('-----------------------------------------')
final_words = {
    "words_180": filtered_words_180,
    "words_360": filtered_words_360,
    "words_3600": filtered_words_3600,
    "dict_words_to_number_180": {
        y: x for x, y in enumerate(filtered_words_180)
    },
    "dict_words_to_number_360": {
        y: x for x, y in enumerate(filtered_words_360)
    },
    "dict_words_to_number_3600": {
        y: x for x, y in enumerate(filtered_words_3600)
    },
    "dict_number_to_words_180": {
        x: y for x, y in enumerate(filtered_words_180)
    },
    "dict_number_to_words_360": {
        x: y for x, y in enumerate(filtered_words_360)
    },
    "dict_number_to_words_3600": {
        x: y for x, y in enumerate(filtered_words_3600)
    }
}
with open("CoordiName_database.json", "w") as outfile:
    json.dump(final_words, outfile)

# final_dict = {
#     "dict_180": {
#         y: x for x, y in enumerate(filtered_words_180)
#     },
#     "dict_360": {
#         y: x for x, y in enumerate(filtered_words_360)
#     },
#     "dict_3600": {
#         y: x for x, y in enumerate(filtered_words_3600)
#     }
# }

# print(final_dict)


# -----------------------NOT WORKING------------------------------
