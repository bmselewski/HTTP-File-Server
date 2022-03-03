# You need to implement the "get" and "head" functions.
from pathlib import Path
import mimetypes
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import os

class FileReader:

    def __init__(self):
        pass

    def get(self, filepath, cookies):
        """
        Returns a binary string of the file contents, or None.
        """

        if Path(filepath).is_dir():
            display = '<html><body><h1>' + filepath + '</h1></body></html>'
            print(filepath)
            return display.encode()

        x = open(filepath, "rb")
        display = x.read()
        x.close()
        return display

    def head(self, filepath, cookies):
        """
        Returns the size to be returned, or None.
        """
        size = os.path.getsize(filepath)
        if Path(filepath).is_dir():
            string = '<html><body><h1>' + filepath + '</h1></body></html>'
            size = len(string)
        now = datetime.now()
        stamp = mktime(now.timetuple())
        date = format_date_time(stamp)
        mimetype = mimetypes.guess_type(filepath, strict=True)
        mime = str(mimetype).split(',')[0]
        mime = mime[2:len(mime) - 1]
        if '.' not in filepath:
            mime = 'text/html'

        response = 'HTTP/1.1 200 OK\r\n'+'Date: '+ date+'\r\nContent-Type: ' + mime + '\r\nContent-Language: en '+ '\r\nContent-Length: '+ str(size)+'\n\n'
        return response
