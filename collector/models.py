from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str
    company: str

    @classmethod
    def from_json(cls, data):
        # company лежит вложенным объектом
        company = data.get("company") or {}
        return cls(
            id=data["id"],
            name=data.get("name", ""),
            email=data.get("email", ""),
            company=company.get("name", ""),
        )


@dataclass
class Post:
    user_id: int
    id: int
    title: str
    body: str

    @classmethod
    def from_json(cls, data):
        return cls(
            user_id=data["userId"],
            id=data["id"],
            title=data.get("title", ""),
            body=data.get("body", ""),
        )


@dataclass
class UserReport:
    user_id: int
    name: str
    email: str
    company: str
    posts_count: int
    average_post_length: float
    post_titles: list[str]

    def as_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "company": self.company,
            "posts_count": self.posts_count,
            "average_post_length": self.average_post_length,
            "post_titles": self.post_titles,
        }
