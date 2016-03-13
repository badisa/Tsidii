from tsidii.parser import HTMLParser
from tsidii.reader import ReaderCollection


class TsidiiEmail(object):

    def __init__(self, body, recipients, parser=None):
        if not isinstance(body, str):
            raise ValueError("Email body must be a string")
        if not isinstance(recipients, ReaderCollection):
            raise ValueError("Recipients must be an instance of ReaderCollection")
        self.body = body
        self.recipients = recipients
        if parser is None:
            parser = HTMLParser()
        self.parser = parser

    def reader_emails(self):
        for reader in self.recipients:
            yield reader, self.parser.parse_reader_email(self.body, reader)
