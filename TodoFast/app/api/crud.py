from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.db.firebase import get_todo_collection
from app.schemas.schema_todo import TodoCreate, TodoUpdate, TodoResponse
from app.auth.firebase_auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, user: dict = Depends(get_current_user)):
    todo_ref = get_todo_collection().document()
    todo_id = todo_ref.id
    new_todo = {**todo.dict(), "id": todo_id, "completed": False}
    todo_ref.set(new_todo)
    return new_todo

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: str, user: dict = Depends(get_current_user)):
    todo_ref = get_todo_collection().document(todo_id)
    todo = todo_ref.get()
    if not todo.exists:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo.to_dict()

@router.get("/", response_model=List[TodoResponse])
def get_all_todos(user: dict = Depends(get_current_user)):
    todos = get_todo_collection().stream()
    todo_list = [todo.to_dict() for todo in todos]
    return todo_list

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, todo_update: TodoUpdate, user: dict = Depends(get_current_user)):
    todo_ref = get_todo_collection().document(todo_id)
    todo = todo_ref.get()
    if not todo.exists:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_ref.update(todo_update.dict(exclude_unset=True))
    updated_todo = todo_ref.get().to_dict()
    return updated_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: str, user: dict = Depends(get_current_user)):
    todo_ref = get_todo_collection().document(todo_id)
    todo = todo_ref.get()
    if not todo.exists:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_ref.delete()
    return {"message": "Todo deleted"}