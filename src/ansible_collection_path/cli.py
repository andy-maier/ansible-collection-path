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
main() entry point that prints the install path of an installed Ansible
collection.
"""

import sys
import os
import argparse

from .collection_path import collection_path, \
    CollectionPathDetermineError, CollectionNotInstalled, \
    CollectionInstalledMoreThanOnce


def parse_args(args):
    """
    Parses the CLI arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
Print the installation path of an installed Ansible collection.

The installation path is determined using the currently configured Ansible
collection path.

If the collection is installed, the command prints its absolute installation
path (unless -q is specified) and ends with exit code 0. The installation path
includes the 'namespace/name' path below the 'ansible_collections'
directory, i.e. it is the directory in which the collection has its FILES.json
and MANIFEST.json files.

Otherwise, the command displays an error message on stderr (unless -q is
specified) and ends with an exit code != 0.

Exit code  Meaning
-------------------------------------------------------------------------------
0          Collection is installed (once)
1          Collection is not installed
2          Error in command line arguments
3          Collection is installed more than once in the collection path
9          Error running ansible-galaxy command or parsing its output
""")
    parser.add_argument(
        "ns_name", metavar="NAMESPACE.NAME", action='store',
        help="collection namespace and name.")
    parser.add_argument(
        "-q", action='store_true',
        help="suppress messages (except error messages) and path output.\n"
        "This is useful for just testing whether the collection is installed.")
    return parser.parse_args(args)


def main():
    """
    Entry point for the script.
    """

    args = parse_args(sys.argv[1:])
    # exits with exit code 2 if required arguments are not provided.

    my_cmd = os.path.basename(sys.argv[0])
    pp = f"{my_cmd}: "

    ns_name_list = args.ns_name.split('.')
    if len(ns_name_list) != 2:
        print(f"{pp}Error: Invalid Ansible collection name: "
              f"{args.ns_name} - must be NAMESPACE.NAME",
              file=sys.stderr)
        return 2

    namespace, name = ns_name_list

    try:
        path = collection_path(namespace, name)
    except CollectionPathDetermineError as exc:
        print(f"{pp}Error: {exc}", file=sys.stderr)
        return 9
    except CollectionInstalledMoreThanOnce as exc:
        if not args.q:
            print(f"{pp}{exc}", file=sys.stderr)
        return 3
    except CollectionNotInstalled as exc:
        if not args.q:
            print(f"{pp}{exc}", file=sys.stderr)
        return 1

    if not args.q:
        print(path)

    return 0
