from celery import Celery
import createCodeAndRegsImages as cc
import base64
import pandas as pd
import io
import urllib.parse

host = 'host'
port = 99999
password = 'password'

# URL encode the password
encoded_password = urllib.parse.quote(password)

# Initialize Celery
celery = Celery('celery_tasks',
                broker=f'redis://:{encoded_password}@{host}:{port}/0',
                backend=f'redis://:{encoded_password}@{host}:{port}/0')

@celery.task
def create_code_book_task(book_title, full_file_b64, now, docsdropdown, pagenumber):
    file_content = base64.b64decode(full_file_b64)

    # Reconstruct the ExcelFile object
    excel_file = io.BytesIO(file_content)

    try:
        all_errors, footer_error = cc.create_code_book(book_title, excel_file, now, docsdropdown, pagenumber)
        download_link = f"/download/saved_code/{book_title}.pdf"

        result = {
            'status': 'success',
            'download_link': download_link,
            'all_errors': all_errors,
            'footer_error': footer_error
        }
    except Exception as e:
        result =  {
            'status': 'failure',
            'error': str(e)
        }

    return result

