from unittest import TestCase

from tsidii.reader import ReaderCollection
from tsidii.parser import HTMLParser


class TestHTMLParser(TestCase):

    def test_body_type(self):
        parser = HTMLParser()
        readers = ReaderCollection()
        readers.add_reader(
            first_name="Dipper",
            last_name="Pines",
            email="dipper@example.com",
            identifier="dippy",
            groups=["pinesfamily", "mysterytwins"]

        )
        with self.assertRaises(ValueError):
            parser.parse_reader_email(["invalid", "body"], readers.readers[0])

    def test_reader_type(self):
        parser = HTMLParser()

        with self.assertRaises(ValueError):
            parser.parse_reader_email("Valid email body", ["invalid", "reader", "obj"])
