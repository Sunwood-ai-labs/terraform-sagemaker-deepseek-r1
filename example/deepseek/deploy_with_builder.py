#!/usr/bin/env python3
import argparse
import logging
import json
import os

from sagemaker.jumpstart.model import ModelAccessConfig
from sagemaker.serve.builder.model_builder import ModelBuilder
from sagemaker.serve.builder.schema_builder import SchemaBuilder
from sagemaker.session import Session


def get_sagemaker_role():
    """Terraformの出力からSageMakerロールARNを取得"""
    try:
        with open('terraform.tfstate') as f:
            tfstate = json.load(f)
        return tfstate['outputs']['sagemaker_role_arn']['value']
    except Exception as e:
        raise Exception("SageMaker実行ロールのARNが見つかりません。Terraformをapplyしてください。") from e


def deploy_deepseek(model_id, instance_type, endpoint_name):
    # Create a SageMaker session
    sagemaker_session = Session()
    
    # Get the execution role ARN from Terraform state
    execution_role = get_sagemaker_role()
    
    # Define sample input and expected output for schema building
    sample_input = {
        "inputs": "Hello, I'm a language model,",
        "parameters": {"max_new_tokens": 128, "top_p": 0.9, "temperature": 0.6}
    }
    sample_output = [{"generated_text": "Hello, I'm a language model, and I'm here to help you with your English."}]
    
    # Build schema
    schema_builder = SchemaBuilder(sample_input, sample_output)
    
    logging.info("Building model with JumpStart model ID: %s", model_id)
    
    # Build the model using SageMaker JumpStart
    model_builder = ModelBuilder(
        model=model_id,
        schema_builder=schema_builder,
        sagemaker_session=sagemaker_session,
        role_arn=execution_role,
        log_level=logging.ERROR
    )

    model = model_builder.build()
    
    logging.info("Deploying model to endpoint '%s' using instance type '%s'", endpoint_name, instance_type)
    
    # Deploy the model to SageMaker endpoint
    predictor = model.deploy(
        model_access_configs={
            model_id: ModelAccessConfig(accept_eula=True)
        },
        accept_eula=True,
        instance_type=instance_type,
        initial_instance_count=1,
        endpoint_name=endpoint_name
    )
    
    return predictor


def run_prediction(predictor, prompt):
    """モデルにテストプロンプトを送信"""
    request = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 128, "top_p": 0.9, "temperature": 0.6}
    }
    
    print(f"\nSending test prompt: {prompt}")
    response = predictor.predict(request)
    print("\nResponse:", json.dumps(response, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='DeepSeek LLMをSageMakerにデプロイ')
    parser.add_argument('--model-id', type=str, default='deepseek-llm-r1',
                      help='JumpStartモデルID (default: deepseek-llm-r1)')
    parser.add_argument('--instance-type', type=str, default='ml.p5e.48xlarge',
                      help='インスタンスタイプ (default: ml.p5e.48xlarge)')
    parser.add_argument('--endpoint', type=str, default='deepseek-r1-rcecypfxrc-endpoint',
                      help='エンドポイント名 (default: deepseek-r1-endpoint)')
    parser.add_argument('--test-prompt', type=str,
                      default='日本の歴史について教えてください。',
                      help='テスト用プロンプト')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    predictor = deploy_deepseek(args.model_id, args.instance_type, args.endpoint)
    
    print("\nデプロイメント完了。テスト予測を実行中...")
    run_prediction(predictor, args.test_prompt)
        
    # Uncomment the following lines to clean up resources after testing
    predictor.delete_model()
    predictor.delete_endpoint()


if __name__ == "__main__":
    main()
