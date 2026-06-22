from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Topic


def list_topics(db: Session) -> list[Topic]:
    return db.query(Topic).order_by(Topic.created_at.desc()).all()


def get_topic(db: Session, topic_id: int) -> Topic | None:
    return db.query(Topic).filter(Topic.id == topic_id).first()


def create_topic(db: Session, title: str, theory: str, prompt: str) -> Topic:
    topic = Topic(
        title=title,
        theory=theory or None,
        prompt=prompt or None,
        created_at=datetime.utcnow(),
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def update_topic(
    db: Session,
    topic_id: int,
    title: str,
    theory: str,
    prompt: str,
) -> Topic | None:
    topic = get_topic(db, topic_id)
    if topic is None:
        return None
    topic.title = title
    topic.theory = theory or None
    topic.prompt = prompt or None
    db.commit()
    db.refresh(topic)
    return topic
