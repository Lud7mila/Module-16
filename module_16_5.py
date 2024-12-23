# Задача "Модель пользователя"
from email.policy import default
from http.client import responses
from lib2to3.fixes.fix_input import context

from fastapi import FastAPI, Path, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, ValidationError
from typing import Annotated, List

# FastAPI(debug=True): Включает режим отладки, который выводит более подробные сообщения об ошибках в консоль.
# swagger_ui_parameters={"tryItOutEnabled": True позволяет в swagger не нажимать постоянно Try It Out
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

# Настраиваем Jinja2 для загрузки шаблонов из папки templates
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int = Field(default=None, ge=1, le=100, description="User ID")  # номер пользователя
    username: str = Field(default=None, min_length=3, max_length=20, description="User name")  # имя пользователя
    age: int = Field(default=None, ge=18, le=120, description="User age")  # возраст пользователя

users: List[User] = [] #User(id = 1, username="first_user", age=28)]


# получение данных
@app.get('/', response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse(name="users.html", context={"request": request, "users": users})


@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_user(request: Request,
                   user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", examples=1)]): #-> User:
    for cur_user in users:
        if cur_user.id == user_id:
            return templates.TemplateResponse(name="users.html", context={"request": request, "user": cur_user})
    raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не найден")

# добавление нового пользователя
@app.post('/user/{username}/{age}', response_class=HTMLResponse)
async def create_user(request: Request,
                      username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", examples='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", examples=24)]):
    new_id = 1
    if users:
        new_id = users[-1].id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse(name="users.html", context={"request": request, "users": users})

@app.post('/', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
async def create_user(request: Request,
                      age: int = Form(),
                      username: str = Form(), #Annotated[str, Path(min_length=5, max_length=20, description="Enter username", examples='UrbanUser')],
                      #age: Annotated[int, Path(ge=18, le=120, description="Enter age", examples=24)],
                      ):
    new_id = 1
    if users:
        new_id = users[-1].id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse(name="users.html", context={"request": request, "users": users})


# обновление данных
@app.put('/user/{user_id}/{username}/{age}', response_class=HTMLResponse)
async def update_user(request: Request,
                    user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", examples=1)],
                    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", examples='UrbanProfi')],
                    age: Annotated[int, Path(ge=18, le=120, description="Enter age", examples=28)]): # -> User:
    for cur_user in users:
        if cur_user.id == user_id:
            cur_user.username = username
            cur_user.age = age
            return templates.TemplateResponse(name="users.html", context={"request": request, "users": users})
    raise HTTPException(status_code=404, detail="User was not found")

# запрос на удаление конкретного пользователя
@app.delete('/user/{user_id}', response_class=HTMLResponse)
async def delete_user(request: Request,
                      user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", examples=2)]):
    for i, cur_user in enumerate(users):
        if cur_user.id == user_id:
            del_user = users.pop(i)
            return templates.TemplateResponse(name="users.html", context={"request": request, "users": users})
    raise HTTPException(status_code=404, detail="User was not found")

# запрос на удаление всей БД
@app.delete('/user')
async def delete_all_users() -> str:
    users.clear()
    return f"All messages deleted."

