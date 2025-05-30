from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import users, articles, tag, articletag, comment, collector

app = FastAPI()

allowed_origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(comment.router, prefix="/api/v1", tags=["Comments"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(articles.router, prefix="/api/v1", tags=["Articles"])
app.include_router(tag.router, prefix="/api/v1", tags=["Tags"])
app.include_router(articletag.router, prefix="/api/v1", tags=["ArticleTags"])
app.include_router(collector.router, prefix="/api/v1", tags=["Collector"])

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
