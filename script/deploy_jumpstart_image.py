#!/usr/bin/env python3
# deploy_jumpstart_image.py
import argparse
import re
import boto3
from sagemaker import image_uris

def get_jumpstart_image_uri(model_id, region):
    """JumpStartモデル用のECRイメージURIを取得"""
    try:
        return image_uris.retrieve(
            framework=None,
            region=region,
            model_id=model_id,
            model_version="1.0.0",
            image_scope="inference",
            instance_type="ml.g5.24xlarge"  # インスタンスタイプを変更
        )
    except ValueError as e:
        print(f"❌ モデルイメージの取得に失敗: {e}")
        print("利用可能なモデルIDとリージョンの組み合わせを確認してください")
        raise

def update_terraform_vars(image_uri, region):
    """terraform.tfvarsを更新"""
    try:
        with open("terraform.tfvars", "r+") as f:
            content = f.read()
            
            # リージョンとイメージURIを更新
            updated = re.sub(
                r'region\s*=\s*".+"',
                f'region = "{region}"',
                content
            )
            updated = re.sub(
                r'jumpstart_model_image\s*=\s*".+"',
                f'jumpstart_model_image = "{image_uri}"',
                updated
            )
            
            f.seek(0)
            f.write(updated)
            f.truncate()
            
        print(f"✅ terraform.tfvarsを更新しました（リージョン: {region}）")
        return True
    except Exception as e:
        print(f"❌ ファイル更新エラー: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="JumpStartモデルイメージURI取得ツール")
    parser.add_argument("--model-id", required=True, help="JumpStartモデルID（例: deepseek-llm-r1）")
    parser.add_argument("--region", default="us-east-1", help="AWSリージョン（デフォルト: us-east-1）")
    args = parser.parse_args()

    print(f"🔍 モデルイメージを取得中... [モデルID: {args.model_id}, リージョン: {args.region}]")
    
    try:
        # イメージURI取得
        image_uri = get_jumpstart_image_uri(args.model_id, args.region)
        print(f"🔄 取得したイメージURI: {image_uri}")
        
        # Terraform変数ファイル更新
        if update_terraform_vars(image_uri, args.region):
            print("\n🎉 設定が正常に更新されました！以下のコマンドでデプロイを実行してください：")
            print("terraform init && terraform apply")
            
    except Exception as e:
        print(f"🚨 エラーが発生しました: {str(e)}")
        print("👉 トラブルシューティングのヒント：")
        print("- AWS CLIの認証設定を確認")
        print("- 指定したリージョンでモデルが利用可能か確認")
        print("- IAMロールにAmazonEC2ContainerRegistryReadOnly権限があるか確認")

if __name__ == "__main__":
    main()