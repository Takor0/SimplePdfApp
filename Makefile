dev_run:
	uvicorn src.main:app --host localhost --port 8000
dev_run_server:
	uvicorn src.main:app --host "::" --port 8000
dev_run_celery:
	celery -A src.celery_app:celery_app worker --loglevel=info
