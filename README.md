# 📊 GCP Data Analytics Pipeline

## 📌 概要

本プロジェクトは、Google Cloud 上における**自動化されたデータ分析パイプライン**の構築を目的としています。  
Cloud Storage 上のCSVファイルを起点に、Cloud Composer によるスケジュール制御、Dataflow によるETL処理、  
BigQuery によるデータマート生成、Workflows によるSlack通知を連携させたフローを構成しています。

> データ分析の一連の流れをGCP上で完結できる構成を学習・再現できるようにすることを目的としています。

---

## 🎯 この構成で実現できること

- GCP上でデータ分析基盤（ETL〜集計〜通知）を構築
- ComposerやDataflowなどのマネージドサービス連携を体得
- BigQuery上に自動的に構築されたデータマートをもとに、Slack通知などの運用連携が可能

---

## 🗺 アーキテクチャ図

![アーキテクチャ図](picture/arch.png)

---

## ✅ 処理の流れ

1. Cloud Storage にCSVファイルが格納されている状態を前提とします
2. Cloud Composer の DAG により毎朝 9:00 にパイプラインが起動
3. Dataflow が起動し、Cloud Storage 上のCSVを加工して BigQuery に格納
4. BigQuery 上でマート用のクエリが自動実行され、集計テーブルが作成される
5. Workflows により、レポート生成完了後に Slack 通知が送信され、必要に応じてDLリンクも共有される

---

## 🖥 使用環境

| 項目 | 内容 |
|------|------|
| OS | Ubuntu（WSL2）5.15.167.4 |
| Terraform | v1.12.1（任意） |
| Google Cloud SDK | 522.0.0 |
| bq CLI | 2.1.16 |
| Python | 3.10以上（DAG/Dataflowスクリプト） |

---

## 📁 フェーズ構成（説明順）

| フェーズ | 説明 |
|---------|------|
| Phase 1 | Cloud Storage・BigQuery・Composer・Slack Webhook の準備 |
| Phase 2 | Cloud Composer による定期スケジューリング設定 |
| Phase 3 | Dataflow によるCSVのETL処理 → BigQuery書き込み |
| Phase 4 | BigQuery 上でのマート生成クエリ実行 |
| Phase 5 | Workflows によるSlack通知とレポートDLリンクの送信 |

---

## 📌 成果物の例

- Slack通知のスクリーンショット（Workflows経由）
- BigQuery 上に生成されたマートテーブル
- Composer DAG UI 上でのジョブ可視化
- （任意）Cloud Storage へ出力されたレポートCSVファイル

---

## 🛠 使用技術スタック

- **Cloud Composer**（Airflowベースのスケジューラ）
- **Dataflow**（Apache BeamベースのETL処理基盤）
- **BigQuery**（DWH & SQL分析）
- **Workflows**（マネージドワークフロー管理）
- **Slack Webhook**（通知連携）

---

## ⚠️ 注意事項

- `dev/locals.tf` 等に記載されるプロジェクトIDなどの機密情報は `.gitignore` に追加してください
- ServiceAccountのkeyファイルは公開せず、Secret Manager 等で管理してください
- Slack WebhookのURLは外部に漏れないように環境変数またはSecret Manager経由で参照してください

---

## 📌 備考

この構成は、マーケティングやデータ分析基盤構築の実務において頻出の構成です。  
業務自動化・レポーティング・通知までを含む一連のパイプラインの理解・実践に役立ちます。

---

