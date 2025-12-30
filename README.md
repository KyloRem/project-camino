# Project Camino

A detection-as-code repository demonstrating security detection engineering best practices. Built following Datadog's detection-as-code patterns with a structured 5-phase detection development lifecycle.

![project camino logo](assets/projectCaminoLogo.png)

## Overview

Project Camino treats security detections as code. These detections are version controlled, tested, and deployed through CI/CD pipelines; each detection includes threat modeling documentation, detection logic in Terraform, and test cases for validation. 

When developing new detections, scalability and resiliency that accounts for different environmental factors as well as edge cases should be prioritized. 

**Current platform:** Detections are written in Splunk SPL using the Splunk Terraform provider, but the patterns and methodology are transferable to other SIEMs with Terraform support.

## Getting Started

1. Review the [Detection Lifecycle](docs/DETECTION_LIFECYCLE.md)
2. Review the [Schema Requirements](docs/SCHEMA.md)
3. Use an existing detection as your starting point
4. Ensure all schema requirements are met before merging

## Detection Development Lifecycle

Every detection follows a 5-phase process:

| Phase | Focus | Artifact |
|-------|-------|----------|
| 1. Threat Model | What are we detecting and why? | README.md |
| 2. Initial Detection | Core query: Event + Actor + Risk | detection.tf |
| 3. Scale Considerations | Baselines, graceful degradation | detection.tf |
| 4. Tuning Strategy | Reduce false positives | detection.tf |
| 5. Signal Quality | Actionable alerts | detection.tf, README.md |

See [DETECTION_LIFECYCLE.md](docs/DETECTION_LIFECYCLE.md) for full details.

## Repository Structure
```
├── docs/                      # Framework and standards
│   ├── DETECTION_LIFECYCLE.md # 5-phase detection methodology
│   └── SCHEMA.md              # Detection completeness requirements
├── detections/                # Detection rules by data source
│   └── aws/
│       └── <detection_name>/
│           ├── detection.tf   # Detection logic (Terraform)
│           ├── README.md      # Threat model + runbook
│           └── tests/         # Validation test cases
├── lib/                       # Python tooling (validation, coverage)
└── organizations/             # Terraform deployment configs
```

## Detections

| Detection | Data Source | MITRE ATT&CK |
|-----------|-------------|--------------|
| [Lambda Exfil to External S3](detections/aws/lambda_exfil_to_external_s3/) | AWS CloudTrail | T1537 |

## References

- [MITRE ATT&CK Cloud Matrix](https://attack.mitre.org/matrices/enterprise/cloud/)
- [Splunk Terraform Provider](https://registry.terraform.io/providers/splunk/splunk/latest/docs)
- [Datadog: Detection as Code](https://www.datadoghq.com/blog/datadog-detection-as-code/)