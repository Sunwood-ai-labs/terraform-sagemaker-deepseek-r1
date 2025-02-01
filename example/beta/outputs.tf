output "sagemaker_endpoint_name" {
  description = "作成されたSageMakerエンドポイントの名前"
  value       = aws_sagemaker_endpoint.deepseek_endpoint.name
}
