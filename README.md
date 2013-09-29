Gists.CLI
===========

> I'm a Developer who uses VI and the like. iPad and iPhone apps are great, but when I really need a Gist i'm at the command line. 

GistCommand - An easy to use CLI to manage *your* GitHub Gists. Create, edit, append, view, search and download. 

- Github - https://github.com/khilnani/gists.cli 
- Python Package - https://pypi.python.org/pypi/gists.cli

Installation
============

If you have Python PIP http://www.pip-installer.org/ Installed

- `pip install gists.cli`

If you prefer manual installation

- `git clone https://github.com/khilnani/gists.cli` or download the latest Tag Archive from https://github.com/khilnani/gists.cli
- Run the installer
  - `./install.py` with no arguments will install to `/usr/local/bin`.
  - `./install.py INSTALL_PATH` to install to a specific directory.

Usage
=========

Authentication
--------------

- By default the application will attempt to use Basic Auth to authenticate. 
- If `~/.git-credentials` is available, it will use the first entry. 
- If  `~/.gists` is found, it will be given preference over the above two mechanisms.

Usage
---------

- `gists` - list your Gists.
- `gists ID` - view Gist with ID on the console.
- `gists ID PATH` - download Gist files with ID to PATH. Will prompt for confirmation.
- `gists token|t` - setup to use OAuth Token other than `~/.git-credentials`. Saves to `~/.gists`.

Tips
---------

- Add `debug|d` at the end of any execution to view low level details. eg. `gists debug`. *NOTE - This will reveal your OAuth ID but not your Basic Auth password.*
- Add `supress|silent|s` at the end of any execution to supress any prompts of confirmations if you like to live dangerously. eg. `gists ID supress`. *This option cannot be used with `debug` as that would be silly.*


In Development
==============

- `gists new|n|create|c` - Create a new Gist. Content sent via Console, Clipboard or File.
- `gists update|u ID` - Update a Gist. Content sent via Console, Clipboard or File.
- `gists delete|d ID` - Delete a Gist.
- `gists append|a ID` - Append to a Gist. Content sent via Console, Clipboard or File.
- `gists backup|b` - Backup all Gists in the user's account.
- `gists search|s QUERY` - Search Gists.

Issues and Roadmap
==================

- Take a look at https://github.com/khilnani/gists.cli/issues to view Issues and Milestones.


