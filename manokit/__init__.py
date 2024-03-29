# Copyright (C) 2023  Nikolai Beloguzov a/k/a nickythelion

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from email.mime.base import MIMEBase
from pathlib import Path
import re
from typing import Any, Callable, List, Literal, Self, Set
import ssl
from manokit.exceptions import (
    AttachmentError,
    EmailError,
    NotAValidEmailAddressError,
)
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders


class Email:
    """A class that contains everything needed for sending emails

    Attributes:
        * host (str): An SMTP Host used for sending emails
        * port (int): An SMTP port.

        * email_handler (SMTP | SMTP_SSL): An object that actually responsible for sending emails. It is
        noted that Manokit only supports encrypted connections with either SSL or TLS, so if you want to use Manokit for unencrypted connections,
        you can override this object, but in that case the library's functions may be altered/unavailable
        ssl_context (SSLContext): An SSL context used for encryption. Can be overwritten with a custom context

        * author (str): An email address which sends an email (an email's author). It is set during authentication and defaults to the username.
        * subject (str): Email's subject. Defaults to '<no subject>'
        * body (str): Email's body. Defaults to '<no body>'
        * attachments (Set[Path]): a set of pathlib.Path objects that point to the files that need to be attached to the email

        * rec (Set[str]): a set of email addresses which will receive an email
        * cc (Set[str]): a set of email addresses that will be CC'd into the email
        * bcc (Set[str]): a set of email addresses that will be BCC'd into the email

        * FILESIZE_LIMIT (int): A limit on total size of attachments.
        * available_filesize (int): How much free space is available for attachments
        * timestamp (datetime.datetime): A timestamp of when the email was created
        * email_validators (Dict[str, (str) -> bool]): a dictionary that maps different scopes to different validators
    """

    # Maybe we can add an ability for the end user to use custom validators?
    def _check_if_valid_email_address(
        self,
        address: str,
        scope: Literal["author", "recipients", "cc", "bcc"],
    ) -> bool:
        """Checks whether an email address is valid by calling a validator function.

        Args:
            address (str): an email address
            scope (author | recipients | cc | bcc): a scope that will be used

        Returns:
            bool: True if the email address is valid, False otherwise
        """
        return self.email_validators[scope](address)

    def _default_email_validator(self, address: str) -> bool:
        """Checks whether an email address is valid. This validator can be overridden by the user.

        By default, Manokit uses a regular expression (this one: '^[-_+.\d\w]+@[-_+\d\w]+(?:\.{1}[\w]+)+$') to verify an email.

        Args:
            address (str): an email address

        Returns:
            bool: True if the email address is valid, False otherwise
        """
        return bool(
            re.fullmatch(
                "^[-_+.\d\w]+@[-_+\d\w]+(?:\.{1}[\w]+)+$",
                address,
                re.IGNORECASE,
            )
        )

    def __init__(
        self, smtp_host: str, smtp_port: int, *, filesize_limit: int = 26214400
    ) -> None:
        """Creates an Email object.

        Args:
            smtp_host (str): What SMTP host to use, e.g. smtp.google.com, etc
            smtp_port (int): SMTP port to connect to
            filesize_limit (int, optional): Maximum size of all attachments combined. Defaults to 26214400 bytes (25MB), but can be overridden.
        """
        self.host = smtp_host
        self.port = smtp_port

        self.email_handler = None
        self.ssl_context = ssl.create_default_context()

        self.author = None

        self.subject = "<no subject>"
        self.body = "<no body>"
        self.attachments: "Set[Path]" = set()

        self.rec = set()
        self.cc = set()
        self.bcc = set()

        self.FILESIZE_LIMIT = filesize_limit
        self.available_filesize = filesize_limit
        self.email_validators = {
            "author": self._default_email_validator,
            "recipients": self._default_email_validator,
            "cc": self._default_email_validator,
            "bcc": self._default_email_validator,
        }

        # Maybe move it to send() function because it is used only there
        self.timestamp = datetime.datetime.now()

    def login(
        self,
        username: str,
        password: str,
        *,
        use_starttls: bool = True,
    ) -> Self:
        """Authenticates with the SMTP host

        Args:
            username (str): user's email address
            password (str): password to login. Google's app passwords are supported
            use_starttls (bool, optional): Whether to use STARTTLS over SSL or not. Defaults to True.

        Returns:
            Self: Returns a modified instance for method chaining

        Raises:
            SMTPAuthenticationError: the authentication process could not be completed
            NotAValidEmailAddressError: the address email is invalid
        """

        if not self._check_if_valid_email_address(username, "author"):
            raise NotAValidEmailAddressError(
                f"address {username} has failed validation"
            )

        if use_starttls:
            serv = smtplib.SMTP(self.host, self.port)
            serv.starttls(context=self.ssl_context)
        else:
            serv = smtplib.SMTP_SSL(
                host=self.host,
                port=self.port,
                context=self.ssl_context,
            )

        serv.login(user=username, password=password)

        self.email_handler = serv
        self.author = username

        return self

    def logout(self) -> None:
        """Closes the SMTP session"""
        self.email_handler.quit()

    def add_recipient(self, address: str) -> Self:
        """Adds a recipient that will receive an email. This will have no effect if the address is already in CC or BCC lists

        Args:
            address (str): An email address

        Returns:
            Self: Returns a modified instance for method chaining

        Raises:
            NotAValidEmailAddressError: the address email is invalid
        """
        if not self._check_if_valid_email_address(address, "recipients"):
            raise NotAValidEmailAddressError(
                f"address {address} has failed validation"
            )

        if (address not in self.cc) and (address not in self.bcc):
            self.rec.add(address)

        return self

    def add_cc(self, address: str) -> Self:
        """Adds a recipient that will be CC's into an email. This will have no effect if the address is already a direct recipient or is in BCC list

        Args:
            address (str): An email address

        Returns:
            Self: Returns a modified instance for method chaining

        Raises:
            NotAValidEmailAddressError: the address email is invalid
        """
        if not self._check_if_valid_email_address(address, "cc"):
            raise NotAValidEmailAddressError(
                f"address {address} has failed validation"
            )

        if (address not in self.rec) and (address not in self.bcc):
            self.cc.add(address)

        return self

    def add_bcc(self, address: str) -> Self:
        """Adds a recipient that will be BCC'd into an email. This will have no effect if the address is already a direct recipient or is in CC list

        Args:
            address (str): An email address

        Returns:
            Self: Returns a modified instance for method chaining

        Raises:
            NotAValidEmailAddressError: the address email is invalid
        """
        if not self._check_if_valid_email_address(address, "bcc"):
            raise NotAValidEmailAddressError(
                f"address {address} has failed validation"
            )

        if (address not in self.rec) and (address not in self.cc):
            self.bcc.add(address)

        return self

    def set_body(self, body: Any) -> Self:
        """Sets an email's body

        Args:
            body (Any): A body

        Returns:
            Self: Returns a modified instance for method chaining
        """
        self.body = body

        return self

    def set_subject(self, subject: str) -> Self:
        """Sets an email's subject

        Args:
            subject (str): A string representing the email's subject

        Returns:
            Self: Returns a modified instance for method chaining
        """
        self.subject = subject

        return self

    def set_custom_email_validator(
        self,
        validator: "Callable[[str], bool]",
        scopes: List[Literal["all", "author", "recipients", "cc", "bcc"]] = [
            "all"
        ],
    ) -> None:
        """Changes an email validator to the one defined by the user. This is useful in case the user finds default validation insufficient, or the validation needs to be set programmatically

        Args:
            validator ((str) -> bool): A function that takes a single parameter of type 'str' and returns a boolean
            scope (List[all | author | recipients | cc | bcc], optional): what the validator will be scoped to. Available scopes:
                * all - use this validator for validation of all email addresses. This is the default value
                * author - use this email for validating only the sender's email. If this is the case, this function needs to be called before 'login()'
                * recipients - use this email for validating only the recipients' emails.
                * cc - use this email for validating only the addresses that will be CC'd into the email
                * bcc - use this email for validating only the addresses that will be BCC'd into the email

        Raises:
            ValueError: if provided scope is not in the list of allowed scopes
        """

        if "all" in scopes:
            self.email_validators["author"] = validator
            self.email_validators["recipients"] = validator
            self.email_validators["cc"] = validator
            self.email_validators["bcc"] = validator
            return

        for s in scopes:
            if s not in ["all", "author", "recipients", "cc", "bcc"]:
                raise ValueError(f"scope '{s}' if invalid")

            self.email_validators[s] = validator

    def add_attachment(self, path: str) -> Self:
        """Adds an attachments to an email. This has no effect if an attachment already has been added or the file has a size of 0 bytes

        Args:
            path (str): A path to the file what needs to be attached

        Raises:
            AttachmentError: if path points to an object that is not a file
            AttachmentError: if file's size is larger than the available space for attachments

        Returns:
            Self: Returns a modified instance for method chaining
        """

        p = Path(path)

        if p in self.attachments:
            return

        if p.stat().st_size == 0:
            return

        if not p.is_file():
            raise AttachmentError(
                f"cannot attach {p.as_posix()} because it is not a file"
            )

        rem_filesize = self.available_filesize - p.stat().st_size

        if rem_filesize < 0:
            raise AttachmentError(
                f"cannot add an attachment; the combines size of all attachments is larger than the filesize limit ({self.FILESIZE_LIMIT} bytes)"
            )

        self.attachments.add(p)
        self.available_filesize = rem_filesize

        return self

    def send(self) -> Self:
        """Sends an email.

        Raises:
            EmailError: if the recipient list is empty

        Returns:
            Self: Returns a modified instance for method chaining
        """
        if len(self.rec) < 1:
            raise EmailError(
                "cannot send an email because there is no one to receive it"
            )

        message = MIMEMultipart()
        message["Subject"] = self.subject
        message["From"] = self.author
        message["Date"] = self.timestamp.strftime("%d/%m/%Y %H:%M:%S")
        message["Cc"] = ",".join(self.cc)

        # You can use text/plain, but using text/html gives you more flexibility
        message.attach(MIMEText(self.body, "html"))

        for file in self.attachments:
            part = MIMEBase("application", "octet-stream")
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={file.name}",
            )

            with file.open("rb") as f:
                part.set_payload(f.read())
                encoders.encode_base64(part)

            message.attach(part)

        errs = self.email_handler.sendmail(
            self.author,
            list(self.rec | self.cc | self.bcc),
            message.as_string(),
        )

        if errs:
            raise EmailError(
                f"message to {errs.keys()[0]} failed (code {errs.get(errs.keys()[0])[0]}): {errs.get(errs.keys()[0])[1]}"
            )

        return self
