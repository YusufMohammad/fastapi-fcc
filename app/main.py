
from fastapi import FastAPI
from .database import engine, get_db
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origin = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
''' 
Similar to 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls', namespace='post')),
    path('account/', include('account.urls', namespace='account')),
]

in Django
'''


@app.get("/")
def root():
    return {"message": "Welcome to my api!!!"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {'data': posts}
