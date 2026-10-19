from collections import Counter, defaultdict


LAST_NAME = "Ocampo"
SEED_NUM = 9
SUBJECTS = (
	"PROGRAMMING",
	"MATHEMATICS",
	"ELECTRONICS",
	"PHYSICS",
	"ENGLISH",
)
STUDENT_LABELS = tuple(f"Student_{number}" for number in range(1, 6))


def performance_category(score):
	if score >= 90:
		return "EXCELLENT"
	if score >= 80:
		return "GOOD"
	if score >= 70:
		return "SATISFACTORY"
	if score >= 60:
		return "NEEDS IMPROVEMENT"
	return "AT RISK"


def generate_records(last_name, seed_num, favorite_artist):
	artist_letters = [character.upper() for character in favorite_artist if character.isalpha()]
	if not artist_letters:
		raise ValueError("Favorite artist must contain at least one letter.")

	records = []
	for student_index, label in enumerate(STUDENT_LABELS):
		student_name = f"{last_name}_{label}"
		for subject_index, subject in enumerate(SUBJECTS):
			position = len(records) % len(artist_letters)
			letter_position = ord(artist_letters[position]) - ord("A") + 1
			score = (
				seed_num * 5
				+ letter_position
				+ student_index * 3
				+ subject_index * 4
			) % 101
			if student_index == 2 and subject_index == 2:
				score = None

			records.append(
				{
					"student": student_name,
					"subject": subject,
					"assessment": f"Assessment_{subject_index + 1}",
					"score": score,
					"result": performance_category(score) if score is not None else None,
				}
			)

	records.append(records[0].copy())
	return records


def analyze_records(records):
	record_counts = Counter((record["student"], record["subject"]) for record in records)
	seen = set()
	repeated_records = []
	organized_data = defaultdict(dict)

	for record in records:
		key = (record["student"], record["subject"])
		if key in seen:
			repeated_records.append(record)
			continue
		seen.add(key)
		organized_data[record["student"]][record["subject"]] = record

	incomplete_records = [record for record in records if record["score"] is None]
	valid_records = [
		record
		for subjects in organized_data.values()
		for record in subjects.values()
		if record["score"] is not None
	]

	student_summaries = {}
	for student, subjects in organized_data.items():
		scores = [record["score"] for record in subjects.values() if record["score"] is not None]
		student_summaries[student] = {
			"valid_count": len(scores),
			"average": sum(scores) / len(scores) if scores else None,
			"highest": max(scores) if scores else None,
			"lowest": min(scores) if scores else None,
		}

	subject_summaries = {}
	for subject in SUBJECTS:
		scores = [record["score"] for record in valid_records if record["subject"] == subject]
		subject_summaries[subject] = {
			"valid_count": len(scores),
			"average": sum(scores) / len(scores) if scores else None,
			"highest": max(scores) if scores else None,
			"lowest": min(scores) if scores else None,
		}

	ordered_records = sorted(
		(record for subjects in organized_data.values() for record in subjects.values()),
		key=lambda record: (
			record["student"],
			SUBJECTS.index(record["subject"]),
		),
	)
	return {
		"record_counts": record_counts,
		"organized_data": organized_data,
		"repeated_records": repeated_records,
		"incomplete_records": incomplete_records,
		"student_summaries": student_summaries,
		"subject_summaries": subject_summaries,
		"ordered_records": ordered_records,
	}


def print_summary(title, summaries):
	print(f"\n{title}")
	for name, summary in summaries.items():
		if summary["average"] is None:
			print(f"{name:<24} No valid scores")
			continue
		print(
			f"{name:<24} Count: {summary['valid_count']}, "
			f"Average: {summary['average']:.2f}, "
			f"Highest: {summary['highest']}, Lowest: {summary['lowest']}"
		)


def print_report(favorite_artist, records, analysis):
	print("=== FINAL STUDENT PERFORMANCE REPORT ===")
	print(f"Student family name: {LAST_NAME}")
	print(f"Score seed: {SEED_NUM}")
	print(f"Favorite artist: {favorite_artist}")

	print("\nORDERED PERFORMANCE RECORDS")
	print(f"{'STUDENT':<25} {'SUBJECT':<15} {'ASSESSMENT':<14} {'SCORE':<7} RESULT")
	for record in analysis["ordered_records"]:
		score = record["score"] if record["score"] is not None else "MISSING"
		result = record["result"] or "INCOMPLETE"
		print(
			f"{record['student']:<25} {record['subject']:<15} "
			f"{record['assessment']:<14} {str(score):<7} {result}"
		)

	print("\nREPEATED STUDENT-SUBJECT RECORDS")
	for record in analysis["repeated_records"]:
		print(f"{record['student']} / {record['subject']} (duplicate entry)")
	if not analysis["repeated_records"]:
		print("None")

	print("\nINCOMPLETE RECORDS")
	for record in analysis["incomplete_records"]:
		print(f"{record['student']} / {record['subject']}: score missing")
	if not analysis["incomplete_records"]:
		print("None")

	print_summary("STUDENT SUMMARIES (valid scores only)", analysis["student_summaries"])
	print_summary("SUBJECT SUMMARIES (valid scores only)", analysis["subject_summaries"])

	category_counts = Counter(
		record["result"]
		for record in analysis["ordered_records"]
		if record["result"] is not None
	)
	print("\nPERFORMANCE CATEGORY COUNTS")
	for category in ("EXCELLENT", "GOOD", "SATISFACTORY", "NEEDS IMPROVEMENT", "AT RISK"):
		print(f"{category:<20} {category_counts[category]}")
	print(f"Raw records: {len(records)}; unique student-subject records: {len(analysis['ordered_records'])}")


def main():
	favorite_artist = input("Enter your favorite artist: ").strip()
	records = generate_records(LAST_NAME, SEED_NUM, favorite_artist)
	analysis = analyze_records(records)
	print_report(favorite_artist, records, analysis)


if __name__ == "__main__":
	main()
