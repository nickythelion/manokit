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

import setuptools
import sys
import os
import shutil

if "clean" in sys.argv:
    print("Removing previous version...")
    if os.path.exists("./build") and os.path.isdir("./build"):
        print("Removing 'build' folder")
        shutil.rmtree("./build")
    if os.path.exists("./dist") and os.path.isdir("./dist"):
        print("Removing 'dist' folder")
        shutil.rmtree("./dist")
    if os.path.exists("./manokit.egg-info") and os.path.isdir(
        "./manokit.egg-info"
    ):
        print("Removing 'manokit.egg-info' folder")
        shutil.rmtree("./manokit.egg-info")
    sys.exit(0)

with open("README.md", "r", encoding="UTF-8") as _f:
    long_desc = _f.read()

setuptools.setup(
    name="manokit",
    version="1.2.1",
    description="An easy-to-use, purely native email sender",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Nikolai Beloguzov",
    author_email="nickythelionfurry@gmail.com",
    url="https://github.com/nickythelion/manokit",
    packages=["manokit"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11" "Topic :: Communications",
        "Topic :: Communications :: Email",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    license="GNU GPLv3",
    install_requires=[],
    include_package_data=True,
    python_requires=">=3.8",
)
