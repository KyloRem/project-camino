# Lambda Exfiltrating Data to External S3 Bucket

## Threat Model

- **Attacker Goal:** Exfiltrate sensitive data to attacker-controlled storage
- **Detectable Behavior:** Lambda execution role performs s3:PutObject to an S3 bucket in a different AWS account
- **Data Source:** CloudTrail
- **MITRE ATT&CK:** [T1537 - Transfer Data to Cloud Account](https://attack.mitre.org/techniques/T1537/)

## Detection Logic

This detection identifies Lambda functions writing objects to S3 buckets outside the source AWS account. 

The core query looks for:
- `eventName=PutObject` 
- `userIdentity.type=AssumedRole` (Lambda execution context)
- Destination bucket account differs from source account

### Scale Considerations

- Baselines bucket access per Lambda over 30 days when available
- Falls back to cross-account check if no baseline exists
- Severity elevated if destination bucket is completely new to the environment

### Known False Positives

- Cross-account backup services (excluded by role name pattern)
- S3 cross-region replication to DR accounts
- Legitimate data sharing with partner accounts

## Runbook

### Triage Steps

1. Identify the Lambda function and review its intended purpose
2. Check if the destination bucket/account is known and authorized
3. Review recent code changes to the Lambda function
4. Examine the IAM role permissions - are they overly broad?
5. Check for other indicators of compromise on the source account

### True Positive Response

1. Disable the Lambda function immediately
2. Revoke the execution role's permissions
3. Preserve CloudTrail logs for investigation
4. Identify what data was exfiltrated
5. Check destination bucket for exfiltrated objects (if accessible)
6. Investigate how the Lambda was compromised (code injection, supply chain, stolen credentials)

### Related Detections

- IAM role policy changes
- Lambda code updates
- Unusual Lambda invocation patterns