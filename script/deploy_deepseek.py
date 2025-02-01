#!/usr/bin/env python3
import argparse
import logging
import json

from sagemaker.jumpstart.model import ModelAccessConfig
from sagemaker.serve.builder.model_builder import ModelBuilder
from sagemaker.serve.builder.schema_builder import SchemaBuilder
from sagemaker.session import Session


def deploy_deepseek(model_id, instance_type, endpoint_name):
    # Create a SageMaker session
    sagemaker_session = Session()
    
    # Get the execution role ARN (assumes proper AWS credentials are configured)
    execution_role = sagemaker_session.get_caller_identity_arn()
    
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
    
    # Deploy the model to SparkMaker endpoint
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
    sample_input = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 128, "top_p": 0.9, "temperature": 0.6}
    }
    result = predictor.predict(sample_input)
    print("\nPrediction result:")
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Deploy and test DeepSeek-R1 using SageMaker JumpStart via CLI (no GUI required)"
    )
    parser.add_argument(
        "--model-id",
        default="deepseek-llm-r1",
        help="DeepSeek model identifier used by JumpStart (default: deepseek-llm-r1)"
    )
    parser.add_argument(
        "--instance-type",
        default="ml.p5e.48xlarge",
        help="SageMaker instance type (default: ml.p5e.48xlarge)"
    )
    parser.add_argument(
        "--endpoint",
        default="deepseek-r1-endpoint",
        help="Name of the endpoint to create (default: deepseek-r1-endpoint)"
    )
    parser.add_argument(
        "--test-prompt",
        default="What's 1+1?",
        help="Prompt for test inference (default: What's 1+1?)"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    
    predictor = deploy_deepseek(args.model_id, args.instance_type, args.endpoint)

    print("\nDeployment complete. Running test prediction...")
    run_prediction(predictor, args.test_prompt)

    # Uncomment the following lines to clean up resources after testing
    predictor.delete_model()
    predictor.delete_endpoint()


if __name__ == "__main__":
    main()
