# Detection Schema

This document defines the required structure for all detections in this repository.

When building a new detection, you can use a completed detection subdirectory under detections/ as a template.

## Directory Structure

Each detection lives in its own directory under `detections/<data_source>/`:

```
detections/aws/s3_exfil_external_bucket/
├── detection.tf
├── README.md
└── tests/
    ├── should_match/
    ├── should_not_match/
    └── test_config.yaml
```

## Required Files

| File                    | Purpose                                                   | Phases Covered |
| ----------------------- | --------------------------------------------------------- | -------------- |
| detection.tf            | Detection logic, thresholds, alert configuration          | 2, 3, 4        |
| README.md               | Threat model context and analyst runbook                  | 1, 5           |
| tests/should_match/     | Sample logs that must trigger the detection               | 2              |
| tests/should_not_match/ | Sample logs that must not trigger (FP tests)              | 4              |
| tests/test_config.yaml  | Test configs/values for macros, lookups, conditions, etc. | 2, 4           |

## File Specifications

### detection.tf

Required elements:

- Resource name matching directory name
- `name` - Clear alert title (Actor + Action + Context format)
- `description` - Brief explanation of what the detection catches
- `search` or `query` - The detection logic
- `severity` - Alert severity level
- `mitre_attack` - Technique ID in tags or comments
- `message` - Alert context with key fields for analysts

### README.md

Required sections:

```markdown
# Detection Name

## Threat Model

- **Attacker Goal:** [What is the adversary trying to achieve?]
- **Detectable Behavior:** [Specific event/action being detected]
- **Data Source:** [e.g., CloudTrail, VPC Flow]
- **MITRE ATT&CK:** [Technique ID and name]

## Detection Logic

[Brief explanation of how the detection works, including any scale considerations or graceful degradation]

## Runbook

### Triage Steps

1. [First thing analyst should check]
2. [Second step]
3. [Third step]

### True Positive Response

[What to do if confirmed malicious]

### Known False Positives

[Document expected FP sources and why they're excluded]
```

### tests/

Requirements:

- At least one `.json` file in `should_match/` containing a log that triggers the detection
- At least one `.json` file in `should_not_match/` containing a log that should NOT trigger
- Test file names should be descriptive (e.g., `lambda_writes_to_external_bucket.json`)

### test_config.yaml

Defines test values for a given detection's efficacy/resiliency evaluation. Located at `tests/test_config.yaml`.

Possible sections:

```yaml
macros:
  "macro name":
    index: "index_name"
    sourcetype: "sourcetype_value"

lookups:
  lookup_name:
    "key1": "value1"
    "key2": "value2"

conditions:
  - field: "field.path"
    operator: "operator_type"
    value: "expected_value"
```

#### Condition Operators

| Operator           | Purpose                          | Required Fields          |
| ------------------ | -------------------------------- | ------------------------ |
| `equals`           | Field exactly matches value      | `field`, `value`         |
| `in`               | Field is in list of values       | `field`, `values` (list) |
| `contains`         | Field contains substring         | `field`, `value`         |
| `not_equals_field` | Field differs from another field | `field`, `other_field`   |
| `not_in_lookup`    | Field not in lookup table        | `field`, `lookup`        |

#### Example

```yaml
macros:
  "aws cloudtrail":
    index: "aws"
    sourcetype: "aws:cloudtrail"

lookups:
  aws_accounts_allowed:
    "111111111111": "internal-prod"
    "222222222222": "internal-dev"

conditions:
  - field: "eventName"
    operator: "in"
    values: ["PutObject", "CopyObject"]
  - field: "userIdentity.type"
    operator: "equals"
    value: "AssumedRole"
  - field: "resources[0].accountId"
    operator: "not_in_lookup"
    lookup: "aws_accounts_allowed"
```

## Completeness Checklist

A detection is not ready for merge until:

- [ ] detection.tf contains all required elements
- [ ] test_config.yaml has all required variables for efficacy testing
- [ ] README.md documents threat model and runbook
- [ ] At least one should_match test exists
- [ ] At least one should_not_match test exists
- [ ] MITRE ATT&CK technique is mapped
- [ ] Alert message includes actionable context
- [ ] Detection has been tested against sample logs
