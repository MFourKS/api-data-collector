from collector.models import Post, User
from collector.report import build_reports


def user(uid):
    return User(uid, f"User {uid}", f"u{uid}@ex.com", "Acme")


def test_count_and_avg():
    posts = [
        Post(1, 1, "A", "12345"),    # 5
        Post(1, 2, "B", "1234567"),  # 7
    ]
    r = build_reports([user(1)], posts)[0]
    assert r.posts_count == 2
    assert r.average_post_length == 6.0
    assert r.post_titles == ["A", "B"]


def test_no_posts():
    r = build_reports([user(2)], [])[0]
    assert r.posts_count == 0
    assert r.average_post_length == 0.0
    assert r.post_titles == []


def test_other_users_posts_skipped():
    r = build_reports([user(1)], [Post(99, 1, "X", "aaa")])[0]
    assert r.posts_count == 0
