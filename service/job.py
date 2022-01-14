import email.message
import os
import ssl
import smtplib
import subprocess
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from pathlib import Path

class Job:
    def __init__(self, id, file, skip_conversion):
        self.id = id
        self.file = file
        self.skip_conversion = skip_conversion

    def execute_job(self, db):
        print('Job ' + self.id + ' started.')
        if not self.skip_conversion:
            db.set_step(self.id, 'converting', 'started')
            try:
                book_file = self.convert_book()
                db.set_step(self.id, 'converting', 'done')
            except Exception as e:
                print(str(e))
                db.set_step(self.id, 'converting', 'error', str(e))
                return

        db.set_step(self.id, 'sending', 'started')
        try:
            book_file = self.convert_book()
            self.send_email(book_file)
        except Exception as e:
            db.set_step(self.id, 'sending', 'error', str(e))
            return
        db.set_step(self.id, 'sending', 'done')
        print('Job ' + self.id + ' completed.')

    def convert_book(self):
        new_name = Path(self.file).with_suffix('.azw').name
        completed = subprocess.run(['kindlegen', self.file, '-c2', '-o', new_name],
                capture_output=True, timeout=15*60)
        if completed.returncode == 0:
            return new_name
        else:
            raise Exception(completed.stdout.decode('utf-8') + '\n' + completed.stderr.decode('utf-8'))

    def send_email(self, book_file):
        port = os.environ['SMTP_PORT'] or (587 if os.environ['SMTP_SSL'] else 25)
        smtp = smtplib.SMTP(os.environ['SMTP_SERVER'], port=port, timeout=60)
        try:
            smtp.set_debuglevel(2)
            smtp.noop()
            if os.environ['SMTP_TLS']:
                context = ssl.create_default_context()
                smtp.starttls(context=context)
            if os.environ['SMTP_USER']:
                smtp.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
            msg = MIMEMultipart()
            msg['From'] = os.environ['EMAIL_FROM']
            msg['Date'] = formatdate(localtime=True)
            msg['To'] = os.environ['EMAIL_TO']
            msg['Subject'] = book_file
            msg.attach(MIMEText('The book is attached.'))
            msg.attach(self.create_attachment(book_file))
            smtp.send_message(msg)
        except Exception as e:
            print(str(e))
            raise e
        finally:
            smtp.quit()

    def create_attachment(self, book_file):
        part = MIMEBase('application', "octet-stream")
        with open(book_file, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename={}'.format(book_file))
        return part
