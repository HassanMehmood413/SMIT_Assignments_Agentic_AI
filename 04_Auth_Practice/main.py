from fastapi import FastAPI,Depends,HTTPException,status
from database import Base,engine
from routers import posts_routes,users_routes,authentication,votes_routes,message_route
import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_rout():
    return {'Hello World'}



app.include_router(authentication.router)
app.include_router(posts_routes.router)
app.include_router(users_routes.router)
app.include_router(votes_routes.router)
app.include_router(message_route.router)