from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")
    
    # def validate(post):
    #     return schemas.PostResponse(**post)
    # posts_map = map(validate, res.json())
    # posts_list = list(posts_map)
    
    # assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401
    
def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_get_one_nonexistent_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/543")
    assert res.status_code == 404
    
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content
    assert post.title == test_posts[0].title
    
@pytest.mark.parametrize("title, content, published", [
    ("tests!", "writing some tests!", True),
    ("testing yet another title", "another content test", False),
    ("another title test", "another content tests", False),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts", json={"title": title, "content": content, "published": published})
    assert res.status_code == 201
    created_post = schemas.PostResponse(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    
    
def test_create_post_with_default_published(authorized_client):
    res = authorized_client.post("/posts", json={"title": "some placeholder title", "content": "some placeholder content"})
    created_post = schemas.PostResponse(**res.json())
    assert created_post.published == True
    assert res.status_code == 201
    
def test_unauthorized_user_create_post(client):
    res = client.post("/posts", json={"title": "some placeholder title", "content": "some placeholder content"})
    assert res.status_code == 401
    
def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    
def test_delete_nonexistent_post(authorized_client, test_posts):
    res = authorized_client.delete("/posts/73452")
    assert res.status_code == 404
    
def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    
def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/8000000", json=data)
    assert res.status_code == 404