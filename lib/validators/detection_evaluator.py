import json
import yaml

# =============================================================================
# LOAD TEST FILES
# =============================================================================

# Load sample log that SHOULD trigger the detection
with open('detections/aws/lambda_exfil_to_external_s3/tests/should_match/lambda_puts_to_external_bucket.json', 'r') as f:
    should_match = json.load(f)

# Load sample log that should NOT trigger the detection
with open('detections/aws/lambda_exfil_to_external_s3/tests/should_not_match/lambda_puts_to_internal_bucket.json', 'r') as f:
    should_not_match = json.load(f)

# Load test configuration (conditions, lookups, macros)
with open('detections/aws/lambda_exfil_to_external_s3/tests/test_config.yaml', 'r') as f:
    test_config = yaml.safe_load(f)


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
# EVALUATE CONDITIONS
# =============================================================================

print("Evaluating should_match log...")
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
        print(f"{field}: {actual} != '{other_actual}' → {result}")

    elif operator == "not_in_lookup":
        # Check if a specific value in the log is not in the test_config lookup
        actual = get_field(should_match, field)
        lookup_name = condition['lookup']
        lookup_data = test_config['lookups'][lookup_name]
        result = "PASS" if actual not in lookup_data else "FAIL"
        print(f"{field}: '{actual}' is not in lookup '{lookup_name}' → {result}")

