# Detection Development Lifecycle

This document defines the 5-phase process for developing detections in this repository.

## Why Do We Have This Process? 

Developing resilient, high quality detections at scale requires a thorough methodology. This methodology needs to consider the overall threat model, a system for developing the foundational detection, how to prevent drift, and the overall longterm health of the detection among other factors.

This process serves as your blueprint; use it to journey from an abstract threat model to effective detection and response actions with confidence. 

## Phase 1: Threat Model

Before writing any detection logic, you need to understand what you're detecting and why. A clear threat model prevents you from chasing vague "suspicious activity" and keeps the detection focused on real attacker behavior.

- [ ] Define the attacker's goal.  
- [ ] What events or API calls would indicate this behavior?  
    - Define what's detectable and be specific (e.g. "S3: PutObject to external bucket" instead of "S3 Suspicious Activity"  
- [ ] Identify data sources for the event(s)  
    - AWS Cloudtrail/GuardDuty? Okta IM2:log? Crowdstrike:devices?  
- [ ] Identify MITRE ATT&CK technique(s)  
    - [Cloud Matrix](https://attack.mitre.org/matrices/enterprise/cloud/)  
    - [Containers Matrix](https://attack.mitre.org/matrices/enterprise/containers/)  

## Phase 2: Initial Detection

Building a robust detection needs to start simple. Catch the foundational behavior with a "core query" before you start applying thresholds and baselines. 

Build your core query using this structure:

**[Data Source/Event] + [Actor Context] + [Risk Indicator]**

Example:
- `eventName = "DeleteDBSnapshot"` (event)
- `by IAM User` (actor context)
- `from new IP address` (risk indicator)

[] Write the core query  
[] Add immediate context filters to remove obvious noise  
[] Enrich with fields an analyst would need to investigate  
    - Who? (user, role, service account)  
    - What? (resource affected, action taken)  
    - Where? (region, account, network)  
    - When? (timestamp, duration)  
    - Anything else?  

### Data Source Quick Reference (AWS Only)

| Source | Best For |
|--------|----------|
| CloudTrail | Who did what, when (IAM changes, config changes, data access) |
| VPC Flow | Network activity (C2, exfil, lateral movement) |
| CloudWatch | Application-level behavior (Lambda, RDS) |
| GuardDuty | AWS-native threat intel, corroboration |

### Actor Context Considerations

- `userIdentity.type=AssumedRole` → Usually a service (Lambda, EC2)
- `userIdentity.type=IAMUser` → Usually a human
- Which actor type matters for this detection?

## Phase 3: Scale Considerations

When building high quality, resilient detections, you need to consider multiple environment variables. This helps you approach the problem with a best-practice mindset from the beginning. 

### The Problem

- Entity A tags production as `prod`
- Entity B has no tags
- Entity C uses `production`
- You can't hardcode asset lists or IP ranges because "expected" and "anomalous" are different in each environment. 

### Scalable Solutions

- [ ] Use dynamic baselining (e.g. compare today's activity to the entity's history over the last 30 days)  
- [ ] Use relative thresholds (e.g. `10x normal` not fixed numbers)  
- [ ] Use tag-based logic (leverage entity's own asset tags if possible)  
    - Detection still fires without tags, tags just enhance severity/context  

Example:
```spl
| eval is_production = if(match(resourceTags, "prod|production"), "true", "unknown")
| eval severity = if(is_production="true", "critical", "high")
```


### Graceful Degradation

What if baseline data isn't available? New entity, data retention issues, etc.

Design detections with fallback tiers:

| Tier | Condition | Logic | Severity |
|------|-----------|-------|----------|
| 1 (Ideal) | Baseline available | Alert if never seen in 30 days | Critical |
| 2 (Okay) | No baseline, have account info | Alert if different AWS account | High |
| 3 (Basic) | Minimal context | Alert if high volume + unusual time | Medium |

- [ ] Document graceful degradation tiers in `scale.yaml`

## Phase 4: Tuning Strategy

In development, "drift" is when a deployed system (in our case, a detection) experiences performance or characteristic changes over time, deviating from its initial intended state. This leads to inaccuracy, errors, and gaps. 

Phase 4 aims to define a systematic process for reducing false positives after deployment via a Four-Layer Tuning Method. 

**Layer 1: Tighten Core Logic**
- [ ] Combine multiple weak signals  
- [ ] Add time-based correlation  
- [ ] Require sequence of events  

**Layer 2: Exclude Known-Good**
- [ ] Service account exclusions (with documented reason)  
- [ ] Automation tool filtering  
- [ ] Expected maintenance windows  
- [ ] Known infrastructure patterns  

*Requires feedback loops - analysts mark FPs, exclusions get added.*

**Layer 3: Add Baseline Context**
Detect deviation from normal, not just "suspicious" actions.

- [ ] First-time-seen logic (new bucket, new region, new role)  
- [ ] Volume anomalies (10x normal transfer)  
- [ ] Temporal anomalies (3am activity for 9-5 user)  
- [ ] Geographic anomalies (login from new country)  

**Layer 4: Require Business Impact**
Focus on what matters. Filter for:

- [ ] Critical assets  
```spl
| where (bucket IN critical_buckets) OR (resourceTags LIKE "%production%")
```
- [ ] Data classification  
```spl
| where data_classification IN ("restricted", "confidential")
```
- [ ] Compliance scope  
```spl
| where (pci_scope=true OR sox_scope=true)
```
- [ ] Privilege level  
```spl
| where (admin_role=true OR cross_account_role=true)
```

## Phase 5: Signal Quality

A detection is only valuable if it can be understood and acted on quickly.

### Alert Title Format

**Actor + Suspicious Action + Key Context**

Bad: `S3 Alert`
Good: `Lambda execution role wrote to external S3 bucket`

### Required Alert Components

- [ ] Clear, descriptive title  
- [ ] Severity rating based on risk  
- [ ] Key fields surfaced (who, what, where, when)  
- [ ] Recommended response steps  
- [ ] Links to relevant runbooks or resources  

### Example Alert
```
Alert: Lambda execution role wrote to external S3 bucket
Severity: High

Lambda: my-api-function
Bucket: attacker-exfil-bucket (external account)
First seen: Yes (never accessed this bucket before)

Recommended Actions:
1. Review Lambda code for unauthorized changes
2. Check IAM role permissions  
3. Verify bucket ownership
4. Check for other exfil indicators
```

- [ ] Document alert template in detection's README.md 