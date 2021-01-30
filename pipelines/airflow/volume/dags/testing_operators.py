from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


def print_context(**context):
    """Print the Airflow context and ds variable from the context."""
    print('AVAILABLE CONTEXT:', context)


# Use the op_args and op_kwargs arguments to pass additional arguments to the Python callable.
def square_argument(argument: int) -> None:
    """Square the argument"""
    print(f'SQUARE {argument} =', argument**2)

default_args = {'owner': 'az',
                'start_date': datetime(2021, 1, 1),
                'retries': 5,
                'retry_delay': timedelta(minutes=1)}

with DAG(dag_id='test_operators',
        # catchup means that airflow will execute all tasks from the start_date in default_args
        catchup=True,
        default_args=default_args,
        # pipeline starts at every third hour:
        # schedule_interval='* */3 * * *'
        # 1 day intereval:
        #schedule_interval=timedelta(1)
        # 2 minutes interval:
        schedule_interval=timedelta(minutes=2)) as dag:
    
    print_context = PythonOperator(task_id='print_the_context', 
                                   python_callable=print_context,
                                   provide_context=True)
    square_argument = PythonOperator(task_id='square_the_argument', 
                                     python_callable=square_argument,
                                     op_kwargs={'argument': 5})     
    
    bash_test = BashOperator(task_id='check_bash',
                             bash_command='echo "current ds: {{ ds }}"')

print_context >> square_argument >> bash_test
#print_context >> [getting_articles, getting_telemetry] >> done

