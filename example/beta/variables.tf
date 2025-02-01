variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "sagemaker_execution_role_name" {
  description = "IAM role name for SageMaker execution"
  type        = string
  default     = "sagemaker_execution_role_deepseek"
}

variable "sagemaker_endpoint_name" {
  description = "Name of the SageMaker endpoint (1-50 alphanumeric characters)"
  type        = string
  default     = "deepseek-r1-endpoint"
}

variable "jumpstart_model_image" {
  description = "Container image URI for the DeepSeek-R1 JumpStart model (update to actual URI)"
  type        = string
  default     = "123456789012.dkr.ecr.us-east-1.amazonaws.com/deepseek-llm-r1:latest"
}

variable "sagemaker_model_name" {
  description = "Name of the SageMaker model for DeepSeek-R1"
  type        = string
  default     = "deepseek-r1-model"
}

variable "sagemaker_endpoint_config_name" {
  description = "Name of the SageMaker endpoint configuration for DeepSeek-R1"
  type        = string
  default     = "deepseek-r1-endpoint-config"
}

variable "sagemaker_instance_type" {
  description = "Instance type for the production variant in the endpoint configuration"
  type        = string
  default     = "ml.g5.24xlarge"
}
