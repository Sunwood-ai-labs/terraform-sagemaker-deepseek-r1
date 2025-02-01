# 🤖 DeepSeek LLM SageMakerデプロイメント例

このディレクトリには、DeepSeek LLMをAWS SageMakerにデプロイするために必要な設定とスクリプトが含まれています。

## 📋 前提条件

- AWS CLIがインストールされ、適切に設定されていること
- Terraformがインストールされていること
- Python 3.8以上がインストールされていること
- 必要なPythonパッケージがインストールされていること

## 🚀 デプロイ手順

1. Terraformの初期化：
```bash
terraform init
```

2. インフラストラクチャのデプロイ：
```bash
terraform apply
```

3. Pythonの仮想環境を作成し、必要なパッケージをインストール：
```bash
python -m venv .venv
source .venv/bin/activate
pip install sagemaker
```

4. DeepSeek LLMのデプロイ：
```bash
python deploy_deepseek.py
```

## 🛠️ カスタマイズ

- `variables.tf`でAWSリージョンやIAMロール名を変更できます
- `deploy_deepseek.py`の引数でモデルIDやインスタンスタイプを指定できます：
  ```bash
  python deploy_deepseek.py --model-id deepseek-llm-r1 --instance-type ml.g5.2xlarge --endpoint custom-endpoint
  ```

## ⚠️ 注意事項

- SageMakerのエンドポイントは使用中は課金が発生します
- 使用後は`terraform destroy`でリソースを削除することを推奨します
- 大規模なインスタンスタイプを使用する場合は、AWSのクォータ制限を確認してください
