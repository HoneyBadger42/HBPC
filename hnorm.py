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

`
    Ce script vise a simplifier les corrections P2P.
    C'est en quelques sortes un wrapper pour le programme `norminette`
        offerte par le bocal.
    Il verifie les fichiers auteurs, les headers au dessus des fichiers,
        envoie les fichiers source a la norminette, en enfin,
        compile le rendu.
    Attention:
        Ce script n'est pas votre gourou! (Tout comme n'importe quel script,
        par ailleurs.) Il vous aide, mais il ne fait pas la correction a
        votre place. Il y aura surement des faux-positifs ou faux-positifs,
        c'est votre devoir de veiller a ce que tout se passe bien.
`

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
0.2:
    - Source file iteration
    - Added check for headers
    * TODO in get_header (returns arbitrary variable)

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

- Unit tests

- Translations/Shorter messages? (?)
"""

# User config:

DISPLAY_MESSAGES = True

# End of user config


from sys import version_info

if not version_info[:2] == (3, 4):
    print("Installing Py3 using brew.\n")
    call(["brew", "update"])
    call(["brew", "install", "python3"])
    print("\nNext time, call this script using a Python3 interpreter.")
    exit(0)


from pathlib import Path
import re
from time import sleep

try:
    from colorama import init, Fore, Back
    from docopt import docopt
except ImportError as e:
    module = str(e).split("'")[1]
    print("Module named %s missing: trying to install it." % module)
    call(["pip3", "install", module])
    print("\nPlease, launch hnorm again.")
    exit(0)


def message(message):
    sleep(0.3)
    if DISPLAY_MESSAGES:
        print(Fore.GREEN + "[!] " + Fore.RESET + message)


def warning(message):
    sleep(0.3)
    print(Fore.YELLOW + "[W] " + Fore.BLACK + Back.YELLOW + message)


def error(message):
    sleep(0.3)
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


header_regexp = [
    "^/\* \*{74} \*/$",
    "^/\* {76}\*/$",
    "^/\* {56}:::      ::::::::   \*/$",
    "^/\* {3}(.{50}) :\+: {6}:\+: {4}:\+: {3}\*/$",
    "^/\* {52}\+:\+ \+:\+ {9}\+:\+     \*/$",
    "\
^/\* {3}By: ([a-z-]{3,8}) <((.+)@.+)> {1,30}\+#\+  \+:\+ {7}\+#\+ {8}\*/$",
    "^/\* {48}\+#\+#\+#\+#\+#\+   \+#\+ {11}\*/$",
    "^/\* {3}Created: (\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) by ([a-z-]{3,8}) \
{10,15}#\+# {4}#\+# {13}\*/$",
    "^/\* {3}Updated: (\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) by ([a-z-]{3,8}) \
{9,14}###   ########\.fr {7}\*/$",
    "^/\* {76}\*/$",
    "^/\* \*{74} \*/",
]


def get_header(source):
    text = source.read()
    text_header = text.splitlines()[:11]
    if len(text_header) != 11:
        return None
    header = {}
    for line, regexp in zip(text_header, header_regexp):
        r = re.compile(regexp)
        if not r.match(line):
            return None
    header["created_by"] = "ldesgoui"
    return header


def check_source(path):
    source = path.open()
    header = get_header(source)
    if header:
        if users:
            pass
        elif 'created_by' in header:
            warning("Assuming %s as author" % header['created_by'])
            users.append(header['created_by'])
        message("Header of file %s was valid." % path.relative_to(folder))
    else:
        error("No valid header was found in %s" % path.relative_to(folder))
    source.close()


def main(args):
    global folder
    global users
    global sources

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
        warning("No usernames availables, headers cannot be checked properly.")

    sources = sorted((s for s in folder.glob('**/*.[ch]') if s.is_file()),
                     key=lambda p: p.stat().st_size,
                     reverse=True)
    amount_sources = len(sources)
    if 0 < amount_sources < 32:
        joined = ", ".join(map(lambda p: str(p.relative_to(folder)), sources))
        message("Found %d source files: %s." % (amount_sources, joined))
    elif sources:
        message("Found %d source files." % amount_sources)
    else:
        error("No source files were found.")

    for source in sources:
        check_source(source)


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    if not arguments["--changelog"]:
        main(arguments)
    else:
        print(__changes__)
