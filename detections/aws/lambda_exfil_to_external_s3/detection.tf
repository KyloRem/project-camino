resource "splunk_saved_searches" "lambda_exfil_to_external_s3" {
  name        = "AWS - Lambda exfiltrating data to external S3 bucket"
  description = <<-EOT
    Detects potential data exfiltration via AWS Lambda to an external S3 bucket. This detection identifies instances where an AWS Lambda function is performing PutObject or CopyObject operations to an S3 bucket outside your organization. MITRE ATT&CK: T1537
    Lambda function detected writing to external S3 bucket.
    Target Bucket: $result.target_bucket$
    Actor: $result.actor$
    Destination Account: $result.dest_account$
    Source Account: $result.src_account$
    Region: $result.region$
    Event Count: $result.event_count$
    First Seen: $result.first_seen$
    Last Seen: $result.last_seen$

    MITRE ATT&CK: T1537 - Transfer Data to Cloud Account

    Triage Steps:
    1. Identify the Lambda and check the IAM role assigned to it
    2. Investigate the destination bucket ownership
    3. Check for recent UpdateFunctionCode events for this Lambda
    4. Examine traffic volume - single file or high-frequency dump?
EOT 

  search = <<-EOT
    `aws cloudtrail` 
    eventName IN ("PutObject", "CopyObject")
    userIdentity.type=AssumedRole
    userIdentity.arn=*lambda.amazonaws.com*
    | where 'userIdentity.accountId' != 'resources{}.accountId'
    | lookup aws_accounts_allowed accountId AS resources{}.accountId OUTPUT accountName
    | where isnull(accountName)
    | rename requestParameters.bucketName as target_bucket
    | eval _time = strptime(eventTime, "%Y-%m-%dT%H:%M:%SZ")
    | stats count as event_count, values(userIdentity.arn) as actor, values(userAgent) as userAgent, values(awsRegion) as region, values(userIdentity.accountId) as src_account, values(resources{}.accountId) as dest_account, earliest(_time) as first_seen, latest(_time) as last_seen by target_bucket
  EOT

  # Scheduling
  is_scheduled  = true
  cron_schedule = "*/5 * * * *"

  # Alert trigger
  alert_type       = "number of events"
  alert_comparator = "greater than"
  alert_threshold  = 0

  # Severity (1-2=info, 3-4=low, 5-6=medium, 7-8=high, 9-10=critical)
  alert_severity = 8

  # MITRE ATT&CK: T1537 - Transfer Data to Cloud Account
  # https://attack.mitre.org/techniques/T1537/

  # Alert message

}
