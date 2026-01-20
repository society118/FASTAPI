from pydantic import BaseModel,Field,EmailStr,ConfigDict
from fastapi import FastAPI
import uvicorn
app =FastAPI()

data ={
    "email":"abcd123@mail.com",
    "bio":"hello",
    "age":12,
}

data_wo_age ={
    "email":"abcd123@mail.com",
    "bio":"hello",
    "gender":"male",
    "birthday":"2022",
}

class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None =Field(max_length=10)

users =[]

@app.post("/users/")
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "msg": "Юзер добавлен"}

@app.get("/users/")
def get_user() -> list[UserSchema]:
    return users

class UserAgeSchema(UserSchema):
    age: int =Field(ge=0,le=130)

def func(data_:dict):
    data_["age"] += 1

print(repr(UserSchema(**data_wo_age)))

if __name__ =='__main__':
    uvicorn.run("schemas:app",reload=True,port=5051)
