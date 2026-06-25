from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import batches as batch_service
from app.services import topics as topic_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

BATCH_STATUSES = ("draft", "active", "archived")


@router.get("/topics/{topic_id}/batches/new", response_class=HTMLResponse)
def new_batch_form(request: Request, topic_id: int, db: Session = Depends(get_db)):
    topic = topic_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return templates.TemplateResponse(
        request,
        "batches/form.html",
        {
            "topic": topic,
            "batch": None,
            "form_action": f"/topics/{topic_id}/batches/new",
            "statuses": BATCH_STATUSES,
        },
    )


@router.post("/topics/{topic_id}/batches/new")
def create_batch(
    topic_id: int,
    name: str = Form(...),
    content: str = Form(""),
    status: str = Form("draft"),
    db: Session = Depends(get_db),
):
    topic = topic_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    batch = batch_service.create_batch(db, topic_id, name, content, status)
    return RedirectResponse(
        url=f"/topics/{topic_id}/batches/{batch.id}",
        status_code=303,
    )


@router.get("/topics/{topic_id}/batches/{batch_id}", response_class=HTMLResponse)
def batch_detail(
    request: Request,
    topic_id: int,
    batch_id: int,
    db: Session = Depends(get_db),
):
    topic = topic_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    batch = batch_service.get_batch_for_topic(db, topic_id, batch_id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return templates.TemplateResponse(
        request,
        "batches/detail.html",
        {"topic": topic, "batch": batch},
    )


@router.get("/topics/{topic_id}/batches/{batch_id}/edit", response_class=HTMLResponse)
def edit_batch_form(
    request: Request,
    topic_id: int,
    batch_id: int,
    db: Session = Depends(get_db),
):
    topic = topic_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    batch = batch_service.get_batch_for_topic(db, topic_id, batch_id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return templates.TemplateResponse(
        request,
        "batches/form.html",
        {
            "topic": topic,
            "batch": batch,
            "form_action": f"/topics/{topic_id}/batches/{batch_id}/edit",
            "statuses": BATCH_STATUSES,
        },
    )


@router.post("/topics/{topic_id}/batches/{batch_id}/edit")
def update_batch(
    topic_id: int,
    batch_id: int,
    name: str = Form(...),
    content: str = Form(""),
    status: str = Form("draft"),
    db: Session = Depends(get_db),
):
    batch = batch_service.update_batch(db, topic_id, batch_id, name, content, status)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return RedirectResponse(
        url=f"/topics/{topic_id}/batches/{batch.id}",
        status_code=303,
    )
