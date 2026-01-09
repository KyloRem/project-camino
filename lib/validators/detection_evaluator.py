import json
import yaml
from pathlib import Path
import sys


# =============================================================================
# ARGUMENT SUPPORT
# =============================================================================

# sys.argv[0] is the script name
# sys.argv[1] is the first argument (if provided)

if len(sys.argv) > 1:
    target_detection = sys.argv[1]
else:
    target_detection = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_field(data, path):
    """
    Extract a value from nested dictionary using dot notation.
    Supports array indexing: 'resources[0].accountId'
    
    Example: get_field(log, 'userIdentity.type') returns 'AssumedRole'
    """
    value = data
    parts = path.split('.')
    
    for part in parts:
        if '[' in part:
            # Handle array notation like 'resources[0]'
            bracket_pos = part.index('[')
            key = part[0:bracket_pos]           # 'resources'
            index_str = part[bracket_pos+1:-1]  # '0'
            index = int(index_str)              # 0
            value = value[key][index]
        else:
            value = value[part]
    
    return value


# =============================================================================
# FIND AND EVALUATE DETECTIONS
# =============================================================================

detections_dir = Path('detections')
detection_found = False

for data_src in detections_dir.iterdir():
    if data_src.is_dir():
        for detection in data_src.iterdir():
            if detection.is_dir():
                # Build dynamic paths to files
                detection_name = detection.name
                # Skip if a specific detection was requested and this isn't it
                if target_detection and detection_name != target_detection:
                    continue
                detection_found = True
                test_config_path = detection / 'tests' / 'test_config.yaml'
                should_match_dir = detection / 'tests' / 'should_match'
                should_not_match_dir = detection / 'tests' / 'should_not_match'
                tf_path = detection / 'detection.tf'

                
                # Print the detection name
                print("=" * 60)
                print(f"Detection Name: {detection_name}")
                print("=" * 60)
                print()

                # Load test configuration
                with open(test_config_path, 'r') as f:
                    test_config = yaml.safe_load(f)

                # Load detection.tf for macro validation
                with open(tf_path, 'r') as f:
                    tf_content = f.read()


                # ==========================================================
                # MACRO VALIDATION (once per detection)
                # ==========================================================
                
                print("Evaluating macro conditions...")
                print("-" * 60)

                for macro_name in test_config['macros']:
                    if f"`{macro_name}`" in tf_content:
                        print(f"Macro '{macro_name}' found in detection.tf → PASS")
                    else:
                        print(f"Macro '{macro_name}' NOT found in detection.tf → FAIL")
                print()


                # ==========================================================
                # POSITIVE TESTS (should_match files)
                # ==========================================================
                
                print("[POSITIVE TESTS]")
                print()

                should_match_files = list(should_match_dir.glob('*.json'))
                for file in should_match_files:
                    with open(file, 'r') as f:
                        should_match = json.load(f)
                    
                    print(f"Evaluating: {file.name}")
                    print("-" * 60)

                    for condition in test_config['conditions']:
                        field = condition['field']
                        operator = condition['operator']

                        if operator == 'equals':
                            # Check if field exactly matches expected value
                            actual = get_field(should_match, field)
                            expected = condition['value']
                            result = "PASS" if actual == expected else "FAIL"
                            print(f"{field}: '{actual}' equals '{expected}' → {result}")

                        elif operator == 'in':
                            # Check if field value is in list of allowed values
                            actual = get_field(should_match, field)
                            expected = condition['values']
                            result = "PASS" if actual in expected else "FAIL"
                            print(f"{field}: '{actual}' in {expected} → {result}")

                        elif operator == 'contains':
                            # Check if field contains a substring
                            actual = get_field(should_match, field)
                            expected = condition['value']
                            result = "PASS" if expected in actual else "FAIL"
                            print(f"{field}: '{actual}' contains '{expected}' → {result}")

                        elif operator == 'not_equals_field':
                            # Check if the expected field does not match another specified field in the same log
                            other_field = condition['other_field']
                            actual = get_field(should_match, field)
                            other_actual = get_field(should_match, other_field)
                            result = "PASS" if actual != other_actual else "FAIL"
                            print(f"{field}: {actual} != '{other_field}': '{other_actual}' → {result}")

                        elif operator == "not_in_lookup":
                            # Check if a specific value in the log is not in the test_config lookup
                            actual = get_field(should_match, field)
                            lookup_name = condition['lookup']
                            lookup_data = test_config['lookups'][lookup_name]
                            result = "PASS" if actual not in lookup_data else "FAIL"
                            print(f"{field}: '{actual}' is not in lookup '{lookup_name}' → {result}")
                    
                    print()


                # ==========================================================
                # NEGATIVE TESTS (should_not_match files)
                # ==========================================================
                
                print("[NEGATIVE TESTS]")
                print()

                should_not_match_files = list(should_not_match_dir.glob('*.json'))
                for file in should_not_match_files:
                    with open(file, 'r') as f:
                        should_not_match = json.load(f)
                    
                    print(f"Evaluating: {file.name}")
                    print("-" * 60)

                    for condition in test_config['conditions']:
                        field = condition['field']
                        operator = condition['operator']

                        if operator == 'equals':
                            # Check if field exactly matches expected value
                            actual = get_field(should_not_match, field)
                            expected = condition['value']
                            result = "PASS" if actual == expected else "FAIL"
                            print(f"{field}: '{actual}' equals '{expected}' → {result}")

                        elif operator == 'in':
                            # Check if field value is in list of allowed values
                            actual = get_field(should_not_match, field)
                            expected = condition['values']
                            result = "PASS" if actual in expected else "FAIL"
                            print(f"{field}: '{actual}' in {expected} → {result}")

                        elif operator == 'contains':
                            # Check if field contains a substring
                            actual = get_field(should_not_match, field)
                            expected = condition['value']
                            result = "PASS" if expected in actual else "FAIL"
                            print(f"{field}: '{actual}' contains '{expected}' → {result}")

                        elif operator == 'not_equals_field':
                            # Check if the expected field does not match another specified field in the same log
                            other_field = condition['other_field']
                            actual = get_field(should_not_match, field)
                            other_actual = get_field(should_not_match, other_field)
                            result = "PASS" if actual != other_actual else "FAIL"
                            print(f"{field}: {actual} != '{other_field}': '{other_actual}' → {result}")

                        elif operator == "not_in_lookup":
                            # Check if a specific value in the log is not in the test_config lookup
                            actual = get_field(should_not_match, field)
                            lookup_name = condition['lookup']
                            lookup_data = test_config['lookups'][lookup_name]
                            result = "PASS" if actual not in lookup_data else "FAIL"
                            if result == "PASS":
                                print(f"{field}: '{actual}' is not in lookup '{lookup_name}' → {result}")
                            elif result == "FAIL":
                                print(f"{field}: '{actual}' found in lookup '{lookup_name}' → {result}")
print()


# =============================================================================
# ERROR HANDLING
# =============================================================================

if target_detection and not detection_found:
    print(f"ERROR: Detection '{target_detection}' not found")
    exit(1)