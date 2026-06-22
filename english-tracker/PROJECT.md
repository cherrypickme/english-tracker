Goal

Local English learning tracker with spaced repetition.

System stores:

topics
learning batches
review schedule per batch
Core principle
No REST API layer
No authentication
No complex architecture
Single-user local app
SQLite only
Data model

Topic

id
title
theory
prompt
created_at

Batch

id
topic_id
name
content
status
created_at
next_review_date
interval_days
review_count

Review

id
batch_id
review_date
interval_days
Business rules
Review happens per Batch (not Topic)
Each batch has independent spaced repetition schedule
Topic is just container for batches
next_review_date determines what is due today
Tech stack
FastAPI (server-rendered HTML only)
Jinja2 templates
SQLAlchemy
SQLite
Forbidden (do not implement)
REST API
Pydantic schemas
authentication
repositories layer
microservices
complex service architecture
Allowed simplification

Business logic can be:

inside routes OR
small helpers in services/
Build order
database.py + models.py
topic CRUD
batch CRUD
practice view
spaced repetition logic