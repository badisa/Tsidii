from unittest import TestCase

from tsidii.email import TsidiiEmail
from tsidii.reader import ReaderCollection


class TestTsidiiEmail(TestCase):

    def test_invalid_body_type(self):
        body = 618
        recipients = ReaderCollection()
        with self.assertRaises(ValueError):
            TsidiiEmail(body, recipients)

    def test_invalid_recipients_object(self):
        body = "Just a test body"
        recipients = [
            ("stan", "stan@example.com"),
            ("yumber jacks", "axvice@example.com")
        ]
        with self.assertRaises(ValueError):
            TsidiiEmail(body, recipients)

    def test_valid_body_and_recipients(self):
        body = "Just a test body"
        recipients = ReaderCollection()
        TsidiiEmail(body, recipients)

    def test_invalid_recipient_email(self):
        recipients = ReaderCollection()
        with self.assertRaises(ValueError):
            recipients.add_reader(
                first_name="Stan",
                last_name="Pines",
                email="mystery shack",
                identifier="grunkle"
            )

    def test_valid_parser_instantiation_minimum(self):
        body = "Just a test body"
        recipients = ReaderCollection()
        recipients.add_reader(
            first_name="Mabel",
            email="mabel@example.com"
        )
        TsidiiEmail(body, recipients)

    def test_valid_parser_instantiation_all(self):
        body = "Just a test body"
        recipients = ReaderCollection()
        recipients.add_reader(
            first_name="Mabel",
            last_name="Pines",
            email="mabel@example.com",
            identifier="mabel",
            groups=["pinesfamily", "mysterytwins"]

        )
        TsidiiEmail(body, recipients)

    def test_invalid_parser_group_dict_with_tuples(self):
        body = "Just a test body"
        recipients = [
            ("stan", "stan@example.com"),
            ("yumberjacks", "axvice@example.com")
        ]
        groups = {
            "cleaningcrew": ("soos"),
            "mysteryshack": ("stan", "yumberjacks")
        }
        with self.assertRaises(ValueError):
            TsidiiEmail(body, recipients)
        with self.assertRaises(ValueError):
            TsidiiEmail(body, recipients, groups)

    def test_parsing_of_basic_body(self):
        body = "Just a test body"
        recipients = ReaderCollection()
        recipients.add_reader(
            first_name="Mabel",
            last_name="Pines",
            email="mabel@example.com",
            identifier="mabel",
            groups=["pinesfamily", "mysterytwins"]

        )
        recipients.add_reader(
            first_name="Dipper",
            last_name="Pines",
            email="dipper@example.com",
            identifier="dippy",
            groups=["pinesfamily", "mysterytwins"]

        )
        for reader, email in TsidiiEmail(body, recipients).reader_emails():
            self.assertEqual(body, email[0])

    def test_parsing_of_body_with_message(self):
        body = "Just a test body\n<note message='mabel'>MABEL!</note>"
        recipients = ReaderCollection()
        recipients.add_reader(
            first_name="Mabel",
            last_name="Pines",
            email="mabel@example.com",
            identifier="mabel",
            groups=["pinesfamily", "mysterytwins"]

        )
        recipients.add_reader(
            first_name="Dipper",
            last_name="Pines",
            email="dipper@example.com",
            identifier="dippy",
            groups=["pinesfamily", "mysterytwins"]

        )
        for reader, email in TsidiiEmail(body, recipients).reader_emails():
            if reader.first_name == "Dipper":
                self.assertEqual("Just a test body\n", email[0])
            else:
                self.assertIn("MABEL!", email[0])

    def test_parsing_of_body_with_private_message(self):
        body = "Just a test body\n<note private='mabel'>MABEL!</note>"
        recipients = ReaderCollection()
        recipients.add_reader(
            first_name="Mabel",
            last_name="Pines",
            email="mabel@example.com",
            identifier="mabel",
            groups=["pinesfamily", "mysterytwins"]

        )
        recipients.add_reader(
            first_name="Dipper",
            last_name="Pines",
            email="dipper@example.com",
            identifier="dippy",
            groups=["pinesfamily", "mysterytwins"]

        )
        for reader, email in TsidiiEmail(body, recipients).reader_emails():
            if reader.first_name == "Dipper":
                self.assertFalse(email[1])
                self.assertEqual("Just a test body\n", email[0])
            else:
                self.assertTrue(email[1])
                self.assertIn("MABEL!", email[0])

    def test_parsing_of_body_with_hidden_message(self):
        body = "Just a test body\n<note hidden='dippy'>Dipper can't see this!</note>"
        recipients = ReaderCollection()
        recipients.add_reader(
            first_name="Mabel",
            last_name="Pines",
            email="mabel@example.com",
            identifier="mabel",
            groups=["pinesfamily", "mysterytwins"]

        )
        recipients.add_reader(
            first_name="Dipper",
            last_name="Pines",
            email="dipper@example.com",
            identifier="dippy",
            groups=["pinesfamily", "mysterytwins"]

        )
        for reader, email in TsidiiEmail(body, recipients).reader_emails():
            if reader.first_name == "Dipper":
                self.assertFalse(email[1])
                self.assertEqual("Just a test body\n", email[0])
            else:
                self.assertIn("Dipper can't see this!", email[0])

    def test_parsing_of_body_with_hidden_message_using_group_flag(self):
        body = "Just a test body\n<note hidden='pinesfamily'>Twins can't see this!</note>"
        recipients = ReaderCollection()
        recipients.add_reader(
            first_name="Mabel",
            last_name="Pines",
            email="mabel@example.com",
            identifier="mabel",
            groups=["pinesfamily", "mysterytwins"]

        )
        recipients.add_reader(
            first_name="Dipper",
            last_name="Pines",
            email="dipper@example.com",
            identifier="dippy",
            groups=["pinesfamily", "mysterytwins"]

        )
        for reader, email in TsidiiEmail(body, recipients).reader_emails():
            self.assertFalse(email[1])
            self.assertEqual("Just a test body\n", email[0])

    def test_parsing_of_body_with_message_using_group_flag(self):
        body = "Just a test body\n<note message='pinesfamily'>Twins can see this!</note>"
        recipients = ReaderCollection()
        recipients.add_reader(
            first_name="Mabel",
            last_name="Pines",
            email="mabel@example.com",
            identifier="mabel",
            groups=["pinesfamily", "mysterytwins"]

        )
        recipients.add_reader(
            first_name="Dipper",
            last_name="Pines",
            email="dipper@example.com",
            identifier="dippy",
            groups=["pinesfamily", "mysterytwins"]

        )
        for reader, email in TsidiiEmail(body, recipients).reader_emails():
            self.assertFalse(email[1])
            self.assertEqual("Just a test body\nTwins can see this!", email[0])

    def test_parsing_of_body_with_tag_no_attributes(self):
        body = "Just a test body\n<note>This doesn't show up!</note>"
        recipients = ReaderCollection()
        recipients.add_reader(
            first_name="Mabel",
            last_name="Pines",
            email="mabel@example.com",
            identifier="mabel",
            groups=["pinesfamily", "mysterytwins"]

        )
        recipients.add_reader(
            first_name="Dipper",
            last_name="Pines",
            email="dipper@example.com",
            identifier="dippy",
            groups=["pinesfamily", "mysterytwins"]

        )
        for reader, email in TsidiiEmail(body, recipients).reader_emails():
            self.assertFalse(email[1])
            self.assertEqual("Just a test body\n", email[0])
