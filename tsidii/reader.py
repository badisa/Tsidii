import re
import json
import random
import logging


class ReaderCollection(object):

    def __init__(self):
        self.readers = []
        self.groups = set()

    def __iter__(self):
        for reader in self.readers:
            yield reader

    def add_reader(self, first_name, email, last_name=None, identifier=None,
                   groups=None, create_identifier=False):
        reader = self.TsidiiReader(
            first_name=first_name,
            last_name=last_name,
            email=email,
            identifier=identifier,
            groups=groups
        )
        self.verify_unique_identifier(reader)
        if reader.groups:
            self.groups.update(set(reader.groups))
        self.readers.append(reader)

    def verify_unique_identifier(self, new_reader):
        # Recursive call seems excessive
        for reader in self.readers:
            if reader.identifier == new_reader.identifier:
                raise ValueError(
                    "'{}' not unique".format(new_reader.identifier)
                )
            elif new_reader.groups and reader.identifier in new_reader.groups:
                raise ValueError(
                    "Group conflicts with user identifier '{}'".format(reader.identifier)
                )
        return True

    def as_json(self):
        data = {
            "readers": [reader.get_data() for reader in self.readers]
        }
        return json.dumps(data)

    class TsidiiReader(object):

        def __init__(self, first_name, last_name, email, identifier=None,
                     groups=None):
            if not(identifier is None or isinstance(identifier, str)):
                raise TypeError("Identifier must be a String")
            if not self._check_email(email):
                raise ValueError("Invalid Email")
            if not self._check_string(identifier):
                raise ValueError("Invalid identifier - '{}'".format(identifier))
            if not self._check_string(first_name):
                raise ValueError("Invalid first name - '{}'".format(first_name))
            if not self._check_string(last_name):
                raise ValueError("Invalid last name - '{}'".format(last_name))
            self.first_name = first_name
            self.last_name = last_name
            if identifier is None:
                self._create_identifier()
            else:
                self.identifier = identifier
            self.email = email
            if groups is not None and not self._check_groups(groups):
                raise TypeError("Invalid list of groups")
            self.groups = groups

        def _check_groups(self, groups):
            if not isinstance(groups, list):
                logging.error(
                    "Groups are not a list"
                )
                return False
            for group in groups:
                if " " in group:
                    logging.error("Group {} has a space".format(group))
                    return False
            return True

        def _check_email(self, email):
            if not re.match(r"^[a-zA-Z0-9_.\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_.\-]+$", email):
                logging.error("{} is an invalid email address".format(email))
                return False
            return True

        def _check_string(self, string):
            if string is None:
                return True
            elif ' ' in string:
                return False
            return True

        def _create_identifier(self):
            letters = "abcdefghijklmnopqrstuvwxyz123456789"
            identifier = "".join(
                letters[random.randint(0, len(letters)-1)] for _ in range(0, 8)
            )
            self.identifier = identifier
            logging.info(
                "Created identifier for {0} {1}".format(
                    self.first_name,
                    self.last_name
                )
            )

        def get_data(self):
            reader = {
                "firstName": self.first_name,
                "lastName": self.last_name,
                "email": self.email,
                "identifier": self.identifier,
                "groups": self.groups if self.groups else []
            }
            return reader
