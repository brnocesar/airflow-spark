from datetime import datetime
from os.path import abspath, join
from airflow.models import DAG
from airflow.operators.alura import TwitterOperator

with DAG(dag_id="twitter_dag", start_date=datetime.now()) as dag:
    twitter_operator = TwitterOperator(
        task_id="twitter_aluraonline",
        query="AluraOnline",
        file_path=join(
            abspath("datalake").replace("/airflow/dags", ""),
            "twitter_aluraonline",
            "extract_date={{ ds }}",
            "AluraOnline_{{ ds_nodash}}.json"
        )
    )