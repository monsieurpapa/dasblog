# DasBlog

A modern, extensible blog platform built with Django, Docker, and Bootstrap (Falcon theme). Features include user authentication, internationalization, analytics, newsletter, comments, and a beautiful, responsive UI.

---

## 🚀 Features
- Modern, responsive blog UI (Falcon-based)
- User registration, login, profile management
- Comments, categories, tags, newsletter
- Analytics dashboard (admin only)
- Internationalization (i18n) with English, French, and Spanish
- Dockerized for easy local development and deployment
- Makefile for all common operations
- Static/media file management
- Comprehensive test suite

---

## 🛠️ Tech Stack
- Python 3.11+
- Django 4.x
- Bootstrap 5 (Falcon theme)
- Docker & Docker Compose
- SQLite (default, easily swappable)
- Celery (for async tasks)
- django-allauth (authentication)
- django-widget-tweaks, tinymce, etc.

---

## ⚡ Quickstart (Docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/monsieurpapa/dasblog.git
   cd dasblog
   ```
2. **Build and start the containers:**
   ```bash
   make docker-build
   make docker-up
   ```
3. **Apply migrations and create a superuser:**
   ```bash
   make migrate
   make createsuperuser
   ```
4. **Collect static files:**
   ```bash
   make collectstatic
   ```
5. **Access the app:**
   - Main app: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

---

## 🧑‍💻 Local Development (without Docker)
1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations, create a superuser, and start the server:
   ```bash
   make migrate
   make createsuperuser
   make run
   ```

---

## 🗂️ Project Structure
```
dasblog/
  docker/           # Dockerfiles and configs
  src/              # Django project root
    config/         # Django settings, URLs, WSGI/ASGI
    core/           # Main app: models, views, forms, admin, etc.
    templates/      # All HTML templates (Falcon-based)
    static/         # Static files (CSS, JS, images)
    media/          # Uploaded media files
    locale/         # Translation files (.po/.mo)
    manage.py       # Django entry point
  requirements.txt  # Python dependencies
  Makefile          # Project automation
  docker-compose.yml
```

---

## 📝 Makefile Usage
All common operations are available via `make`:

- `make docker-build`        # Build Docker images
- `make docker-up`           # Start containers
- `make docker-down`         # Stop containers
- `make docker-logs`         # View logs
- `make docker-bash`         # Bash shell in Django container
- `make migrate`             # Run migrations
- `make createsuperuser`     # Create admin user
- `make test`                # Run tests
- `make lint`                # Lint code
- `make makemessages`        # Extract translation strings
- `make compilemessages`     # Compile translation files
- `make collectstatic`       # Collect static files
- `make clean`               # Remove .pyc/__pycache__

---

## 🌍 Internationalization (i18n)
- Supported languages: English, French, Spanish
- To add/update translations:
  ```bash
  make makemessages
  # Edit .po files in src/locale/
  make compilemessages
  ```
- Language can be switched via the UI or `/i18n/setlang/` endpoint.

---

## 🛡️ Deployment
- Production deployment is Docker-based. Customize `docker-compose.yml` and `docker/django/Dockerfile` as needed.
- Set environment variables for secrets and production settings.
- Use `make collectstatic` and `make migrate` before going live.
- For custom deployment steps, edit the `deploy` target in the Makefile.

---

## 🧪 Testing & Quality
- Run all tests: `make test`
- Lint code: `make lint`
- Coverage and CI integration recommended for production

---

## 🤝 Contributing
- Fork the repo and create a feature branch
- Write clear, well-documented code and tests
- Follow PEP8 and Django best practices
- Submit a pull request with a clear description

---

## 📄 License
[MIT License](LICENSE)

---

## 📬 Contact & Support
- Use the GitHub issue tracker for bugs and feature requests
- For questions, open an issue or contact the maintainers
- Project repo: https://github.com/monsieurpapa/dasblog 