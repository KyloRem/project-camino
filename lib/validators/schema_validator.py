from pathlib import Path

# Define the root directory (e.g. the current working directory)
detections_dir = Path('detections')

# Track overall validation status
validation_passed = True

# Loop through the data sources (first level)
for data_src in detections_dir.iterdir():
     if data_src.is_dir():
          # Loop through the detections in each data source (second level)
          for detection in data_src.iterdir():
               if detection.is_dir():
                    # Check for required files
                    readme_exists = (detection / 'README.md').exists()
                    tf_exists = (detection / 'detection.tf').exists()

                    # Check test directories have files
                    should_match_dir = detection / 'tests' / 'should_match'
                    should_not_match_dir = detection / 'tests' / 'should_not_match'

                    # Check if should_match_dir has .json files
                    should_match_files = list(should_match_dir.glob('*.json'))
                    has_should_match = len(should_match_files) > 0

                    # Check if should_not_match_dir has .json files
                    should_not_match_files = list(should_not_match_dir.glob('*.json'))
                    has_should_not_match = len(should_not_match_files) > 0

                    # Print results
                    print(f"{detection}: README={readme_exists}, Terraform={tf_exists}, Should Match File(s)={has_should_match}, Should Not Match File(s)={has_should_not_match}")

                    # Evaluate all compliance checks, print result
                    all_pass = readme_exists and tf_exists and has_should_match and has_should_not_match
                    if all_pass:
                         print("PASS")
                    else:
                         print("FAIL")
                         validation_passed = False

# Note something failed so CI/CD will block the merge
if not validation_passed:
     exit(1)