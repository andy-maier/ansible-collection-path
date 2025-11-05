# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Determine the install path of an installed Ansible collection.
"""

import os
import subprocess  # nosec: B404
import json


class CollectionPathError(Exception):
    """
    Base class for any errors in this module.
    """
    pass


class CollectionPathDetermineError(CollectionPathError):
    """
    Error determining the collection version.
    """
    pass


class CollectionNotInstalled(CollectionPathError):
    """
    The collection is not installed.
    """
    pass


class CollectionInstalledMoreThanOnce(CollectionPathError):
    """
    The collection is installed more than once.
    """
    pass


def collection_path(namespace, name):
    """
    Return the absolute path name of the install path of the specified
    Ansible collection.

    Parameters:
      namespace (str): Collection namespace.
      name (str): Collection name.

    Returns:
      str: Install path of the collection.

    Raises:
      CollectionPathDetermineError: Error determining the collection version.
      CollectionNotInstalled: Collection is not installed.
      CollectionInstalledMoreThanOnce: Collection is installed more than once.
    """
    cmd = (f"ansible-galaxy collection list {namespace}.{name} --format json")
    completed = subprocess.run(
        cmd, shell=True, check=False, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)  # nosec: B602
    out_str = completed.stdout.decode().strip()
    if completed.returncode != 0:
        raise CollectionPathDetermineError(
            f"Cannot list Ansible collection {namespace}.{name}: {out_str}")

    # Example JSON output:
    # {
    #     "/.../ansible_collections":
    #     {
    #         "ibm.qradar":
    #             {
    #                 "version": "3.0.0"
    #             }
    #         }
    #     }
    # The JSON string is the empty dict '{}' if the collectin is not installed

    # Remove possible warnings, e.g.
    #   [WARNING]: - unable to find ns.name in collection paths
    try:
        json_begin = out_str.index("{")
    except ValueError:
        raise CollectionPathDetermineError(
            f"List output for Ansible collection {namespace}.{name} does not "
            f"have a JSON start character:\n"
            f"Command:\n{cmd}\n"
            f"Output:\n{out_str}")
    json_out_str = out_str[json_begin:]

    try:
        out_dict = json.loads(json_out_str)
    except json.decoder.JSONDecodeError as exc:
        raise CollectionPathDetermineError(
            f"List output for Ansible collection {namespace}.{name} cannot be "
            f"parsed as JSON: {exc}\n"
            f"Command:\n{cmd}\n"
            f"Output:\n{out_str}")

    paths = list(out_dict.keys())
    if not paths:
        raise CollectionNotInstalled(
            f"Ansible collection {namespace}.{name} is not installed")

    if len(paths) > 1:
        path_lines = '\n'.join(paths)
        raise CollectionInstalledMoreThanOnce(
            f"Ansible collection {namespace}.{name} is installed more than "
            "once:\n"
            f"{path_lines}")

    path = os.path.join(paths[0], namespace, name)
    if not os.path.exists(path):
        raise CollectionNotInstalled(
            f"Ansible collection {namespace}.{name} is reported to be "
            f"installed but its install directory does not exist: {path}")

    return path
