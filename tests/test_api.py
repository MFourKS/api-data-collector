import pytest

from collector.api import HttpClient, Posts, Users


class FakeClient(HttpClient):
    def __init__(self, data):
        self.data = data

    async def get(self, path):
        return self.data[path]


@pytest.mark.asyncio
async def test_users():
    client = FakeClient({
        "/users": [
            {"id": 1, "name": "Лев", "email": "lev@ex.com", "company": {"name": "Globex"}}
        ]
    })
    users = await Users(client).load()
    assert users[0].company == "Globex"
    assert users[0].name == "Лев"


@pytest.mark.asyncio
async def test_posts():
    client = FakeClient({"/posts": [{"userId": 3, "id": 10, "title": "T", "body": "B"}]})
    posts = await Posts(client).load()
    assert posts[0].user_id == 3
    assert posts[0].id == 10
