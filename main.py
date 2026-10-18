LAST_NAME = "Ocampo"
STUDENT_ID = "TUPM-26-7949"

seed_digit = int(STUDENT_ID[-1]) 
id_checksum = sum(int(d) for d in STUDENT_ID if d.isdigit())
vector_dim = len(LAST_NAME)

sys_config = {
    "operator": LAST_NAME,
    "auth_id": STUDENT_ID,
    "base_seed": seed_digit,
    "checksum": id_checksum,
    "vector_dimension": vector_dim,
    "status": "INITIALIZED"
}

print("== SYSTEM CONFIGURATION ==")
for key, value in sys_config.items():
    print(f"{key.upper()}: {value}")

base_val = sys_config["base_seed"]
number_sequence = [base_val, base_val + 15, sys_config["checksum"]]

print(f"Initial Sequence: {number_sequence}")

number_sequence.append(base_val + 20)
print(f"After Append: {number_sequence}")

new_numbers = [base_val + 5, sys_config["vector_dimension"], base_val]
number_sequence.extend(new_numbers)
print(f"After Extend: {number_sequence}")

base_count = number_sequence.count(base_val)
print(f"Occurances of {base_val}: {base_count}")

number_sequence.sort()
print(f"Sorted Sequence: {number_sequence}")

fixed_coordinates = (sys_config["vector_dimension"], sys_config["base_seed"], 0)
print(f"Fixed Coordinates: {fixed_coordinates}")

x_val, y_val, z_val = fixed_coordinates
print(f"Unpacked Values -> X: {x_val}, Y: {y_val}, Z: {z_val}")

print("\nAttempting Modification...")
try:
    fixed_coordinates[0] = 99
except TypeError as error_msg:
    print(f"Modification Error: {error_msg}")

data_payload = {
    "identifier": sys_config["auth_id"],
    "dimension": sys_config["vector_dimension"],
    "status": "active"
}

print("--- Payload Data ---")
for key, value in data_payload.items():
    print(f"{key.capitalize()}: {value}")

data_payload["efficiency_rating"] = 98.5
print(f"\nUpdated Payload: {data_payload}")

base_val = sys_config["base_seed"]
raw_data = [base_val, base_val + 5, base_val, sys_config["vector_dimension"], base_val + 5]
print(f"\nRaw List (with dupliates): {raw_data}")

unique_data = set(raw_data)
print(f"Unique Set: {unique_data}")


reference_set = {base_val, base_val + 10, base_val + 20}
print(f"Reference Set: {reference_set}")

common_elements = unique_data.intersection (reference_set)
combined_elements = unique_data.union(reference_set)
print(f"Intersection (Common): {common_elements}")
print(f"Union (Combined): {combined_elements}")

import array

number_array = array.array('i', [sys_config["base_seed"],
sys_config["vector_dimension"], 100])
print(f"Integer Array: {number_array}")

print("\nAttempting to append a string...")
try:
    number_array.append("invalid")
except TypeError as error_msg:
    print(f"Type Error: {error_msg}")

base_val = sys_config["base_seed"]

generated_list = [(x * base_val) for x in range(1, 6)]
print(f"Generated Comprehension: {generated_list}")

filtered_list = [x for x in generated_list if x > 15]
print(f"Filtered Comprehension (Values > 15): {filtered_list}")

from collections import deque

data_queue = deque([sys_config["base_seed"], sys_config["vector_dimension"]])
print(f"Initial Deque: {data_queue}")

data_queue.append(100)
data_queue.appendleft (200)
print(f"After Appends: {data_queue}")

data_queue.popleft()
print(f"Final Deque (After Popleft): {data_queue}")

from collections import defaultdict

default_data = defaultdict(int)

default_data['active_key'] = sys_config["vector_dimension"]
print(f"Existing Key Value: {default_data['active_key']}")

print(f"Missing Key Value (Auto-generated): {default_data['unknown_key']}")