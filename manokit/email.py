# Copyright (C) 2021  Nickolai Beloguzov

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

# manokit.email module
#
# Provides all classes for sending emails
#
# > BaseEmail -> Base class. Only for inhereting
# > SimpleEmail -> Class for sending plain-text emails (does not support HTML)
# > HTMLEmail -> class for sending email containing HTML

from email.mime.base import MIMEBase
from typing import Union
from manokit._internal import ManokitInternal
import ssl
from manokit.exceptions import (
    AttachmentError,
    AuthError,
    EmailError,
    NotAValidEmailAddressError,
    ParameterError,
    SMTPError,
    BodyError,
)
import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders


class BaseEmail:
    """
    Basic class with barebone email sending functionality. Is designed primarily for inheritance purposes
    """

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        credentials: tuple[str, str],
        _ssl: bool = False,
    ) -> None:
        """
        Initialize BaseEmail instance for enabling email functionality for its subclasses

        Arguments:
            smtp_server: a SMTP server to send emails through (e.g. smtp.gmail.com, ...)
            smtp_host: a SMTP port to connect to (587 for TLS is the default one)
            credentials: a tuple, where first item is sender's login and second item is sender's password for authentication.
            Be aware, that all letters will be sent from address provided during this step.
            _ssl: connect via SSL ot TLS. Is is disabled by default

        Returns:
            None

        Raises:
            ParameterError: if at least one of function's parameters is not valid
            SMTPError: if there's a problem with SMTP connection
            AuthError: if SMTP authentication has failed
            NotAValidEmailAddressError: if sender's email address is not valid
        """
        # Checking if SMTP server is valid
        if not isinstance(smtp_server, str):
            raise ParameterError(
                "smtp_server: expected str; got {type}".format(
                    type=type(smtp_server).__name__
                )
            )

        if not smtp_server:
            raise ParameterError("no SMTP server specified")

        # Checking if SMTP port is valid
        if not isinstance(smtp_port, int):
            raise ParameterError(
                "smtp_port: expected int; got {type}".format(
                    type=type(smtp_port).__name__
                )
            )

        # Check if port not equal to 25 as this port does not support encryption
        if smtp_port == 25:
            raise SMTPError(
                "Sending emails via port 25 is not supported as this type of communication does not support encryption. Please use port 587 for TLS and port 465 for SSL instead"
            )

        # Check if _ssl is valid
        if not isinstance(_ssl, bool):
            raise ParameterError(
                "_ssl: expected bool; got {type}".format(type=type(_ssl).__name__)
            )

        # Checking if _creds is valid
        if not isinstance(credentials, tuple):
            raise ParameterError(
                "_creds: expected tuple; got {type}".format(
                    type=type(credentials).__name__
                )
            )

        if not credentials:
            raise ParameterError("cannot use empty credentials object")
        # SMTP server info
        self._host = smtp_server
        self._port = smtp_port
        self._ssl = _ssl

        # Email handler (will be generated later)
        self._server = None
        self._context = ssl.create_default_context()
        self._timestamp = datetime.datetime.now()
        self._FILESIZE_LIMIT = 20971520

        # Email info
        self._body = None
        self._attachments = []
        self._recepients = []
        self._subject = None

        # Credentials
        self._creds = credentials

        # Checking if sender's email is valid
        if not ManokitInternal.check_email_address(self._creds[0]):
            raise NotAValidEmailAddressError(
                "cannot use {email} for sending emails: invalid email".format(
                    email=self._creds[0]
                )
            )

        # Try and initialize a connection and login with given credentials
        # If cannot do that, raise an appropriate exception and close the connection
        try:
            # If SSL is enabled, connect via SMTP_SSL() method, otherwise use SMTP().starttls() sequence
            if self._ssl:
                self._server = smtplib.SMTP_SSL(
                    host=self._host, port=self._port, context=self._context
                )
            else:
                self._server = smtplib.SMTP(host=self._host, port=self._port)
                self._server.starttls(context=self._context)

            # Try to login with provided credentials
            self._server.login(user=self._creds[0], password=self._creds[1])
        except smtplib.SMTPAuthenticationError as exc:
            if self._server:
                self._server.quit()
            raise AuthError(
                "cannot connect to {host}:{port}. Bad credentials ({login}, {pwd})".format(
                    host=self._host,
                    port=self._port,
                    login=self._creds[0],
                    pwd=self._creds[1],
                )
            )

        except Exception as e:
            if self._server:
                self._server.quit()
            raise SMTPError(
                "cannot connect to {host}:{port}. Message: {msg}".format(
                    host=self._host, port=self._port, msg=str(e)
                )
            )

    def __repr__(self) -> str:
        return "{_class}(host={host}, port={port}, ssl={ssl}, handler={handler}, sender={sender_email}, sender_pwd={sender_pwd}, timestamp={time}, subject={sub}, recepients={rec}, attachments={attach}, body={body})".format(
            _class=self.__class__.__name__,
            host=self._host,
            port=self._port,
            ssl=self._ssl,
            handler=self._server,
            sender_email=self._creds[0],
            sender_pwd=self._creds[1],
            time=self._timestamp.strftime("%m-%d-%y %H:%M:%S"),
            sub=self._subject,
            rec=self._recepients,
            attach=self._attachments,
            body=self._body,
        )

    @property
    def subject(self) -> str:
        """
        Email's subject
        """
        return self._subject

    @subject.setter
    def subject(self, value) -> None:
        self._subject = str(value)

    @property
    def filesize_limit(self) -> int:
        """
        Maximum filsize for an attachment
        """
        return self._FILESIZE_LIMIT

    @property
    def timestamp(self) -> str:
        """
        Email's time of creation
        """
        return self._timestamp

    @property
    def body(self) -> str:
        """
        Email's content
        """
        return self._body

    @body.setter
    def body(self, value) -> None:
        self._body = value

    @property
    def recepients(self) -> list[str]:
        """
        List of recepients of current email
        """
        return self._recepients

    @recepients.setter
    def recepients(self, value: Union[str, list[str]]) -> None:
        if isinstance(value, str):
            self._recepients.clear()
            if not ManokitInternal.check_email_address(value):
                raise NotAValidEmailAddressError(
                    "cannot send email to {email}: invalid address".format(email=value)
                )
            self._recepients.append(value)

        else:
            for _, email in enumerate(value):
                if not ManokitInternal.check_email_address(email):
                    raise NotAValidEmailAddressError(
                        "cannot send email to {email}: invalid address".format(
                            email=email
                        )
                    )

            self._recepients = value

    @property
    def attachments(self) -> list[str]:
        """
        List of current email's attachments
        """
        return self._attachments

    @attachments.setter
    def attachments(self, value: Union[str, list[str]]) -> None:
        if isinstance(value, str):
            self._attachments.clear()
            self._attachments.append(os.path.abspath(str(value)))

        else:
            self._attachments = [os.path.abspath(str(file)) for file in value]

    @property
    def sender_email(self) -> str:
        """
        Sender's email
        """
        return self._creds[0]

    def send(self) -> None:
        """
        Send an email

        Arguments:
            None

        Returns:
            None

        Raises:
            EmailError: if email cannot be sent
        """

        # Checking if all necessare parameters for sending basic email are present
        if not self._subject:
            raise EmailError("cannot send email: no subject")

        if not self._body:
            raise EmailError("cannot send email: no body")

        if not self._recepients:
            raise EmailError("cannot send email: no recepients")

        # Creating Message object and setting necessary headers
        msg = MIMEMultipart()
        msg["Subject"] = self._subject
        msg["From"] = self._creds[0]
        msg["Date"] = self._timestamp.strftime("%d-%m-%y %H:%M:%S")

        content = self._body

        # If body contains html tags, encode it as 'text/html', otherwise encode it as 'text/plait'
        # NOTE: This might be deprecated in favor of all-html encoding
        body = MIMEText(
            content, "html" if ManokitInternal.contains_html(content) else "plain"
        )

        # Attaching converted body to Message
        msg.attach(body)

        # If any attachments are specifies, append it
        if self._attachments:
            for attachment in self._attachments:
                # If attachment does not exist, raise an exception
                if not os.path.exists(attachment):
                    raise AttachmentError(
                        "cannot attach '{file}': it does not exist".format(
                            file=os.path.split(attachment)[1]
                        )
                    )
                # If attachment is not a file, raise an exception
                if not os.path.isfile(attachment):
                    raise AttachmentError(
                        "cannot attach '{file}': it is not a file".format(
                            file=os.path.split(attachment)[1]
                        )
                    )

                # If file is empty, do not append it and skip current loop iteration
                if os.stat(attachment).st_size == 0:
                    continue

                # If attachment's size is more than 50Mb, raise an exception
                if os.stat(attachment).st_size > self._FILESIZE_LIMIT:
                    raise AttachmentError(
                        "cannot attach '{file}' file: filesize is more than 20Mb ({curr_size:.2f} Mb)".format(
                            file=attachment,
                            curr_size=os.stat(attachment).st_size / (1024 * 1024.0),
                        )
                    )

                # Read file and append it to Message
                _a_file = open(attachment, "rb")

                part = MIMEBase("application", "octet-stream")
                part.set_payload(_a_file.read())

                encoders.encode_base64(part)

                part.add_header(
                    "Content-Disposition",
                    "attachment; filename={file}".format(
                        file=os.path.split(attachment)[1]
                    ),
                )

                msg.attach(part)

        # Iterate over a list of recepients and send email to each
        for rec in self._recepients:
            msg["To"] = rec
            self._server.sendmail(self._creds[0], rec, msg.as_string())


class SimpleEmail(BaseEmail):
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        credentials: tuple[str, str],
        _ssl: bool = False,
    ) -> None:
        """
        Initialize a SimpleEmail instance to enable sending plain-text emails

        Arguments:
            smpt_server: a SMTP server to send emals through
            smtp_port: a SMTP port for connection
            credentials: a tuple with sender's login and password
            _ssl: use SSL to connect to SMTP (disabled by default)

        Returns:
            None

        Raises:
            ParameterError: if at least one of function's parameters is not valid
            SMTPError: if there's a problem with SMTP connection
            AuthError: if SMTP authentication has failed
            NotAValidEmailAddressError: if sender's email address is not valid

        """
        super().__init__(smtp_server, smtp_port, credentials, _ssl=_ssl)

    @BaseEmail.body.setter
    def body(self, value) -> None:
        if ManokitInternal.contains_html(value):
            raise BodyError("plain-text emails cannot contain HTML tags")
        self._body = value

    def body_from_file(self, file: str) -> None:
        # Check if path is valid
        if not isinstance(file, str):
            raise ParameterError(
                "file: expected str; got {type}".format(type=type(file).__name__)
            )

        if not file:
            raise ParameterError("path to file is empty")

        # Check if file exists and is a file
        if not os.path.exists(file):
            raise BodyError(
                "cannot read letter's body from {file} file: this file does not exist"
            )

        if not os.path.isfile(file):
            raise BodyError(
                "cannot read letter's body from {file} file: this is not a file"
            )

        path = ManokitInternal.format_path(file)
        with open(path, "r") as _f:
            body = _f.read()

        # If body from file contains HTML tags, raise an exception
        if ManokitInternal.contains_html(body):
            raise BodyError("plain-text emails cannot contain HTML tags.")

        self._body = body


class HTMLEmail(BaseEmail):
    """
    Class for sending emails containing HTML elements
    """

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        credentials: tuple[str, str],
        _ssl: bool = False,
    ) -> None:
        """
        Initialize a HTMLEmail instance to send emails with HTML support

        Arguments:
            smtp_server: a SMTP server to send emails through (e.g. smtp.gmail.com, ...)
            smtp_host: a SMTP port to connect to (587 for TLS is the default one)
            credentials: a tuple, where first item is sender's login and second item is sender's password for authentication.
            Be aware, that all letters will be sent from address provided during this step.
            _ssl: connect via SSL ot TLS. Is is disabled by default

        Returns:
            None

        Raises:
            ParameterError: if at least one of function's parameters is not valid
            SMTPError: if there's a problem with SMTP connection
            AuthError: if SMTP authentication has failed
            NotAValidEmailAddressError: if sender's email address is not valid
        """
        super().__init__(smtp_server, smtp_port, credentials, _ssl=_ssl)

    @BaseEmail.body.setter
    def body(self, value) -> None:
        if not ManokitInternal.contains_html(value):
            self._body = '<div style="font-family: Verdana; font-color: #262626">{body}</div>'.format(
                body=value
            )
            return
        self._body = value

    def body_from_file(self, file: str) -> None:
        """
        Read content from file and make it email's body

        Arguments:
            file: path to file. If content from file does not contain any HTML, default
            styling is applied (font family is Verdana, font's color is #262626)

        Returns:
            None

        Raises:
            ParameterError: if function's parameter is invalid
            BodyError: if email's body cannot be appended
        """
        # Check if path is valid
        if not isinstance(file, str):
            raise ParameterError(
                "file: expected str; got {type}".format(type=type(file).__name__)
            )

        if not file:
            raise ParameterError("path to file is empty")

        # Check if file exists and is a file
        if not os.path.exists(file):
            raise BodyError(
                "cannot read letter's body from {file} file: this file does not exist"
            )

        if not os.path.isfile(file):
            raise BodyError(
                "cannot read letter's body from {file} file: this is not a file"
            )

        # Retrieve file content
        path = ManokitInternal.format_path(file)
        with open(path, "r") as _f:
            body = _f.read()

        # If content does not contain any HTML, default styling is applied
        if not ManokitInternal.contains_html(body):

            self._body = '<div style="font-family: Verdana; font-color: #262626">{body}</div>'.format(
                body=body
            )
            return

        self._body = body
