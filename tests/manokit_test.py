from pathlib import Path
import shutil
import tempfile
from typing import Callable
import unittest

from manokit import Email


# This suite does not test anything that includes connecting to an SMTP host because it is a security risk


class ManokitTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # We will set a small limit so we can test how the filesize limit works
        self.email = Email("smtp.google.com", 587, filesize_limit=60)

        tmpdir = tempfile.mkdtemp()
        self.tmpdir = tmpdir
        self.file_30kb = Path(tmpdir, "30kb.txt")
        self.file_70kb = Path(tmpdir, "70kb.txt")

        with self.file_30kb.open("w") as f30:
            f30.write("b" * 30)

        with self.file_70kb.open("w") as f70:
            f70.write("a" * 70)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)

    def test_set_attachment_within_limit(self):
        self.email.add_attachment(self.file_30kb.as_posix())

        assert self.file_30kb.samefile(
            list(self.email.attachments)[0].as_posix()
        )
        assert self.email.available_filesize == 30

    @unittest.expectedFailure
    def test_set_attachments_exceeding_limit_one(self):
        self.email.add_attachment(self.file_70kb.as_posix())

    @unittest.expectedFailure
    def test_set_attachments_exceeding_limit_multiple(self):
        self.email.add_attachment(self.file_30kb.as_posix())  # Now 30kb left
        self.email.add_attachment(self.file_70kb.as_posix())

    def test_set_rec_valid_address(self):
        valid_address = "test@example.edu.ua"
        self.email.add_recipient(valid_address)

    @unittest.expectedFailure
    def test_set_rec_invalid_address(self):
        invalid_address = "test@ohmygod......what"
        self.email.add_recipient(invalid_address)

    def test_set_rec_already_in_bcc(self):
        addr = "alreadybcc@examplecorp.com"

        self.email.add_bcc(addr)
        assert len(self.email.bcc) == 1

        self.email.add_recipient(addr)
        assert len(self.email.rec) == 0

    def test_set_cc_already_in_rec(self):
        addr = "alreadybcc@examplecorp.com"

        self.email.add_recipient(addr)
        assert len(self.email.rec) == 1

        self.email.add_cc(addr)
        assert len(self.email.cc) == 0

    def test_set_bcc_already_in_cc(self):
        addr = "alreadybcc@examplecorp.com"

        self.email.add_cc(addr)
        assert len(self.email.cc) == 1

        self.email.add_bcc(addr)
        assert len(self.email.bcc) == 0

    def test_set_custom_email_validator(self):
        validator: Callable[[str], bool] = lambda addr: addr.endswith(
            "@examplecorp.com"
        )
        self.email.set_custom_email_validator(validator=validator)

        assert (
            self.email._check_if_valid_email_address("boss@examplecorp.com")
            == True
        )
        assert (
            self.email._check_if_valid_email_address("spy@rivalcorp.com")
            == False
        )
