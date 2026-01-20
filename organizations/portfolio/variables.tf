variable "splunk_url" {
  description = "Splunk instance URL"
  type        = string
}

variable "splunk_auth_token" {
  description = "Splunk authentication token"
  type        = string
  sensitive   = true    # Hides value in logs
}