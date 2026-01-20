# Main.tf is where Terraform knows what to deploy
    # Ties everything together. Each detection is a module that main.tf calls.      

module "lambda_exfil_to_external_s3" {
    source = "../../detections/aws/lambda_exfil_to_external_s3"
}