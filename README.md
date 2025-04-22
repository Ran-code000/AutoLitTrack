# LitGenius Scheduler Module

The **Scheduler Module** is a core component of the **LitGenius** project, designed to automate the periodic retrieval and storage of academic papers from arXiv. Built with `APScheduler`, it schedules tasks to fetch papers based on specific keywords and saves them to a SQLite database for further processing and analysis. This module is integrated into the FastAPI backend, ensuring seamless operation within the LitGenius ecosystem.

## Table of Contents

- Features
- Architecture
- Installation
- Configuration
- Usage
- Testing
- Contributing
- License

## Features

- **Automated Paper Retrieval**: Fetches papers from arXiv using the `ArxivCrawler` based on specified keywords.
- **Scheduled Tasks**: Uses `APScheduler` to run tasks daily at 2:00 AM (Asia/Shanghai timezone) or at custom intervals for testing.
- **Database Integration**: Saves fetched papers to a SQLite database (`papers.db`) using SQLAlchemy.
- **Robust Logging**: Provides detailed logs for task execution, paper saving, and error handling.
- **Asynchronous Processing**: Leverages `asyncio` for efficient handling of I/O-bound operations.

## Architecture

The Scheduler Module is implemented in `backend/app/services/scheduler.py` and integrates with the following components:

- **ArxivCrawler**: A custom module (`backend/app/services/arxiv.py`) to query and retrieve papers from arXiv.
- **Database CRUD**: Functions in `backend/app/database/crud.py` to save papers to the SQLite database.
- **FastAPI Backend**: The scheduler is initialized and started in `backend/app/main.py` during application startup.
- **APScheduler**: An `AsyncIOScheduler` manages task scheduling and execution.

The module operates as follows:

1. Initializes an `AsyncIOScheduler` with the Asia/Shanghai timezone.
2. Schedules a daily task to fetch papers for the keyword `"machine learning"` at 2:00 AM.
3. Fetches papers using `ArxivCrawler` and saves them to the database via `save_paper`.
4. Logs task progress and errors for monitoring.

## Installation

### Prerequisites

- Python 3.12+
- Virtual environment (recommended)
- SQLite (included with Python)
- Git

### Steps

1. **Clone the LitGenius Repository**:

   ```bash
   git clone https://github.com/your-username/LitGenius.git
   cd LitGenius
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv backend/litgenius_venv
   source backend/litgenius_venv/Scripts/activate  # Windows
   # source backend/litgenius_venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r backend/requirements.txt
   ```

   Example `requirements.txt`:

   ```
   fastapi>=0.115.2
   uvicorn>=0.30.0
   sqlalchemy>=2.0
   pytest>=8.3.4
   requests>=2.32.0
   apscheduler>=3.10
   pytest-asyncio>=0.26.0
   ```

4. **Verify Installation**:

   ```bash
   python -m backend.app.services.scheduler
   ```

## Configuration

The Scheduler Module is configured in `backend/app/services/scheduler.py`. Key settings include:

- **Timezone**: `Asia/Shanghai` (modifiable in `Scheduler.__init__`).
- **Task Schedule**: Daily at 2:00 AM (configurable via `CronTrigger` in `schedule_tasks`).
- **Keyword**: Defaults to `"machine learning"` (adjustable in `schedule_tasks`).
- **Max Results**: Limits to 5 papers per fetch (set in `ArxivCrawler`).

To modify the schedule for testing (e.g., every 10 seconds):

1. Edit `backend/app/services/scheduler.py`:

   ```python
   self.scheduler.add_job(
       self.fetch_and_save_papers,
       trigger="interval",
       seconds=10,
       id="daily_fetch_papers",
       replace_existing=True,
       kwargs={"keyword": "machine learning"}
   )
   ```

2. Revert to `CronTrigger(hour=2, minute=0)` for production.

## Usage

### Running the Scheduler

The scheduler is automatically started with the FastAPI application:

```bash
cd backend
uvicorn app.main:app --reload
```

**Expected Output**:

```
INFO:     Started server process [13960]
INFO:     Waiting for application startup.
2025-04-22 16:30:55,464 - backend.app.services.scheduler - INFO - Scheduled daily paper fetch at 2:00 AM
2025-04-22 16:30:55,466 - backend.app.services.scheduler - INFO - Scheduler started
INFO:     Application startup complete.
2025-04-22 16:31:05,469 - backend.app.services.scheduler - INFO - Fetching papers for keyword: machine learning at 2025-04-22 16:31:05.469117
2025-04-22 16:31:07,222 - backend.app.services.scheduler - INFO - Saved paper: Lecture Notes: Optimization for Machine Learning
...
2025-04-22 16:31:07,240 - backend.app.services.scheduler - INFO - Completed: Saved 5 papers
```

### Manual Task Trigger

To manually trigger a task:

1. Modify `schedule_tasks` to use an interval trigger (e.g., every 10 seconds, as shown above).

2. Run the application:

   ```bash
   uvicorn backend.app.main:app --reload
   ```

3. Check logs for paper fetching and saving every 10 seconds.

### Database Inspection

Verify saved papers in the SQLite database:

```bash
sqlite3 backend/papers.db
sqlite> SELECT * FROM papers;
```

### API Integration

The saved papers can be queried via the FastAPI endpoint:

```bash
curl "http://localhost:8000/search?keyword=machine%20learning"
```


## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request to the `master` branch.

Please ensure:

- Tests pass (`pytest test_backend/unit -v`).
- Code follows PEP 8 style guidelines.
- New features include documentation and tests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**LitGenius Team**\
*Automating Academic Discovery*\
GitHub Repository
