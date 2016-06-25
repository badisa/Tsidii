from bs4 import BeautifulSoup

from tsidii.reader import TsidiiReader


class HTMLParser(object):
    # Should inherit from abstract base class to allow for easy modification

    def __init__(self, note_tag="note"):
        self.note_tag = note_tag
        self.message_tag = "message"
        self.hidden_tag = "hidden"
        self.private_tag = "private"

    def parse_reader_email(self, body, reader):
        '''
            Parses a body that has HTML in it that matches up with the format
            specified (undocumented currently) for Tsidii Emails.

            :param string body: The message to be parsed
            :param TsidiiReader reader: TsidiiReader Instance to parse message with
            :return tuple: The parsed message as well as flag indicating private message
        '''
        if not isinstance(body, str):
            raise ValueError(
                "Body must be a string, not a '{}'".format(type(body))
            )
        if not isinstance(reader, TsidiiReader):
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
                if tag.get(self.hidden_tag) and not self._user_flag_in_tag(reader, tag.get(self.hidden_tag)):
                    # Unwrap tag if user flag is not in in hidden attributes
                    tag.unwrap()
                elif self._user_flag_in_tag(reader, tag.get(self.private_tag)):
                    # Append Name then unwrap tag
                    tag.insert_before(
                        " {} - ".format(reader.first_name.title())
                    )
                    tag.unwrap()
                    pm = True
                elif self._user_flag_in_tag(reader, tag.get(self.message_tag)):
                    # Unwrap tag if user is flagged in the tag
                    tag.unwrap()
                else:
                    tag.decompose()
        soup = str(soup)
        return (soup, pm)

    def _user_flag_in_tag(self, reader, tag_attrs):
        if not tag_attrs:
            return False
        if reader.identifier in tag_attrs:
            return True
        return any((group in tag_attrs for group in reader.groups))
