terraform {
    required_providers {
        splunk = {
            source = "splunk/splunk"
        }
    }
}


provider "splunk" {
    url                  = var.splunk_url
    auth_token           = var.splunk_auth_token
    insecure_skip_verify = true     # For a trial instance with self-signed certs
}

