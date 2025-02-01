#!/usr/bin/env python3
import boto3
import json

# ※ 必要に応じて、環境変数やAWSプロファイルの設定を行ってください

# 作成したSageMakerエンドポイント名（Terraformの変数と一致させる）
ENDPOINT_NAME = "deepseek-r1-endpoint"

def invoke_deepseek(prompt, max_new_tokens=128, temperature=0.6, top_p=0.9):
    runtime = boto3.client("sagemaker-runtime")
    
    # 入力用のテンプレート（ブログ記事中の例に準拠）
    payload = {
        "inputs": f"You are an AI assistant. Do as the user asks.\n### Instruction: {prompt}\n### Response: <think>",
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
    }
    
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="application/json",
        Body=json.dumps(payload)
    )
    
    result = json.loads(response["Body"].read().decode())
    return result

if __name__ == "__main__":
    test_prompt = "What's 1+1?"
    result = invoke_deepseek(test_prompt)
    print("Model response:")
    print(json.dumps(result, indent=2))
