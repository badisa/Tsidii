
from bs4 import BeautifulSoup

from tsidii.reader import ReaderCollection


class HTMLParser(object):
    # Should inherit from abstract base class to allow for easy modification

    def __init__(self, note_tag="note"):
        self.note_tag = note_tag
        self.message_tag = "message"
        self.hidden_tag = "hidden"
        self.private_tag = "private"

    def parse_reader_email(self, body, reader):
        if not isinstance(body, str):
            raise ValueError(
                "Body must be a string, not a '{}'".format(type(body))
            )
        if not isinstance(reader, ReaderCollection.TsidiiReader):
            raise ValueError(
                "Reader must be an instance of TsidiiReader"
            )
        soup = BeautifulSoup(body)
        note_tags = soup.findAll(self.note_tag)
        pm = False
        if note_tags is not None:
            for tag in note_tags:
                if not tag.attrs:
                    tag.decompose()
                    continue
                if tag.get(self.hidden_tag) and not self._check_user_flag_in_tag(reader, tag.get(self.hidden_tag)):
                    # Unwrap tag if user flag is not in in hidden attributes
                    tag.unwrap()
                elif self._check_user_flag_in_tag(reader, tag.get(self.private_tag)):
                    # Append Name then unwrap tag
                    tag.insert_before(
                        " {} - ".format(reader.first_name.title())
                    )
                    tag.unwrap()
                    pm = True
                elif self._check_user_flag_in_tag(reader, tag.get(self.message_tag)):
                    # Unwrap tag if user is flagged in the tag
                    tag.unwrap()
                else:
                    tag.decompose()
        soup = str(soup)
        return (soup, pm)

    def _check_user_flag_in_tag(self, reader, tag_attributes):
        if not tag_attributes:
            return False
        if reader.identifier in tag_attributes:
            return True
        return any((group in tag_attributes for group in reader.groups))
