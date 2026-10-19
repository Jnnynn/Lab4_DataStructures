from collections import Counter, defaultdict


LAST_NAME = "Ocampo"
SEED_NUM = 9
PRODUCTS = ("NOTEBOOK", "PEN", "USB", "HEADPHONES", "CALCULATOR")
PRODUCT_PRICES = {
	"NOTEBOOK": 2.50,
	"PEN": 1.25,
	"USB": 12.99,
	"HEADPHONES": 24.99,
	"CALCULATOR": 18.50,
}
PRODUCT_CATEGORIES = {
	"NOTEBOOK": "STATIONERY",
	"PEN": "STATIONERY",
	"USB": "ELECTRONICS",
	"HEADPHONES": "ELECTRONICS",
	"CALCULATOR": "SCHOOL EQUIPMENT",
}
CUSTOMER_LABELS = tuple(f"C{number}" for number in range(1, 6))


def generate_records(last_name, seed_num, favorite_artist):
	artist_letters = [character.upper() for character in favorite_artist if character.isalpha()]
	if not artist_letters:
		raise ValueError("Favorite artist must contain at least one letter.")

	artist_positions = [ord(character) - ord("A") + 1 for character in artist_letters]
	transaction_pairs = []
	for customer_index in range(len(CUSTOMER_LABELS)):
		product_indices = (
			customer_index,
			(customer_index + 1) % len(PRODUCTS),
			(customer_index + 3) % len(PRODUCTS),
		)
		transaction_pairs.extend((customer_index, product_index) for product_index in product_indices)

	transaction_pairs.append((0, 0))
	records = []
	for transaction_index, (customer_index, product_index) in enumerate(transaction_pairs):
		product = PRODUCTS[product_index]
		quantity = (
			seed_num
			+ artist_positions[transaction_index % len(artist_positions)]
			+ customer_index
			+ product_index
			+ transaction_index
		) % 10 + 1
		records.append(
			{
				"transaction_id": f"T{transaction_index + 1:02d}",
				"customer": f"{last_name}_{CUSTOMER_LABELS[customer_index]}",
				"product": product,
				"category": PRODUCT_CATEGORIES[product],
				"quantity": quantity,
				"unit_price": PRODUCT_PRICES[product],
				"total_value": quantity * PRODUCT_PRICES[product],
			}
		)
	return records


def analyze_records(records):
	organized_data = defaultdict(lambda: defaultdict(list))
	pair_counts = Counter()
	for record in records:
		organized_data[record["customer"]][record["product"]].append(record)
		pair_counts[(record["customer"], record["product"])] += 1

	ordered_records = sorted(
		records,
		key=lambda record: (
			record["customer"],
			PRODUCTS.index(record["product"]),
			record["transaction_id"],
		),
	)
	repeated_purchases = [
		{"customer": customer, "product": product, "count": count}
		for (customer, product), count in sorted(pair_counts.items())
		if count > 1
	]

	customer_summaries = {}
	for customer in sorted(organized_data):
		customer_records = [
			record
			for product_records in organized_data[customer].values()
			for record in product_records
		]
		customer_summaries[customer] = {
			"transaction_count": len(customer_records),
			"distinct_products": len(organized_data[customer]),
			"total_quantity": sum(record["quantity"] for record in customer_records),
			"total_value": sum(record["total_value"] for record in customer_records),
		}

	product_summaries = {}
	for product in PRODUCTS:
		product_records = [record for record in records if record["product"] == product]
		product_summaries[product] = {
			"transaction_count": len(product_records),
			"distinct_customers": len({record["customer"] for record in product_records}),
			"total_quantity": sum(record["quantity"] for record in product_records),
			"total_value": sum(record["total_value"] for record in product_records),
		}

	return {
		"organized_data": organized_data,
		"ordered_records": ordered_records,
		"repeated_purchases": repeated_purchases,
		"customer_summaries": customer_summaries,
		"product_summaries": product_summaries,
		"total_value": sum(record["total_value"] for record in records),
		"total_quantity": sum(record["quantity"] for record in records),
		"distinct_customers": len({record["customer"] for record in records}),
		"distinct_products": len({record["product"] for record in records}),
	}


def print_report(favorite_artist, records, analysis):
	print("=== FINAL CONSOLIDATED TRANSACTION REPORT ===")
	print(f"Customer family name: {LAST_NAME}")
	print(f"Quantity seed: {SEED_NUM}")
	print(f"Favorite artist: {favorite_artist}")

	print("\nORDERED TRANSACTION RECORDS")
	print(f"{'ID':<5} {'CUSTOMER':<16} {'PRODUCT':<13} {'CATEGORY':<19} {'QTY':>3} {'UNIT PRICE':>11} {'TOTAL':>10}")
	for record in analysis["ordered_records"]:
		print(
			f"{record['transaction_id']:<5} {record['customer']:<16} "
			f"{record['product']:<13} {record['category']:<19} "
			f"{record['quantity']:>3} ${record['unit_price']:>9.2f} "
			f"${record['total_value']:>8.2f}"
		)

	print("\nORGANIZED CUSTOMER / PRODUCT RELATIONSHIPS")
	for customer in sorted(analysis["organized_data"]):
		products = analysis["organized_data"][customer]
		product_details = ", ".join(
			f"{product} ({len(products[product])} transaction(s))"
			for product in PRODUCTS
			if product in products
		)
		print(f"{customer}: {product_details}")

	print("\nREPEATED CUSTOMER-PRODUCT PURCHASES")
	if analysis["repeated_purchases"]:
		for purchase in analysis["repeated_purchases"]:
			print(
				f"{purchase['customer']} / {purchase['product']}: "
				f"{purchase['count']} transactions"
			)
	else:
		print("None")

	print("\nCUSTOMER SUMMARIES")
	for customer, summary in analysis["customer_summaries"].items():
		print(
			f"{customer:<16} Transactions: {summary['transaction_count']}, "
			f"Products: {summary['distinct_products']}, "
			f"Quantity: {summary['total_quantity']}, "
			f"Value: ${summary['total_value']:.2f}"
		)

	print("\nPRODUCT SUMMARIES")
	for product, summary in analysis["product_summaries"].items():
		print(
			f"{product:<13} Transactions: {summary['transaction_count']}, "
			f"Customers: {summary['distinct_customers']}, "
			f"Quantity: {summary['total_quantity']}, "
			f"Value: ${summary['total_value']:.2f}"
		)

	print("\nOVERALL TRANSACTION SUMMARY")
	print(f"Transaction records: {len(records)}")
	print(f"Distinct customers: {analysis['distinct_customers']}")
	print(f"Distinct products: {analysis['distinct_products']}")
	print(f"Repeated customer-product pairs: {len(analysis['repeated_purchases'])}")
	print(f"Total quantity sold: {analysis['total_quantity']}")
	print(f"Overall transaction value: ${analysis['total_value']:.2f}")


def main():
	favorite_artist = input("Enter your favorite artist: ").strip()
	records = generate_records(LAST_NAME, SEED_NUM, favorite_artist)
	analysis = analyze_records(records)
	print_report(favorite_artist, records, analysis)


if __name__ == "__main__":
	main()
