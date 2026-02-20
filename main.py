import sys
import argparse
import webbrowser
from pathlib import Path
from src.orchestration.pipeline import ContentPipeline
from src.orchestration.scheduler import DailyScheduler
from src.core.utils import setup_logging

logger = setup_logging(__name__)

def main():
    parser = argparse.ArgumentParser(description="MadeInTracker AI Content Generator")
    parser.add_argument("--schedule", action="store_true", help="Run in daily scheduler mode")
    parser.add_argument("--time", type=str, default="09:00", help="Time to run daily (HH:MM)")
    args = parser.parse_args()

    try:
        if args.schedule:
            scheduler = DailyScheduler(run_time=args.time)
            scheduler.start()
        else:
            pipeline = ContentPipeline()
            output_folder = pipeline.run()
            
            if output_folder:
                preview_path = (output_folder / "preview.html").absolute()
                logger.info(f"Opening preview: {preview_path}")
                webbrowser.open(f"file:///{preview_path}")
            else:
                logger.warning("Pipeline finished but no content was generated.")
            
    except KeyboardInterrupt:
        logger.info("Stopped by user.")
    except Exception as e:
        logger.critical(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
