# Задача "Модель пользователя"
from email.policy import default
from http.client import responses

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, List

app = FastAPI()

class User(BaseModel):
    id: int = Field(default=None, ge=1, le=100, description="User ID")  # номер пользователя
    username: str = Field(default="Undefined", min_length=3, max_length=20, description="User name")  # имя пользователя
    age: int = Field(default=18, ge=18, le=120, description="User age")  # возраст пользователя

users = []

# получение данных
@app.get('/users', response_model=List[User])
async def get_all_messages(): #-> List[User]:
    return users


@app.get('/user/{user_id}', response_model=User)
async def get_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example=1)]): #-> User:
    for cur_user in users:
        if cur_user.id == user_id:
            return cur_user
    raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не найден")

# создание нового пользователя
@app.post('/user/{username}/{age}', response_model=User)
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example=24)]): # -> User:
    new_id = 1
    if users:
        new_id = users[-1].id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


# обновление данных
@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example=1)],
                      username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example='UrbanProfi')],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example=28)]): # -> User:
    for cur_user in users:
        if cur_user.id == user_id:
            cur_user.username = username
            cur_user.age = age
            return cur_user
    raise HTTPException(status_code=404, detail="User was not found")

# запрос на удаление конкретного пользователя
@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example=2)]): # -> str:
    for i, cur_user in enumerate(users):
        if cur_user.id == user_id:
            del_user = users.pop(i)
            return del_user
    raise HTTPException(status_code=404, detail="User was not found")

# запрос на удаление всей БД
@app.delete('/users')
async def delete_all_users() -> str:
    users.clear()
    return f"All messages deleted."

