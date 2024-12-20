# Задача "Имитация работы с БД"

from fastapi import FastAPI, Path, HTTPException

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

# получение данных
@app.get('/users')
async def get_all_messages() -> dict:
    return users

@app.get('/user/{user_id}')
async def get_user(user_id: int = Path(ge=1, le=100, description="Enter User ID", example=1)) -> str:
    if users.get(str(user_id)):
        return users.get(str(user_id))
    raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не найден")

# создание новой задачи
@app.post('/user/{username}/{age}')
async def create_user(username: str = Path(min_length=5, max_length=20, description="Enter username", example='UrbanUser'),
                      age: int = Path(ge=18, le=120, description="Enter age", example=24)) -> str:
    user_id = '1'
    if users:
        user_id = str(int(max(users, key=int)) + 1)
    users[user_id] = f"Имя: {username}, " + f"возраст: {age}"
    return f"User {user_id} has been registered"

# обновление данных
@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int  = Path(ge=1, le=100, description="Enter User ID", example=1),
                      username: str = Path(min_length=5, max_length=20, description="Enter username", example='NewUser'),
                      age: int = Path(ge=18, le=120, description="Enter age", example=24)) -> str:
    if users.get(str(user_id)):
        users[str(user_id)] = f"Имя: {username}, " + f"возраст: {age}"
        return f"The user {user_id} has been updated"
    raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не найден")

# запрос на удаление конкретного сообщения
@app.delete('/user/{user_id}')
async def delete_user(user_id: int = Path(ge=1, le=100, description="Enter User ID", example=1)) -> str:
    if users.get(str(user_id)):
        users.pop(str(user_id))
        return f"User {user_id} has been deleted."
    raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не найден")

# запрос на удаление всей БД
@app.delete('/users')
async def delete_all_users() -> str:
    users.clear()
    return f"All messages deleted."

