from celery import Celery
import createCodeAndRegsImages as cc
import os
import base64
import pandas as pd
import io
import urllib.parse
import logging
from dotenv import load_dotenv
from celery.signals import after_setup_logger

load_dotenv()

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
password = os.getenv("REDIS_PASSWORD")

# URL encode the password
encoded_password = urllib.parse.quote(password)

# Initialize Celery
celery = Celery(
    "celery_tasks",
    broker=f"redis://:{encoded_password}@{host}:{port}/0",
    backend=f"redis://:{encoded_password}@{host}:{port}/0",
)
celery.conf.broker_connection_retry_on_startup = True


@after_setup_logger.connect
def setup_celery_logger(logger, *args, **kwargs):
    try:
        # Get the directory where your code is running
        current_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(current_dir, "celery_debug.log")

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh = logging.FileHandler(log_path)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info("Celery logging initialized successfully")
    except Exception as e:
        print(f"Failed to setup file logging: {str(e)}")
        print(f"Will log to stderr instead")


@celery.task(bind=True)
def create_code_book_task(
    self, book_title, full_file_b64, now, docsdropdown, pagenumber
):
    logger = logging.getLogger(__name__)
    logger.info(f"Task ID: {self.request.id} - Starting task for book: {book_title}")

    try:
        file_content = base64.b64decode(full_file_b64)
        logger.info("Successfully decoded base64 content")

        excel_file = io.BytesIO(file_content)

        xl = pd.ExcelFile(excel_file)
        MAX_ROWS = 250  # Adjust this number

        # Check first sheet
        df1 = xl.parse(0)  # First sheet
        df2 = xl.parse(1)  # Second sheet

        total_rows = len(df1) + len(df2)
        if total_rows > MAX_ROWS:
            logger.warning(
                f"File exceeds maximum allowed sections: {total_rows} > {MAX_ROWS}"
            )
            return {
                "status": "failure",
                "error": f"Your request contains {total_rows} sections total, Code and regulations combined. For performance reasons, please limit requests to {MAX_ROWS} sections at a time. If your class assigns more sections than that, consider breaking your request into multiple spreadsheets and uploading them separately.",
            }

        # Reset file pointer for main processing
        excel_file.seek(0)

        logger.info("Created BytesIO object")

        all_errors, footer_error = cc.create_code_book(
            book_title, excel_file, now, docsdropdown, pagenumber
        )
        logger.info("Code book created")

        download_link = f"/download/saved_code/{book_title}.pdf"
        result = {
            "status": "success",
            "download_link": download_link,
            "all_errors": all_errors,
            "footer_error": footer_error,
        }
        logger.info("Task completed successfully")

    except Exception as e:
        logger.error(f"Task failed with error: {str(e)}", exc_info=True)
        result = {"status": "failure", "error": str(e)}

    return result


def test_redis_connection():
    try:
        celery.backend.client.ping()
        return True
    except Exception as e:
        return str(e)


# If needed, additional Celery tasks can be added here
