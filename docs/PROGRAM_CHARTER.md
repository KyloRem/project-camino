# Program Charter: Threat-Informed Detection Engineering (TIDE)

## 1. Mission Statement

The mission of the **TIDE Program** is to provide high-fidelity, actionable security monitoring for the organization’s most critical assets. We transition from a "coverage-first" mindset to a **"risk-first"** mindset, ensuring that our limited engineering resources are spent on detections that prevent business-ending events.

## 2. Core Principles

- **Asset-Centric:** We prioritize our "Crown Jewels" (Identity, CI/CD, Production Infrastructure) over generic or low-risk alerts.
- **Quality over Quantity:** We prioritize high-fidelity alerts. A single, reliable alert is more valuable than 50 noisy ones that cause SOC fatigue.
- **Prevention First:** If a threat can be mitigated through configuration or policy, we prioritize that fix over building a detection.
- **Actionability:** Every detection must be accompanied by a runbook. If an alert cannot be investigated or remediated by the SOC, it does not belong in production.

---

## 3. The TIDE Lifecycle

We follow a repeatable five-stage process to move from an abstract threat to a production alert:

1.  **Threat Modeling:** Identifying "Abuser Stories" and technical attack paths for a specific Crown Jewel.
2.  **Telemetry Audit:** Verifying that the required logs exist, are being ingested, and contain the necessary fields.
3.  **Engineering & Tuning:** Authoring logic and testing it against 30 days of historical data to identify and filter "noise."
4.  **Adversary Emulation:** Manually simulating the attack (e.g., using Atomic Red Team) to verify the alert triggers as expected.
5.  **Operationalization:** Deploying the alert to the SIEM and providing the outsourced SOC with a validated response runbook.

For detailed engineering methodology, see [DETECTION_LIFECYCLE.md](docs/DETECTION_LIFECYCLE.md)

---

## 4. Roles & Responsibilities

| Role                                | Responsibility                                                                        |
| :---------------------------------- | :------------------------------------------------------------------------------------ |
| **Internal DE Team (2 People)**     | Crown Jewel identification, threat modeling, SIEM architecture, and alert authoring.  |
| **Engineering/DevOps Partners**     | Providing technical context during quarterly threat modeling workshops.               |
| **On-Call Rotation / SOC Analysts** | 24/7 monitoring, initial triage according to runbooks, and feedback on alert quality. |
| **Leadership**                      | Defining business risk and approving the "Crown Jewels" list.                         |

---

## 5. Governance & Cadence

To ensure consistent progress with a lean team, we adhere to the following schedule:

### A. Asset & Intake

- **Annual Crown Jewel Audit:** Formal review with the CTO/CISO to rank the top 3-5 business-critical assets. This list dictates the roadmap for the following 12 months.
- **New Project Intake:** Any request for new detections outside of the "Crown Jewel" list must undergo a brief risk-assessment to determine if it supersedes current priorities.

### B. Quarterly Deep Dives

- **Month 1:** **Functional Threat Model.** Decompose one Crown Jewel into "Abuser Stories."
- **Month 2:** **Engineering & Authoring.** Build the telemetry and logic for that Jewel.
- **Month 3:** **Validation & SOC Hand-off.** Test the alerts and train the outsourced SOC.

### C. Monthly Maintenance

- **The Tuning Sprint:** Reviewing "The Noisy Ten" and adjusting logic based on SOC feedback.

---

## 6. Definition of "Done"

A detection is considered "Production Ready" only when it meets these criteria:

- [ ] **Documentation:** The alert logic and intent are documented in the central repository.
- [ ] **Validation:** The alert has been successfully triggered by a simulated attack.
- [ ] **Baseline:** The alert has undergone a 7-day "soak" period in report-only mode with acceptable noise levels.
- [ ] **Runbook:** A step-by-step investigation guide has been delivered to the SOC.

---

## 7. Success Metrics (KPIs)

- **False Positive Ratio:** Targeted at < 10% for all TIDE-authored alerts.
- **Crown Jewel Coverage:** Percentage of "Abuser Stories" successfully monitored.
- **MTTD (Mean Time to Detect):** Reduction in time between attack simulation and alert firing.
