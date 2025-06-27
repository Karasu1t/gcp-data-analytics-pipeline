from airflow import models
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

def notify_slack():
    webhook_url = "<Webhook URL>"
    message = {
        "text": ":tada: データマート更新が完了しました！\n👉 <https://lookerstudio.google.com/reporting/XXXXXXXXXXXXXXXX|最新レポートを確認>"
    }
    requests.post(webhook_url, json=message)

with models.DAG(
    dag_id="etl_and_datamart_pipeline",
    start_date=datetime(2025, 6, 28),
    schedule_interval="0 0 * * *",
    catchup=False,
) as dag:

    run_dataflow = DataflowStartFlexTemplateOperator(
        task_id="run_etl_flex_template",
        location="asia-east1",
        body={
            "launchParameter": {
                "jobName": "etl-job-{{ ds_nodash }}",
                "containerSpecGcsPath": "gs://dev-karasuit-dataflow/templates/etl_template.json",
                "parameters": {
                    "inputFile": "gs://dev-karasuit-etldata/*.zip",
                    "outputTable": "analytics_dataset.target_table"
                }
            }
        }
    )

    create_datamart = BigQueryInsertJobOperator(
        task_id="create_dm_analytics",
        configuration={
            "query": {
                "query": """
                    CREATE OR REPLACE TABLE analytics_dataset.dm_analytics AS
                    SELECT 
                        DATE(
                            SAFE_CAST(REGEXP_EXTRACT(o.datetime, r'^(\d{4})年') AS INT64),
                            SAFE_CAST(REGEXP_EXTRACT(o.datetime, r'(\d{1,2})月') AS INT64),
                            1
                        ) AS datetime,
                        SAFE_CAST(o.passengers AS INT64) AS passengers,
                        SAFE_CAST(p.employee AS INT64) * 10000 AS regularemployee,
                        SAFE_CAST(q.employee AS INT64) * 10000 AS nonregularemployee,
                        SAFE_CAST(r.salary AS INT64) AS salary,
                        (SAFE_CAST(p.employee AS INT64) + SAFE_CAST(q.employee AS INT64)) * 10000 AS total_employee
                    FROM `analytics_dataset.passengers` AS o
                    INNER JOIN `analytics_dataset.regularemployee` AS p ON o.datetime = p.datetime
                    INNER JOIN `analytics_dataset.nonregularemployee` AS q ON o.datetime = q.datetime
                    INNER JOIN `analytics_dataset.salary` AS r ON o.datetime = r.datetime;
                """,
                "useLegacySql": False
            }
        },
        location="asia-northeast1"
    )

    notify = PythonOperator(
        task_id="send_slack_notification",
        python_callable=notify_slack
    )

    run_dataflow >> create_datamart >> notify
