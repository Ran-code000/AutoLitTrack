import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from ..database.crud import save_paper
from ..database.config import get_db
from .arxiv import ArxivCrawler

# Custom filter to add separator after each log
class SeparatorFilter(logging.Filter):
    def filter(self, record):
        record.msg = f"{record.msg}\n{'-' * 50}"
        return True

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.addFilter(SeparatorFilter())
logger.addHandler(handler)

class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=timezone("Asia/Shanghai"))
        self.crawler = ArxivCrawler(max_results=5)

    def schedule_tasks(self):
        """Schedule periodic tasks."""
        # Daily task: Fetch papers at 2:00 AM
        self.scheduler.add_job(
            self.fetch_and_save_papers,
            trigger="interval",
            seconds=10,  
            # trigger=CronTrigger(hour=2, minute=0),
            id="daily_fetch_papers",
            replace_existing=True,
            kwargs={"keyword": "machine learning"}
        )
        logger.info("Scheduled daily paper fetch at 2:00 AM")

    async def fetch_and_save_papers(self, keyword: str):
        """Fetch papers from arXiv and save to database."""
        try:
            logger.info(f"Fetching papers for keyword: {keyword} at {datetime.now()}")
            papers = self.crawler.search_papers(keyword)
            db = next(get_db())
            saved_count = 0
            for paper in papers:
                saved_paper = save_paper(db, paper, keyword)
                saved_count += 1
                logger.info(f"Saved paper: {saved_paper.title}")
            logger.info(f"Completed: Saved {saved_count} papers")
        except Exception as e:
            logger.error(f"Error in fetch_and_save_papers: {e}")

    def start(self):
        """Start the scheduler."""
        self.schedule_tasks()
        self.scheduler.start()
        logger.info("Scheduler started")

    def shutdown(self):
        """Shutdown the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
    def get_status(self):
        """Return scheduler and job status."""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "next_run_time": str(job.next_run_time),
                "trigger": str(job.trigger)
            })
        return {
            "scheduler_running": self.scheduler.running,
            "jobs": jobs
        }