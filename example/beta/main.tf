# SageMakerモデルの作成
resource "aws_sagemaker_model" "deepseek_model" {
  name               = var.sagemaker_model_name
  execution_role_arn = aws_iam_role.sagemaker_execution_role.arn

  primary_container {
    image = var.jumpstart_model_image
    
    environment = {
      SAGEMAKER_CONTAINER_LOG_LEVEL = "20"
      SAGEMAKER_REGION             = var.region
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.sagemaker_full_access,
    aws_iam_role_policy.ecr_access
  ]
}

# エンドポイント設定
resource "aws_sagemaker_endpoint_configuration" "deepseek_endpoint_config" {
  name = var.sagemaker_endpoint_config_name

  production_variants {
    variant_name           = "AllTraffic"
    model_name            = aws_sagemaker_model.deepseek_model.name
    initial_instance_count = 1
    instance_type         = var.sagemaker_instance_type
  }
}

# エンドポイントの作成
resource "aws_sagemaker_endpoint" "deepseek_endpoint" {
  name                 = var.sagemaker_endpoint_name
  endpoint_config_name = aws_sagemaker_endpoint_configuration.deepseek_endpoint_config.name
}