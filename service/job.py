import subprocess
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
        pass
