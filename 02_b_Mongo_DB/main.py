from fastapi import APIRouter,FastAPI, Depends,HTTPException
from router import posts,users,authentication


app = FastAPI()



app.include_router(authentication.router)
app.include_router(posts.router)
app.include_router(users.router)



