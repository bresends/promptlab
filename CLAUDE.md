# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a Flask web application for managing and rendering Jinja2 prompt templates. The core architecture consists of:

- **Flask App Factory Pattern**: `app.py` creates the Flask app with database and migration setup
- **Route Registration**: `router.py` centrally registers all routes from the routes/ directory
- **Prompt Management System**: `prompts/prompt_manager.py` handles discovery, parsing, and rendering of Jinja2 templates with frontmatter metadata
- **Template Organization**: Prompts are organized by category in subdirectories under `prompts/` (e.g., `prompts/youtube/`, `prompts/projects/`)
- **Database Models**: SQLAlchemy models in `models/` directory with Flask-Migrate for schema management
- **Frontend**: Jinja2 templates in `templates/` with TailwindCSS styling

## Key Components

**PromptManager Class**: Central system for template discovery and rendering. It automatically scans the prompts/ directory, extracts frontmatter metadata, identifies Jinja2 variables, and organizes templates by category.

**Route Structure**: Dynamic route handling allows nested prompt paths (e.g., `/youtube/compare_videos/`) to map directly to template files in the prompts/ directory structure.

## Development Commands

**Start Development Server**:
```bash
uv run main.py
```

**Database Migrations**:
```bash
uv run flask db migrate     # Generate migration file
uv run flask db upgrade     # Apply migrations
```

**CSS Build** (TailwindCSS):
```bash
npx @tailwindcss/cli -i static/css/input.css -o static/css/output.css --watch
```

## Environment Setup

Required environment variables:
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: PostgreSQL connection string

The application uses python-dotenv to load from `.env` file.

## Frontend Styling

- The app uses custom Prism.js CSS in /static/css/input.css instead of external Prism CSS libraries. All syntax highlighting styles are defined there and built with TailwindCSS.

## Git Workflow
Always follow the Conventional Commits specification for all commit messages. Write clear, concise, and descriptive messages that accurately summarize what was changed and why. Don't ever mention Claude Code on the messages.
The message 🤖 Generated with [Claude Code](https://claude.ai/code)  Co-Authored-By: Claude <noreply@anthropic.com>" if forbidden. Never use it.