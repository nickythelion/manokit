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

# manokit._internal module
#
# Provides internal utilities for manokit package
#
# NOTE: DO NOT USE THIS MODULE IN PRODUCTION
# IT WAS NOT INTENDED BY A DEVELOPER AND IS HIGHLY DISCOURAGED

from manokit.exceptions import ParameterError, SMTPError
from pathlib import Path
from typing import Union
import re


class ManokitInternal:
    @staticmethod
    def format_path(path: Union["str", "list[str]", "tuple[str]", "set[str]"]) -> Path:
        """
        Format string/a collection of strings into a pathlike string

        Arguments:
            path: a string, list, tuple or set of strings to be formatted

        Returns:
            os.PathLike instance

        Raises:
            ParameterError: if function's parameter is not valid
        """
        # Checking if path parameter has a valid type
        if not isinstance(path, (str, list, tuple, str)):
            raise ParameterError(
                "path parameter: expected str, list, tuple or set; got {wrong_type}".format(
                    wrong_type=type(path).__name__
                )
            )

        # Check if path is not empty
        if not path:
            raise ParameterError("path parameter: this parameter is empty")

        # If path is string, make it absolute and normalize it
        if isinstance(path, str):
            # return R"{path}".format(path=os.path.normpath(os.path.abspath(path)))
            return Path(path).absolute().as_posix()

        # If path is a collection of strings, join it together, make it absolute and normalize it
        # return R"{path}".format(path=os.path.normpath(os.path.abspath(os.path.join(*[str(i) for i in path]))))
        return Path(*path).absolute().as_posix()

    @staticmethod
    def check_email_address(email: str) -> bool:
        """
        Check if email address is valid

        Arguments:
            email: email address to verify

        Returns:
            A boolean. If True, address if ok, otherwise address is not valid

        Raises:
            ParameterError: if function's parameter is not valid
        """

        # Check if email is a string
        if not isinstance(email, str):
            raise ParameterError(
                "email parameter: expected str; got {wrong_type}".format(
                    wrong_type=type(email).__name__
                )
            )

        # Check if email is not empty
        if not email:
            raise ParameterError("email parameter is empty")

        # Reex for email verification
        _EMAIL_REGEX = re.compile("^[-_+.\d\w]+@[-_+.\d\w]+\.[\w]+$")

        # Verify email
        if not _EMAIL_REGEX.fullmatch(email):
            return False

        return True

    @staticmethod
    def contains_html(_string: str) -> bool:
        """
        Check if given string contains HTML elements

        Arguments:
            _text: string to verify

        Returns:
            A boolean. If method returns True, HTML elements are present in given string.
            Otherwise False is returned

        Raises:
            ParameterError: if function's parameter is invalid
        """

        # Check if _string's type is valid
        if not isinstance(_string, str):
            raise ParameterError(
                "_string: expected str; got {type}".format(type=type(_string).__name__)
            )

        # If _string is equal to an empty string, immediately return False
        if not _string:
            return False

        _HTML_REGEX = re.compile(
            "<\/?[\w -][\s\S]*>", re.IGNORECASE | re.DOTALL | re.MULTILINE
        )

        if _HTML_REGEX.search(_string):
            return True

        return False
