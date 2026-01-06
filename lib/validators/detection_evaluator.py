import json
import yaml

# Open and load the should_match file
with open('detections/aws/lambda_exfil_to_external_s3/tests/should_match/lambda_puts_to_external_bucket.json', 'r') as should_match_file:
    should_match = json.load(should_match_file)

# Open and load the should_not_match file
with open('detections/aws/lambda_exfil_to_external_s3/tests/should_not_match/lambda_puts_to_internal_bucket.json', 'r') as should_not_match_file:
    should_not_match = json.load(should_not_match_file)

# Open and load the test_config.yaml
with open('detections/aws/lambda_exfil_to_external_s3/tests/test_config.yaml', 'r') as test_config_file:
    test_config = yaml.safe_load(test_config_file)

# Access the dictionaries
print(should_match)
print(should_not_match)
print(test_config)