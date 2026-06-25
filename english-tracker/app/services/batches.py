from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Batch


def list_batches_for_topic(db: Session, topic_id: int) -> list[Batch]:
    return (
        db.query(Batch)
        .filter(Batch.topic_id == topic_id)
        .order_by(Batch.created_at.desc())
        .all()
    )


def get_batch(db: Session, batch_id: int) -> Batch | None:
    return db.query(Batch).filter(Batch.id == batch_id).first()


def get_batch_for_topic(db: Session, topic_id: int, batch_id: int) -> Batch | None:
    return (
        db.query(Batch)
        .filter(Batch.id == batch_id, Batch.topic_id == topic_id)
        .first()
    )


def create_batch(
    db: Session,
    topic_id: int,
    name: str,
    content: str,
    status: str,
) -> Batch:
    batch = Batch(
        topic_id=topic_id,
        name=name,
        content=content or None,
        status=status,
        created_at=datetime.utcnow(),
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def update_batch(
    db: Session,
    topic_id: int,
    batch_id: int,
    name: str,
    content: str,
    status: str,
) -> Batch | None:
    batch = get_batch_for_topic(db, topic_id, batch_id)
    if batch is None:
        return None
    batch.name = name
    batch.content = content or None
    batch.status = status
    db.commit()
    db.refresh(batch)
    return batch
