"""
scripts/helper/notifications.py
================================
Notification / alerting helpers for Airflow DAGs.
"""

import logging
from typing import Optional

log = logging.getLogger(__name__)


def send_alert(context: dict, message: Optional[str] = None) -> None:
    """
    Generic on-failure callback that logs an alert.
    Attach to a DAG or task as on_failure_callback.

    Args:
        context: Airflow task context dictionary.
        message: Optional custom message to include in the alert.

    Example in a DAG::

        from helper.notifications import send_alert

        with DAG(
            dag_id="my_dag",
            default_args={"on_failure_callback": send_alert},
            ...
        ) as dag:
            ...
    """
    dag_id    = context.get("dag").dag_id
    task_id   = context.get("task_instance").task_id
    exec_date = context.get("execution_date")
    exception = context.get("exception")

    log.error(
        "ALERT | DAG: %s | Task: %s | Execution: %s | Error: %s | %s",
        dag_id, task_id, exec_date, exception,
        message or ""
    )


def task_success_log(context: dict) -> None:
    """
    Simple on-success callback that logs task completion details.
    Attach to a task as on_success_callback.

    Example::

        from helper.notifications import task_success_log

        PythonOperator(
            task_id="my_task",
            python_callable=my_func,
            on_success_callback=task_success_log,
        )
    """
    dag_id    = context.get("dag").dag_id
    task_id   = context.get("task_instance").task_id
    exec_date = context.get("execution_date")
    duration  = context.get("task_instance").duration

    log.info(
        "SUCCESS | DAG: %s | Task: %s | Execution: %s | Duration: %.2fs",
        dag_id, task_id, exec_date, duration or 0
    )
