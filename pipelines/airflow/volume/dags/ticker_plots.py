from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {'owner': 'az',
                'start_date': datetime(2021, 1, 4),
                'retries': 2,
                'retry_delay': timedelta(minutes=1)}

with DAG(dag_id='ticker_plots',
        # catchup means that airflow will execute all tasks from the start_date in default_args
        catchup=True,
        default_args=default_args,
        # pipeline starts at every third hour:
        # schedule_interval='* */3 * * *'
        # 1 day intereval:
        #schedule_interval=timedelta(1)
        # 2 minutes interval:
        #schedule_interval=timedelta(minutes=2)
        # 1 day intereval:
        schedule_interval=timedelta(1)) as dag:
    print_pwd = BashOperator(task_id='print_working_dir',
                             bash_command='echo "WORKDIR: $(pwd)"')

    get_ticker = BashOperator(task_id='get_ticker',
                             bash_command='cd /usr/local/airflow \
                                               && python -m src.get_ticker --ticker_name AAPL \
                                                                    --date_time {{ ds }} \
                                                                    --interval 60m \
                                                                    --output_folder ./data')
    make_plot = BashOperator(task_id='make_plot',
                             bash_command='cd /usr/local/airflow \
                                               && python -m src.make_plot --ticker_name AAPL \
                                                                   --date_time {{ ds }} \
                                                                   --output_folder ./data')

print_pwd >> get_ticker >> make_plot
#print_context >> [getting_articles, getting_telemetry] >> done

