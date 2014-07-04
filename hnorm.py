#!/usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                    :::    :::  ::::::::  ::::    ::: :::::::::: :::   :::   #
#                   :+:    :+: :+:    :+: :+:+:   :+: :+:        :+:   :+:    #
#                  +:+    +:+ +:+    +:+ :+:+:+  +:+ +:+         +:+ +:+      #
#                 +#++:++#++ +#+    +:+ +#+ +:+ +#+ +#++:++#     +#++:        #
#                +#+    +#+ +#+    +#+ +#+  +#+#+# +#+           +#+          #
#               #+#    #+# #+#    #+# #+#   #+#+# #+#           #+#           #
#              ###    ###  ########  ###    #### ##########    ### -          #
#         #########      ###     #########   ########  ########## #########   #
#        #+#    #+#   #+# #+#   #+#    #+# #+#    #+# #+#        #+#    #+#   #
#       +#+    +#+  +#+   +#+  +#+    +#+ +#+        +#+        +#+    +#+    #
#      +:++#++:+  +:++#++:++# +:+    +#+ #:#        +:++#++:   +:++#++:#      #
#     +:+    +:+ +:+     +:+ +:+    +:+ +:+   +:+: +:+        +:+    +:+      #
#    :+:    :+: :+:     :+: :+:    :+: :+:    :+: :+:        :+:    :+:       #
#   :::::::::  :::     ::: :::::::::   ::::::::  :::::::::: :::    :::.fr     #
#                                                                             #
# *************************************************************************** #

"""\
        Honeybadger Program Checker

Usage:
    hnorm [-u USER]... [FOLDER]
    hnorm (-h | --help)
    hnorm (-v | --version)
    hnorm (-c | --changelog)

Options:
    -u USER, --user USER        Add user to user list.
    -h, --help                  Display this help screen.
    -v, --version               Display the script version.
    -c, --changelog             Display

"""

__version__ = "0.1b"
__changes__ = """\
0.1b:
    - Now using colorama and pathlib
    - Pretty messages, warnings and errors
    - Get source files from directory

0.1a:
    - Script base
    - Auto-install Python3 and missing libraries
    - Auteur file check added
    - Cool Honeybadger header
"""
__todo__ = """
- Call norminette on source files
- Check header from files
- Check for common banned functions

- Translations/Shorter messages? (?)
"""

# User config:

DISPLAY_MESSAGES = True

# End of user config


from sys import version_info
from subprocess import call, Popen

if not version_info[:2] == (3, 4):
    print("Installing Py3 using brew.\n")
    call(["brew", "update"])
    call(["brew", "install", "python3"])
    print("\nNext time, call this script using a Python3 interpreter.")
    exit(0)

try:
    from colorama import init, Fore, Back
    from docopt import docopt
    from pathlib import Path
except ImportError as e:
    module = str(e).split("'")[1]
    print("Module named %s missing: trying to install it." % module)
    call(["pip3", "install", module])
    print("\nPlease, launch hnorm again.")
    exit(0)


def message(message):
    if DISPLAY_MESSAGES:
        print(Fore.GREEN + "[!] " + Fore.RESET + message)


def warning(message):
    print(Fore.YELLOW + "[W] " + Fore.BLACK + Back.YELLOW + message)


def error(message):
    print(Fore.RED + "[E] " + Fore.RESET + Back.RED + message)


def auteur_users(folder):
    users = []
    auteur = folder/"auteur"
    if auteur.exists():
        with auteur.open() as f:
            users.extend(f.read().splitlines())
        if not users:
            error("`auteur` file is incomplete.")
    else:
        error("`auteur` file is missing.")
    return users


def main(args):
    init(autoreset=True)
    message("Welcome to the Honeybadger Program Checker")

    folder = Path(args['FOLDER'] or '.').resolve()
    message("The folder `%s` will be examinated." % str(folder))

    users = auteur_users(folder) + args["--user"]
    if len(users) > 1:
        message("The authors of this project are: %s." % ", ".join(users))
    elif users:
        message("The author of this project is: %s." % users[0])
    else:
        warning("No usernames availables, headers cannot be checked.")

    sources = sorted([s for s in folder.glob('**/*.[ch]') if s.is_file()],
                     key=lambda p: p.stat().st_size)
    amount_sources = len(sources)
    if amount_sources < 32:
        message("Found %d source files: %s." %
                (amount_sources, ", ".join(map(lambda p: p.name, sources))))
    else:
        message("Found %d source files." % amount_sources)


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    if not arguments["--changelog"]:
        main(arguments)
    else:
        print(__changes__)
