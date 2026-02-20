import schedule
import time
import sys
from .pipeline import ContentPipeline
from ..core.utils import setup_logging

logger = setup_logging(__name__)

class DailyScheduler:
    def __init__(self, run_time: str = "09:00"):
        self.run_time = run_time
        self.pipeline = ContentPipeline()

    def job(self):
        logger.info("Starting scheduled daily run...")
        try:
            self.pipeline.run()
            logger.info("Daily run completed successfully.")
        except Exception as e:
            logger.error(f"Scheduled run failed: {e}")

    def start(self):
        logger.info(f"Scheduling daily run for {self.run_time}")
        schedule.every().day.at(self.run_time).do(self.job)
        
        logger.info("Executing immediate initial run...")
        self.job()

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user.")
            sys.exit(0)

if __name__ == "__main__":
    scheduler = DailyScheduler()
    scheduler.start()
