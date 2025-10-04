# 🤖 lambda_line_reserve - LINE連携ホテル予約API (AWS Lambda)

> **LINEからホテル予約を自動化するサーバーレスAIシステム**

![Python](https://img.shields.io/badge/python-3.9+-blue)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)

![Python](https://img.shields.io/badge/python-3.9+-blue)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📘 概要

`lambda_line_reserve` は、**LINEチャットからホテル予約を行うためのAWS Lambda関数**です。  
ユーザーがLINE上で自然な会話を通じて宿泊予約を行えるように設計されています。  
Amazon API Gateway・DynamoDB・LINE Messaging APIを組み合わせ、**音声・テキストベースの自動予約体験**を実現します。

このプロジェクトは、**AIによる自然言語理解**と**AWSサーバーレスアーキテクチャ**を融合し、  
ホテル・旅館などの宿泊施設が**LINE公式アカウントを通じて予約受付を自動化**できるようにします。

---

## 🧩 主な機能

- 💬 **LINEチャット連携**：ユーザーのメッセージをWebhook経由で受信  
- 🧠 **自然言語解析**：ChatGPT APIや独自ロジックで意図を解析  
- 🏨 **ホテル予約処理**：宿泊日・人数・部屋タイプなどを自動登録  
- 🔄 **RAG（Retrieval-Augmented Generation）対応**：FAQや観光情報を検索して回答  
- ☁️ **サーバーレス構成**：AWS Lambda + API Gateway + DynamoDB  
- 🧾 **予約確認・キャンセル・更新**：ユーザーの要望に応じて予約情報を動的に変更  
- 🔐 **環境変数・認証管理**：`.env` とAWS Secrets Managerで安全にキーを管理  

---

## 🏗️ アーキテクチャ構成

```
LINEユーザー
   ↓
LINE Messaging API (Webhook)
   ↓
API Gateway
   ↓
AWS Lambda (lambda_line_reserve)
   ↓
DynamoDB / 外部予約API
```

---

## 📁 ディレクトリ構成

```
lambda_line_reserve/
├── main.py                    # Lambdaエントリーポイント
├── line_handler.py            # LINEメッセージ処理
├── reservation_service.py     # 予約ロジック
├── utils/                     # 共通ユーティリティ
│   ├── validation.py          # 入力検証
│   ├── logger.py              # CloudWatchログ出力
│   └── api_client.py          # 外部API通信
├── requirements.txt           # 依存パッケージ
└── README.md                  # 本ドキュメント
```

---

## 🧱 前提条件

- Python 3.9 以上  
- AWSアカウント（Lambda, API Gateway, DynamoDBの利用権限）  
- LINE Developersアカウント（Messaging API設定済み）  
- OpenAI APIキー（ChatGPT利用時）

---

## ⚙️ セットアップ手順

### 1. 仮想環境の作成
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定
`.env` ファイルを作成し、以下を設定します。
```bash
LINE_CHANNEL_SECRET=your_line_secret
LINE_CHANNEL_ACCESS_TOKEN=your_access_token
OPENAI_API_KEY=your_openai_key
```

---

## 🧪 ローカルテスト

### Lambda関数のローカル実行
```bash
python lambda_function.py
```

### Webhookイベントのテスト
```bash
curl -X POST http://localhost:8000/line/webhook -H "Content-Type: application/json" -d '{"events": [...]}'
```

---

## 🚀 デプロイ方法

### AWS CLIを使用する場合
```bash
zip -r function.zip .
aws lambda update-function-code --function-name lambda_line_reserve --zip-file fileb://function.zip
```

### SAMまたはServerless Frameworkを使用する場合
`template.yaml` または `serverless.yml` を設定して自動デプロイ可能です。

---

## 🧰 トラブルシューティング

| 問題 | 原因 | 対処法 |
|------|------|--------|
| Lambdaがタイムアウトする | 外部API応答遅延 | タイムアウト設定を延長（例: 30秒→60秒） |
| LINEから応答がない | Webhook URL未設定 | LINE Developersで正しいURLを設定 |
| DynamoDBにデータが保存されない | IAM権限不足 | Lambdaロールに`dynamodb:PutItem`権限を付与 |

---

## 💬 使用例

### LINEチャットでの対話例
```
ユーザー: 明日2名で宿泊予約をしたいです。
AI: ご希望のチェックイン日と部屋タイプを教えてください。
```

### API呼び出し例
```bash
curl -X POST https://your-api-endpoint/line/webhook -d '{"events": [...]}'
```

---

## 🧠 技術スタック

| カテゴリ | 使用技術 |
|-----------|-----------|
| 言語 | Python 3.9+ |
| クラウド | AWS Lambda, API Gateway, DynamoDB |
| 外部API | LINE Messaging API, OpenAI API |
| 開発補助 | boto3, requests, python-dotenv |

---

## 🧾 ライセンス

このプロジェクトは **MITライセンス** のもとで公開されています。  
詳細は `LICENSE` ファイルをご確認ください。

---

## 👥 コントリビューション

バグ報告・機能提案・プルリクエストは歓迎します。  
以下の手順で開発に参加できます。

1. リポジトリをフォーク  
2. 新しいブランチを作成  
3. 変更をコミット  
4. プルリクエストを送信  

```bash
git clone https://github.com/okatano-toshiso/lambda_line_reserve.git
git checkout -b feature/your-feature
```

---

## 👤 作者情報

| 項目 | 内容 |
|------|------|
| **名前** | 岡田 俊宏 (Toshihiro Okada) |
| **GitHub** | [okatano-toshiso](https://github.com/okatano-toshiso) |
| **所属** | SynapseAI |
| **専門分野** | AIソリューション開発・AWSサーバーレス設計・自然言語処理 |
| **連絡先** | info@synapseai.jp |

---

## 📚 参考資料

- [GitHub公式: READMEの書き方](https://docs.github.com/ja/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [Qiita: READMEの書き方まとめ](https://qiita.com/shun198/items/c983c713452c041ef787)
- [C++ Learning: READMEの基本構成](https://cpp-learning.com/readme/)
- [Reddit: Good README Templates](https://www.reddit.com/r/programming/comments/l0mgcy/github_readme_templates_creating_a_good_readme_is/?tl=ja)
