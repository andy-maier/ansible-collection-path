# Ansible Collection Path Printer

**ansible-collection-path** prints the install directory of an Ansible
collection:

For example:

```
$ ansible-collection-path mynamespace.mycollection
/Users/myuser/.ansible/collections/ansible_collections/mynamespace.mycollection
```

The install directory is determined using the `ansible-galaxy collection list`
command, so your existing configuration for Ansible collection paths from
Ansible configuration files and environment variables is used.

# Use cases

The most prominent use case for such a functionality is the installation of
dependent Python packages: If your Ansible collection has dependencies on
Python packages, you can include a `requirements.txt` file with the collection
and instruct your collection users to use the `ansible-collection-path` command
to get the Python dependencies installed after installing the collection:

```
ansible-galaxy collection install <NAMESPACE>.<COLLECTION>

pip install $(ansible-collection-path <NAMESPACE>.<COLLECTION>)/requirements.txt
```

Including a `requirements.txt` file into your collection is easy: Have the file
in the main directory of your collection repo and do not include it in the
`build_ignore` property in your `galaxy.yml` file.

# Installation

If you want to install the package into a virtual Python environment:

```
$ pip install ansible-collection-path
```

Otherwise, you can also install it without depending on a virtual Python
environment:

- If not yet available, install the "pipx" command as described in
  https://pipx.pypa.io/stable/installation/.

- Then, install the package using "pipx":

  ```
  $ pipx install ansible-collection-path
  ```

# Reporting issues

If you encounter a problem, please report it as an
[issue on GitHub](https://github.com/andy-maier/ansible-collection-path/issues).

# License

This package is licensed under the
[Apache 2.0 License](http://apache.org/licenses/LICENSE-2.0).
