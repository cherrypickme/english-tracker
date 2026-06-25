from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import batches as batch_service
from app.services import topics as topic_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/topics", response_class=HTMLResponse)
def list_topics(request: Request, db: Session = Depends(get_db)):
    topics = topic_service.list_topics(db)
    return templates.TemplateResponse(
        request,
        "topics/list.html",
        {"topics": topics},
    )


@router.get("/topics/new", response_class=HTMLResponse)
def new_topic_form(request: Request):
    return templates.TemplateResponse(
        request,
        "topics/form.html",
        {"topic": None, "form_action": "/topics/new"},
    )


@router.post("/topics/new")
def create_topic(
    title: str = Form(...),
    theory: str = Form(""),
    prompt: str = Form(""),
    db: Session = Depends(get_db),
):
    topic = topic_service.create_topic(db, title, theory, prompt)
    return RedirectResponse(url=f"/topics/{topic.id}", status_code=303)


@router.get("/topics/{topic_id}", response_class=HTMLResponse)
def topic_detail(request: Request, topic_id: int, db: Session = Depends(get_db)):
    topic = topic_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    batches = batch_service.list_batches_for_topic(db, topic_id)
    return templates.TemplateResponse(
        request,
        "topics/detail.html",
        {"topic": topic, "batches": batches},
    )


@router.get("/topics/{topic_id}/edit", response_class=HTMLResponse)
def edit_topic_form(request: Request, topic_id: int, db: Session = Depends(get_db)):
    topic = topic_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return templates.TemplateResponse(
        request,
        "topics/form.html",
        {"topic": topic, "form_action": f"/topics/{topic_id}/edit"},
    )


@router.post("/topics/{topic_id}/edit")
def update_topic(
    topic_id: int,
    title: str = Form(...),
    theory: str = Form(""),
    prompt: str = Form(""),
    db: Session = Depends(get_db),
):
    topic = topic_service.update_topic(db, topic_id, title, theory, prompt)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return RedirectResponse(url=f"/topics/{topic.id}", status_code=303)
