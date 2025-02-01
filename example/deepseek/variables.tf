variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-1"
}

variable "sagemaker_execution_role_name" {
  description = "Name for the SageMaker execution role"
  type        = string
  default     = "sagemaker-deepseek-execution-role"
}
