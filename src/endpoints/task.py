from fastapi import APIRouter, HTTPException, status

from src.celery_app import celery_app
from src.validators.task import TaskRequestModel

router = APIRouter(
    prefix="/api/task",
    tags=["task"],
)


@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task.id,
        "status": task.status,
        "result": task.result if task.ready() else None,
        "error": str(task.result) if task.failed() else None,
    }


@router.post("/run", status_code=status.HTTP_202_ACCEPTED)
def run_task(request: TaskRequestModel):
    try:
        async_result = celery_app.send_task(
            request.task_name,
            kwargs=request.model_dump(exclude={"task_name"}),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot run task: {str(e)}",
        )

    return {"task_id": async_result.id}
