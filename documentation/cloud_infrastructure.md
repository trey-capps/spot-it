# Cloud Infrastructure

Terraform has been used to manage and create the cloud infrastructure for Spot-It on Google Cloud Platform. Terraform uses infrastrucutre as code (IaC) to allow users to create infrastructure through code that can be shared and versioned.

Learn more about Terraform [here](https://www.terraform.io/intro). 

## Resources Created

- Google Cloud Storage Bucket
- More to come!

## Steps to Setup Infrastructure for Spot-It (on GCP)

1. Install Terraform
2. Create service account for Terraform
3. Terraform directory
``` cd SpotIt/src/terraform ```
4. Setup configuration files 
- ```main.tf```
    - This file is where we will define all resources will want to use/setup
- ```provider.tf```
    - This file allows Terraform to interact with cloud providers
    - In our case we will add configurations from Google Cloud Platform
- ```variables.tf```
    - This file declares input variables
- ```terraform.tfvars``` 
    - This file is used to define the values of our input variables. This file is ignored by Git but can be defined like the example below:
    ```
    gcp_project  = "[enter project name]"
    gcp_region = "[enter project region]"
    ...
    ```
5. Initialize the directory
Use the following command: ```terraform init```
6. Create infrastructure
Use the following command: ```terraform apply```
7. Terminate infrastructure
If you want to terminate all the resources you created with Terraform use: ```terraform destroy```

[Back to README](../README.md)