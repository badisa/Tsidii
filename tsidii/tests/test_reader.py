from unittest import TestCase

from tsidii.reader import ReaderCollection


class TestReaderCollection(TestCase):

    def test_invalid_first_name(self):
        readers = ReaderCollection()
        with self.assertRaises(ValueError):
            readers.add_reader(
                first_name="Gideon Something",
                email="gideon@example.com"
            )

    def test_invalid_last_name(self):
        readers = ReaderCollection()
        with self.assertRaises(ValueError):
            readers.add_reader(
                first_name="Gideon",
                last_name="'Lil' Gleeful",
                email="tentoftelepathy@example.com",
            )

    def test_invalid_email(self):
        readers = ReaderCollection()
        with self.assertRaises(ValueError):
            readers.add_reader(
                first_name="Gideon",
                email="tent of telepathy@example.com"
            )

    def test_invalid_group(self):
        readers = ReaderCollection()
        with self.assertRaises(TypeError):
            readers.add_reader(
                first_name="Gideon",
                last_name="Gleeful",
                email="tentoftelepathy@example.com",
                groups="tent-of-telepathy")

    def test_invalid_indentifier(self):
        readers = ReaderCollection()
        with self.assertRaises(ValueError):
            readers.add_reader(
                first_name="Gideon",
                last_name="Gleeful",
                email="tentoftelepathy@example.com",
                identifier="tent of telepathy"
            )

    def test_invalid_indentifier_type(self):
        readers = ReaderCollection()
        with self.assertRaises(TypeError):
            readers.add_reader(
                first_name="Gideon",
                last_name="Gleeful",
                email="tentoftelepathy@example.com",
                identifier=["tent", "of", "telepathy"]
            )

    def test_invalid_group_name(self):
        readers = ReaderCollection()
        with self.assertRaises(TypeError):
            readers.add_reader(
                first_name="Gideon",
                last_name="Gleeful",
                email="tentoftelepathy@example.com",
                identifier="gideon",
                groups=["tent of telepathy"]
            )

    def test_errors_duplicate_identifier(self):
        readers = ReaderCollection()
        readers.add_reader(
            first_name="Gideon",
            last_name="Gleeful",
            email="tentoftelepathy@example.com",
            identifier="gideon"
        )
        with self.assertRaises(ValueError):
            readers.add_reader(
                first_name="Bud",
                last_name="Gleeful",
                email="usedcardeals@example.com",
                identifier="gideon"
            )
        self.assertEqual(1, len(readers.readers))

    def test_errors_duplicate_identifier_group_conflict(self):
        readers = ReaderCollection()
        readers.add_reader(
            first_name="Gideon",
            last_name="Gleeful",
            email="tentoftelepathy@example.com",
            identifier="gideon"
        )
        with self.assertRaises(ValueError):
            readers.add_reader(
                first_name="Bud",
                last_name="Gleeful",
                email="usedcardeals@example.com",
                identifier="bud",
                groups=["gideon"]
            )
        self.assertEqual(1, len(readers.readers))

    def test_valid_indentifier(self):
        readers = ReaderCollection()
        readers.add_reader(
            first_name="Gideon",
            last_name="Gleeful",
            email="tentoftelepathy@example.com",
            identifier="gideon"
        )
        self.assertEqual(1, len(readers.readers))

    def test_reader_get_data(self):
        readers = ReaderCollection()
        readers.add_reader(
            first_name="Gideon",
            last_name="Gleeful",
            email="tentoftelepathy@example.com",
            identifier="gideon"
        )
        data = readers.readers[0].get_data()
        self.assertEqual("Gideon", data["firstName"])
        self.assertEqual("Gleeful", data["lastName"])
        self.assertEqual("tentoftelepathy@example.com", data["email"])
        self.assertEqual("gideon", data["identifier"])
        self.assertEqual([], data["groups"])

    def test_add_multiple_readers(self):
        readers = ReaderCollection()
        readers.add_reader(
            first_name="Gideon",
            last_name="Gleeful",
            email="tentoftelepathy@example.com",
            groups=["tent-of-telepathy"]
        )
        readers.add_reader(
            first_name="Bud",
            last_name="Gleeful",
            email="usedcardeals@example.com",
            identifier="buddy"
        )
        self.assertEqual(2, len(readers.readers))
