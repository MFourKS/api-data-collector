import logging
from collections import defaultdict

from .models import UserReport

log = logging.getLogger(__name__)


def build_reports(users, posts):
    # по автору, чтобы не бегать по списку каждого пользователя
    by_user = defaultdict(list)
    for p in posts:
        by_user[p.user_id].append(p)

    reports = []
    for u in users:
        user_posts = by_user.get(u.id, [])
        if user_posts:
            avg_len = round(sum(len(p.body) for p in user_posts) / len(user_posts), 2)
        else:
            avg_len = 0.0

        reports.append(
            UserReport(
                user_id=u.id,
                name=u.name,
                email=u.email,
                company=u.company,
                posts_count=len(user_posts),
                average_post_length=avg_len,
                post_titles=[p.title for p in user_posts],
            )
        )

    log.info("готово отчётов: %d", len(reports))
    return reports
