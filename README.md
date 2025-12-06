# SK Tutorials – Tutorial Website 🧩

Multi‑concept tutorial web application where an admin can create and organize rich‑text tutorials using the Django admin, and publish them as a clean, structured learning site. Users simply browse and read; all content and structure are managed from the backend.

> Built as a reusable base for anyone who wants to host their own tutorial / notes / documentation website without touching HTML for every page.

---

## Overview

SK Tutorials is a stable, production‑ready Django application for publishing tutorials grouped into concepts, topics, and subtitles.  
It focuses on giving the admin a powerful content model (with ordering, drafts, and rich text) while keeping the reading experience simple for end users.

---

## Tech stack

- **Language:** Python 3.11.9  
- **Framework:** Django 5.2.1  
- **Database (prod):** PostgreSQL (Supabase)  
- **Database (local):** SQLite or PostgreSQL (configurable via environment variables)  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap  
- **Rich text editor:** `django-ckeditor-5`  
- **Containerization:** Docker  
- **Hosting (example):** Render (Django app container) + Supabase (managed Postgres)

---

## Core features

- Multi‑level tutorial structure:
  - **Concepts** → **Topics** → **Subtitles** with explicit ordering.
- Full content management from Django admin:
  - Create, edit, reorder, and delete tutorials with no code changes.
- Draft / publish workflow:
  - Per‑item `draft` flag to hide content from the live site until ready.
- SEO‑friendly slugs:
  - Auto‑generated unique slugs for concepts, topics, and subtitles.
- Rich‑text content:
  - CKEditor 5 with configurable toolbar for topics and subtitles.
- Stable, deployment‑ready configuration:
  - Works both with virtualenv and with Docker; DB can be local or remote.

---

## Data model

### Concept

Represents a high‑level subject (e.g., “Python Basics”, “Django ORM”).

- `title` – Concept name.  
- `tagline` – Optional short description/tagline.  
- `slug` – Unique slug; auto‑generated from title on save if left blank.  
- `draft` – Controls whether the concept appears on the live site.  
- `created_at`, `updated_at` – Timestamps.

Relationships:

- One `Concept` has many `Topic` objects (via `topics` related name).

### Topic

Represents an ordered topic within a concept (e.g., “Variables”, “Views”).

- `concept` – Foreign key to `Concept` (cascade on delete).  
- `order` – Positive integer controlling display order within a concept.  
- `title` – Topic title.  
- `slug` – Unique slug; auto‑generated from title if blank.  
- `content` – Rich text content field using `CKEditor5Field`.  
- `draft` – Hide/show topic on live site.  
- `created_at`, `updated_at` – Timestamps.

Meta:

- `ordering = ['order']` to ensure topics appear in the defined order.

Relationships:

- One `Topic` has many `Subtitle` objects (via `subtitles` related name).

### Subtitle

Represents a subsection of a topic (e.g., “Examples”, “Pitfalls”).

- `topic` – Foreign key to `Topic` (cascade on delete).  
- `order` – Positive integer controlling display order within the topic.  
- `title` – Subtitle title.  
- `slug` – Unique slug; auto‑generated from title if blank.  
- `content` – Rich text content field using `CKEditor5Field`.  
- `draft` – Hide/show on live site.  
- `created_at`, `updated_at` – Timestamps.

Meta:

- `ordering = ['order']`  
- `unique_together = ['topic', 'slug']` to keep slugs unique within a topic.

---

## Roles and user flows

### Admin / Staff

- Log in to the Django admin.
- Create a **Concept** with title, tagline, and draft flag.
- Within a concept, create ordered **Topics** and optionally **Subtitles**:
  - Set `order` to control display sequence.
  - Use CKEditor to write and format tutorial content.
- Toggle `draft` to control what appears on the live site.
- Update or delete content at any time; changes are reflected immediately.

### Visitor / Reader

- Browse available concepts (only non‑draft items).
- Navigate topics and subtitles in the defined order.
- Read tutorials in a clean, content‑focused layout (no login required).

---

## Project structure (simplified)

tutorial-website/
├─ manage.py
├─ project_root/
│ ├─ settings.py
│ ├─ urls.py
│ └─ wsgi.py / asgi.py
├─ tutorials/ # App containing Concept, Topic, Subtitle models
│ ├─ models.py
│ ├─ admin.py
│ ├─ views.py
│ ├─ urls.py
│ └─ templates/
└─ Dockerfile


> Note: Adjust this tree to match your actual app and folder names.

---

## Running locally with virtualenv

1. **Clone the repository**

git clone https://github.com/SaikiranNalla/Tutorial-Website

cd MyProject

text

2. **Create and activate a virtual environment**

python -m venv venv

To Activate venv:

source venv/bin/activate # On Windows: venv\Scripts\activate

3. **Install dependencies**

pip install -r requirements.txt


4. **Configure environment**

- Copy the example env file (if present) or create `.env` and set e.g.:
  - `SECRET_KEY=<your-secret-key>`
  - `DEBUG=True`
  - `DATABASE_URL=<your-db-url>` (optional; SQLite by default if not set)
  - Any config needed by `django-ckeditor-5`.

5. **Apply migrations**

python manage.py migrate

text

6. **Create a superuser**

python manage.py createsuperuser

text

7. **Run the development server**

python manage.py runserver

text

Visit http://127.0.0.1:8000/ for the site and http://127.0.0.1:8000/admin/ for the admin.

---

## Running with Docker

1. **Build the image**

docker build -t sk-tutorials .

text

2. **Run the container**

Example using environment variables (Postgres local or remote):

docker run --env-file .env -p 8000:8000 sk-tutorials

text

- Point `DATABASE_URL` or separate `DB_*` env vars to:
  - Local PostgreSQL, or
  - Remote Postgres (e.g., Supabase connection string).

3. **Database migrations from container**

If needed, run:

docker exec -it <container-name> python manage.py migrate
docker exec -it <container-name> python manage.py createsuperuser

text

> For deployment, the same container image can be used on Render with Supabase as the database.

---

## Configuration and database options

- **Local dev:**
- SQLite is easiest; no external service required.
- **PostgreSQL:**
- Recommended for production; tested with Supabase as a managed Postgres instance.
- All DB configuration is environment‑driven so you can swap between SQLite and Postgres without code changes.

---

## Testing

- Manual functional testing of core flows:
- Admin creates concepts, topics, and subtitles.
- Draft vs published content visibility.
- Ordering of topics and subtitles.
- (Optional next steps) Add automated tests with `pytest` or `manage.py test` for:
- Model behaviors (slug generation, ordering, draft filtering).
- Views/templates for public and admin flows.

---

## What I worked on / learned

- Designed the **content hierarchy** (Concept → Topic → Subtitle) and database schema with slugs, unique constraints, and ordering fields.  
- Implemented a **draft/publish workflow** that keeps incomplete content hidden from users while remaining editable in admin.  
- Integrated **CKEditor 5** into Django models and admin for rich‑text editing.  
- Containerized the project with **Docker** and deployed it to **Render** using **Supabase PostgreSQL** as the database backend.  

[//]: # (- Practiced environment‑based configuration so the same code runs with SQLite locally and Postgres in production.)

---

## Roadmap / possible improvements

- Add search and filtering across concepts/topics.  
- Add public API endpoints (e.g., `/api/concepts/`, `/api/topics/`) for headless or SPA clients.  
- Implement automated tests and CI pipeline (GitHub Actions).  
- Add user accounts for bookmarking / tracking progress.

---

## License

[//]: # (Specify your license here &#40;e.g., MIT&#41; and add a `LICENSE` file in the repository.)