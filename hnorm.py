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
0.1a:
    - Script base
    - Cool Honeybadger header
"""

from sys import version_info
from subprocess import call, Popen

if not version_info[:2] == (3, 4):
    print("Installing Py3 using brew.\n")
    call(["brew", "update"])
    call(["brew", "install", "python3"])
    print("\nNext time, call this script using a Python3 interpreter.")
    exit(0)

try:
    from colorama import init
    from docopt import docopt
    from pathlib import Path
except ImportError as e:
    module = str(e).split("'")[1]
    print("Module named %s missing: trying to install it." % module)
    call(["pip3", "install", module])
    print("\nPlease, launch hnorm again.")
    exit(0)


def auteur_users(folder):
    users = []
    auteur = folder/"auteur"
    if auteur.exists():
        with auteur.open() as f:
            users.extend(f.read().splitlines())
    return users


def main(args):
    errors = []
    folder = Path(args['FOLDER'] or '.')
    users = auteur_users(folder)
    if not users:
        errors.append("`auteur` file is invalid.")
    users.extend(args["--user"])
    if not users:
        errors.append("No usernames availables, headers cannot be checked.")


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    if not arguments["--changelog"]:
        main(arguments)
    else:
        print(__changes__)
