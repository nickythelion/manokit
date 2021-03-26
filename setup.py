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

import setuptools

with open("README.md", "r", encoding="UTF-8") as _f:
    long_desc = _f.read()

setuptools.setup(
    name="manokit",
    version="1.0.0",
    description="An easy-to-use email client",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Nickolai Beloguzov",
    author_email="nickolai.beloguzov@gmail.com",
    url="https://github.com/NickolaiBeloguzov/manokit",
    packages=["manokit"],
    classifiers=[],
    license="Apache 2.0",
    install_requires=[],
    include_package_data=True,
    python_requires=">=3.9",
)
