**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*

- [Gists.cli](#gistscli)
- [Overview](#overview)
- [For the Casual User](#for-the-casual-user)
  - [Installation](#installation)
  - [Authentication](#authentication)
  - [Usage](#usage)
- [For The Advanced User](#for-the-advanced-user)
  - [Tips](#tips)
  - [Usage](#usage-1)
- [For the Developer](#for-the-developer)
  - [Installation](#installation-1)
  - [Non-Mac/OS X System Testing](#non-macos-x-system-testing)
- [In Development](#in-development)
- [Issues and Roadmap](#issues-and-roadmap)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)
 

# Gists.cli

An easy to use CLI to manage *your* GitHub Gists. Create, edit, append, view, search and backup your Gists. 

- Github - https://github.com/khilnani/gists.cli 
- Python Package - https://pypi.python.org/pypi/gists.cli

# Overview


I'm a Developer who uses VI and the like. iPad and iPhone apps are great, but when I really need a Gist i'm at the command line. 

The primary goal is to create something designed specifically to capture quick notes/links while requiring minimum typing.
In addition to conventional view, download, edit and delete support, the application attempts to consider a variety scenarios -

- Append - Ability to append text to a Gist instead of having to download, edit and update.
- iOS support - [Pythonista](http://omz-software.com/pythonista/) is pretty damn cool. Use [Pypi.py](https://gist.github.com/anonymous/5243199) or [Pipista](https://gist.github.com/pudquick/4116558)
- VGA terminals - Using a mouse to copy/paste Gists IDs is great, but when a mouse is not handy index number can be used instead of a Gist IDs. 
  - Use `gists .1` or `gists :1` or `gists %1` to view the first Gist. Easier but less explicit than `gists 233HSHS2233`
- Executing without download - You can pipe the output from the application to an interpreter as appropriate. eg. `gists 1111 | sh`
- Each command/action has aliases/formats to suit your preferences.
  - Use `gists --help` or `gists -h` if you prefer standard CLI optiions, or just `gists help` or `gists h` if you want to type less


# For the Casual User

## Installation

- Mac OS X / Linux 
  - `sudo easy_install gists.cli`
- Using PIP
  - Install Python Setup Tools
    - CentOS
      - Run `yum install python-setuptools`
    - Manual Install
      - Run `curl -v https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | sudo python` or, follow instructions at [https://pypi.python.org/pypi/setuptools#installation-instructions]
  - Install the Python package manager PIP (http://www.pip-installer.org/)
    - Run `sudo easy_install pip`
  - Once PIP is installed, 
    - Run `sudo pip install gists.cli`
    - Run `sudo pip install gists.cli --upgrade` if upgrading.
    - Check the installed version by running `pip show gists.cli`

## Authentication

> Two factor authentication (SMS and Application) supported as of 0.350

- By default the application will attempt to use Basic Auth to authenticate i.e. will prompt for username/password each time it is run.
- If the file `~/.git-credentials` is available, it will use the first OAuth token entry. 
- If the file  `~/.gists` with a Github OAuth token is found, it will be given preference over the above two mechanisms.
- Run `gists token|--token|t|-t` to avoid the username/password prompt and to use an OAuth Token other than `~/.git-credentials`. Saves to `~/.gists`.

## Usage

> *All the commands below are interactive and will prompt for user input (eg. public/private, descriptions) and confirmations (eg. directory creation).*

*Each Action/Command has multiple alias e.g. Create can be invoked not only by `gists new|create`, but also  `gists c|n|new|create|--new|--create|-n|-c` Run `gists help|--help|-h|h` for more info.*

**List all your Gists**

- `gists`

**View a Gist**

- `gists ID` - View all files within a Gist with ID on the console.

> ID can be a Gist ID or Index ID (of the Gist in the List view) Index must be in the format `'#N'`, `%N` , `.N` or `:N`

**Download a Gist**

- `gists ID PATH` - Download Gist files with ID to PATH. Will prompt for confirmation.

> ID can be a Gist ID or Index ID (of the Gist in the List view) Index must be in the format `'#N'`, `%N` , `.N` or `:N`

**Create a Gist**

We'll prompt for stuff like Gist type (public/private), Description and Gist Content as needed.

- `gists new` or `gists create`.
- `gists FILE` - Create a Gist using the contents of FILE
- `gists "Content"` - Create a Gist using the string "Content"

To avoid the Public/private Gist type prompt -

> Bool should be `true` for Public, `false` for Private

- `gists Bool FILE`
- `gists Bool "Content"`

**Append to a Gist**

> - If Description or Content is '?', that field will be skipped.
>   - eg. `gists 223322 ? "New link to cool site"` will append a new line but will not update the Description
>   - eg. `gists 223322 "Updated Description ?` will only update the Description
> - ID can be a Gist ID or Index ID (of the Gist in the List view) Index must be in the format `'#N'`, `%N` , `.N` or `:N`

*NOTE - If a Gist contains more than one file, each file will have a new line appended with the content sent.*

- `gists ID Description FILE`
- `gists ID Description "Content"`

**Delete to a Gist**

- `gists delete ID` - Will prompt for confirmation.

# For The Advanced User


## Tips

- Each Action/Command has multiple alias e.g. Create can be invoked not only by `gists new|create`, but also  `gists c|n|new|create|--new|--create|-n|-c` Run `gists help|--help|-h|h` for more info
- ID can be a Gist ID or Index ID (of the Gist in the List view) Index must be in the format `'#N'`, `%N` , `.N` or `:N`
- Add `debug|--debug` to the end of any execution to view low level details. eg. `gists debug`. *NOTE - This will reveal your OAuth ID but not your Basic Auth password.*
- Add `supress|silent|--supress|--silient` at the end of any execution to supress any prompts of confirmations if you like to live dangerously. 
- eg. `gists -n FILE --supress --debug`. 

## Usage

In addition to the usage examples above, you can also gain additional flexibility by specifying command line options (eg. -g, --get)

*All the commands below are interactive and will prompt for user input.*

**List all your Gists**

- `gists list|--list|-l|l`

**View a Gist**

- `gists view|--view|v|-v ID` - View all files within a Gist with ID on the console.
- `gists view|--view|v|-v ID FILE` - View a specific file (FILE) in a Gist on the console. The matching is case-insensitive.

> ID can be a Gist ID or Index ID (of the Gist in the List view) Index must be in the format `'#N'`, `%N` , `.N` or `:N`

**Download a Gist**

- `gists get|--get|g|-g ID PATH` - Download Gist files with ID to PATH. Will prompt for confirmation.
- `gists get|--get|g|-g ID FILE PATH ` - Download a specific file (FILE) in a Gist to PATH. The matching is case-insensitive.

> ID can be a Gist ID or Index ID (of the Gist in the List view) Index must be in the format `'#N'`, `%N` , `.N` or `:N`

**Setup OAuth token**

- `gists token|t|--token|-t` - Setup to use OAuth Token other than `~/.git-credentials`. Saves to `~/.gists`.

**Create a Gist**

> - FILE - is a file path, relative or absolute.
> - Bool - True for Public, False for Private. Supports True, False, 1, 0, Yes, No, y, n. Case-insensitive
> - Description and Content - Text content within quotes


Without specifying a command (eg. create, new), the application will trying to figure it out. However, this supports fewer combinations of arguments.

- `gists FILE`
- `gists "Content"`
- `gists Bool FILE`
- `gists Bool "Content"`
- `gists "Description" FILE`
- `gists "Description" "Content"`
- `gists Bool "Description" FILE`
- `gists Bool "Description" "Content"`


If you like to type, or be specific you can also use the command line option. You will be prompted for stuff like Gist type, Description and Gist Content etc as needed.

*OPTION* = `new|--new|n|-n|create|--create|c|-c`

- `gists OPTION`
- `gists OPTION FILE`
- `gists OPTION "Content"`
- `gists OPTION Bool FILE`
- `gists OPTION Bool "Content"`
- `gists OPTION "Description" FILE`
- `gists OPTION "Description" "Content"`
- `gists OPTION Bool "Description" FILE`
- `gists OPTION Bool "Description" "Content"`


**Append to a Gist**

> - If Description or Content is '?', that field will be skipped.
>   - eg. `gists 223322 ? "New link to cool site"` will append a new line but will not update the Description
>   - eg. `gists 223322 "Updated Description ?` will only update the Description
> - ID can be a Gist ID or Index ID (of the Gist in the List view) Index must be in the format `'#N'`, `%N` , `.N` or `:N`

Without specifiying a specific action, the following will result in an Append. 

*NOTE - If a Gist contains more than one file, each file will have a new line appended with the content sent.*

- `gists ID Description FILE`
- `gists ID Description "Content"`

For more control/specificity

*OPTION* = `append|--append|a|-a`

- `gists OPTION ID File`
- `gists OPTION ID Content`
- `gists OPTION ID Description File`
- `gists OPTION ID Description Content`


**Update**

> - If Description or Content is '?', that field will be skipped.
>   - eg. `gists 223322 ? "New link to cool site"` will append a new line but will not update the Description
>   - eg. `gists 223322 "Updated Description ?` will only update the Description
> - ID can be a Gist ID or Index ID (of the Gist in the List view) Index must be in the format `'#N'`, `%N` , `.N` or `:N`

*NOTE - A file in a Gist will be updated only if the file name sent is an exact match. If not file name match is found, a new file is added to the Gist.*

*OPTION* = `update|--update|u|-u`

- `gists OPTION ID File`
- `gists OPTION ID Content`
- `gists OPTION ID Description File`
- `gists OPTION ID Description Content`

**Delete**

- `gists delete|del|d|--delete|--del|-d ID` - Delete a Gist. Will prompt for confirmation.

> ID can be a Gist ID or Index ID (of the Gist in the List view) Index must be in the format `'#N'`, `%N` , `.N` or `:N`

# In Development

**Export/Backup**

- `gists backup|b|--backup|-b [DIR]` - Backup all Gists in the user's account.

**Search**

- `gists search|query|q|--search|--query|-q QUERY` - Search Gists.

**Misc**

- `gists stars|--stars` - List starred Gists


# For the Developer

## Installation

If you would like to contribute changes to the code base

- Get the code
  - Fork and `git clone` the fork, or ...
  - `git clone https://github.com/khilnani/gists.cli.git`, or ...
  - Download the latest Tag Archive from https://github.com/khilnani/gists.cli  
    - *Downloading the Archive is not recommended, since it won't be easy to merge code back*.
- Install dependencies by running `./dependencies.sh`. 
  - This installs PIP (if not already installed) and then installs the dependencies.
- Run the installer as below. If you get any error run with `sudo ...`
  - `./install.py` with no arguments will install to `/usr/local/bin`.
  - `./install.py INSTALL_PATH` will install to a specific directory.

## Non-Mac/OS X System Testing

- I use http://VagrantUp.com, http://ansibleworks.com and http://www.virtualBox.org to test on CentOS and Ubuntu.
- Prerequisites
  - Vagrant
    - Install Vagrant - http://vagrantup.com/downloads
  - Ansible
    - Install Ansible on Mac OS X or CentOS/RHEL - https://github.com/khilnani/devops/tree/master/ansible
  - Virtual Box
    - Install VirtualBox - https://www.virtualbox.org/wiki/Downloads to download/install
- Run
  -  Run `vagrant up` to install both CentOS6.5 and Ubuntu, or`vagrant up centos` or `vagrant up ubuntu` - start the VMs
    - If my Boxes are not already installed, they will be downloaded and installed
  -  Run `vagrant ssh centos` or `vagrant ssh ubuntu` - to ssh over
  -  Once you SSH over, the current directory is available at `/git_data` on the VM
- Debug
  -  Change directory to `./_vagrant`
  -  Run `./debug.ssh up centos` or `./debug.ssh up ubuntu` - This runs Vagrant with Debug Level INFO

## Docker

- Build the container with `docker build -t gists .`
- If you run the image using the command below, everything in the current directory will be available within the container. In particular, it is useful to put your oauth token into `.gists`, where it will be found by gists running in the container
- Example usage:
  - List gists: `docker run --rm -it -v $(pwd):/gists gists -l`
  - Download: `docker run --rm -it -v $(pwd):/gists gists -g :1 .`
- An example wrapper script is in `gists-docker` and can be invoked in place of `gists`. All options are passed to gists running within the container
- Caveats:
  - Only the current working directory is mounted in the examples above. Files passed as options will not be available if they are in a different directory

# Issues and Roadmap

- Take a look at https://github.com/khilnani/gists.cli/issues to view Issues and Milestones.

# Troubleshooting

- If you get the error `Wheel installs require setuptools >= 0.8 for dist-info support` or `ImportError: No module named pkg_resources`, please ensure you have upgraded setup tools. See the 'Install Python Setup Tools/Manual Install' section above to upgrade setup tools.
  - This dependency was introduced in Pypi 1.5 and will be removed in Pypi 1.5.1 [http://pip.readthedocs.org/en/1.5.X/news.html#]. 
- If you get the error `AttributeError: VerifiedHTTPSConnection instance has no attribute '_tunnel_host`, this is likely due to you running Python 2.6.2 or earlier. 
  - Running `sudo pip install requests==1.2.3` resolves the issue. The requests 2.0 library uses urllib3 that uses some capabilities only available in Python 2.6.3

# Credits

- Author - Nik Khilnani - http://khilnani.org
- Feedback and Spellcheck - Alexander - https://github.com/alexander-bzz
- Stack Overflow - http://stackoverflow.com/questions/tagged/python
- Pythonista Forums - https://omz-forums.appspot.com/pythonista/post/4691117899513856



