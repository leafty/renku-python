# -*- coding: utf-8 -*-
#
# Copyright 2018 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Represent the Common Workflow Language types."""

import os

import attr

from renku._compat import Path

from ._ascwl import CWLClass


@attr.s
class File(CWLClass):
    """Represent a file."""

    path = attr.ib(converter=Path)

    def __str__(self):
        """Simple conversion to string."""
        # TODO refactor to use `basedir`
        return os.path.relpath(
            os.path.realpath(str(self.path)), os.path.realpath(os.getcwd())
        )
