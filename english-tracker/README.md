# English Learning Tracker

Local single-user app for tracking English learning topics, theory, AI prompts, and (planned) exercise batches with spaced repetition.

## Current status

Implemented:

- SQLite database with Topic, Batch, and Review models
- Topic CRUD (list, create, view, edit)

Not yet implemented:

- Batch CRUD
- Practice view
- Spaced repetition (SRS)

## Tech stack

- Python
- FastAPI (server-rendered HTML only)
- Jinja2
- SQLAlchemy
- SQLite

## Setup

```bash
cd english-tracker
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/topics](http://127.0.0.1:8000/topics)

Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

The SQLite database is created automatically at `data/app.db` on first startup.

## Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/topics` | List topics |
| GET | `/topics/new` | New topic form |
| POST | `/topics/new` | Create topic |
| GET | `/topics/{id}` | Topic detail |
| GET | `/topics/{id}/edit` | Edit topic form |
| POST | `/topics/{id}/edit` | Update topic |
| GET | `/health` | Health check |

## Project structure

```
english-tracker/
├── app/
│   ├── main.py              # FastAPI app, DB init
│   ├── database.py          # Engine, session, get_db
│   ├── models.py            # Topic, Batch, Review
│   ├── routes/
│   │   └── topics.py        # Topic pages
│   ├── services/
│   │   └── topics.py        # Topic CRUD logic
│   ├── templates/
│   └── static/
├── data/                    # SQLite DB (gitignored)
├── requirements.txt
└── PROJECT.md               # Architecture notes
```

## Data model

**Topic** — learning unit (title, theory, prompt)

**Batch** — exercise group under a topic; SRS schedule lives here (planned)

**Review** — review history per batch (planned)

See [PROJECT.md](PROJECT.md) for full architecture and build order.
