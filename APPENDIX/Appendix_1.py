LAST_NAME = "Ocampo"
SEED_NUM = 9
CATEGORIES = ("CURRENT", "SPEED", "TEMPERATURE", "VOLTAGE", "PRESSURE")

favorite_artist = input("Enter your favorite artist: ").strip()
artist_letters = [character.upper() for character in favorite_artist if character.isalpha()]
if not artist_letters:
	raise ValueError("Favorite artist must contain at least one letter.")

record_templates = [
	("T1", "CURRENT"),
	("T2", "SPEED"),
	("T3", "TEMPERATURE"),
	("T4", "TEMPERATURE"),
	("T5", "VOLTAGE"),
	("T1", "VOLTAGE"),
	("T2", "PRESSURE"),
]

raw_records = []
for position, (test_label, category) in enumerate(record_templates):
	character = artist_letters[position % len(artist_letters)]
	letter_position = ord(character) - ord("A") + 1
	value = SEED_NUM * 10 + letter_position + position + 1
	raw_records.append((f"{LAST_NAME}_{test_label}", category, value))

raw_records.append(raw_records[0])

unique_records = list(dict.fromkeys(raw_records))

print("=== EXERCISE 1: TEST DATA SUMMARY ===")
print(f"Total Raw Records: {len(raw_records)}")
print(f"Unique Records: {len(unique_records)}")

for category in CATEGORIES:
	values = [record[2] for record in unique_records if record[1] == category]
	count = len(values)
	average = sum(values) / count
	maximum = max(values)
	print(
		f"Category {category:<13} -> Count: {count}, "
		f"Mean: {average:.2f}, Max: {maximum}"
	)