from fastapi import APIRouter, BackgroundTasks, Depends
from tasks import import_students, delete_students
from auth_router import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/import")
def import_csv(file_path: str, background_tasks: BackgroundTasks, user_id: int = Depends(get_current_user)):
    background_tasks.add_task(import_students, file_path)
    return {"message": "import started"}


@router.post("/delete")
def delete(ids: list[int], background_tasks: BackgroundTasks, user_id: int = Depends(get_current_user)):
    background_tasks.add_task(delete_students, ids)
    return {"message": "delete started"}