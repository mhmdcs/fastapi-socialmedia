from fastapi.testclient import TestClient
from app.main import app
from app.oauth2 import create_access_token
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from alembic import command
from starlette.datastructures import MutableHeaders
import pytest

DATABASE_CONNECTION_STRING = "postgresql://postgres:password@localhost:5432/fastapi-socialmedia-test"

engine = create_engine(DATABASE_CONNECTION_STRING)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# creating and dropping db tables via alembic instead of sqlalchemy:
# @pytest.fixture
# def client():
#     command.upgrade("head")
#     yield TestClient(app)
#     command.downgrade("base")

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@test.com", "password": "test"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@test.com", "password": "test"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_posts(test_user, test_user2, session):
    postsDict = [
        {"title": "first title",
         "content": "first content",
         "owner_id": test_user['id']},
        {"title": "second title",
         "content": "second content",
         "owner_id": test_user['id']},
        {"title": "third title",
         "content": "third content",
         "owner_id": test_user['id']},
        {"title": "fourth title",
         "content": "fourth content",
         "owner_id": test_user2['id']}
    ]
    
    def create_post_model(post):
        return models.Post(**post)
        
    postsModel = map(create_post_model, postsDict)
    postList = list(postsModel)
    session.add_all(postList)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                  models.Post(title="second title", content="second content", owner_id=test_user['id']),
    #                  models.Post(title="third title", content="third content", owner_id=test_user['id'])])
    session.commit()
    posts = session.query(models.Post).all()
    return posts

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    # new_header = MutableHeaders(client._headers)
    # new_header["Authorization"]=f"Bearer {token}"
    # client._headers = new_header
    return client