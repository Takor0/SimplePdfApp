import os
from celery import Celery

from src.config import CELERY_RESULT_BACKEND, CELERY_BROKER_URL


def create_celery() -> Celery:
    app = Celery(
        "pdf_workers",
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND,
        include=["src.tasks.pdf"],
    )

    return app


celery_app = create_celery()
