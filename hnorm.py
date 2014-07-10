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

__version__ = "0.3"
__changes__ = """\
0.3:
    - Updated get_header
    - Multithreaded check_source
    - Added checking for logins in header
    - Calling make at the end of script

0.2a:
    - Removed useless header parsing
    - Added calls to norminette
    * TODO get_header

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

from subprocess import call, Popen, PIPE
from sys import version_info

if not version_info[:2] == (3, 4):
    print("Installing Py3 using brew.\n")
    call(["brew", "update"])
    call(["brew", "install", "python3"])
    print("\nNext time, call this script using a Python3 interpreter.")
    exit(0)


from multiprocessing.dummy import Pool
from pathlib import Path
import re
from time import sleep

try:
    from colorama import Fore, Back, init as color_init
    from docopt import docopt
except ImportError as e:
    module = str(e).split("'")[1]
    print("Module named %s missing: trying to install it." % module)
    call(["pip3", "install", module])
    print("\nPlease, launch hnorm again.")
    exit(0)


def message(message):
    print("%s[!]%s %s" % (Back.GREEN, Back.RESET, message))


def warning(message):
    print("%s[W]%s %s" % (Back.YELLOW + Fore.BLACK,
                          Back.RESET + Fore.RESET,
                          message))


def error(message):
    print("%s[E]%s %s" % (Back.RED, Back.RESET, message))


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

header_regexp = {
    3: re.compile("^/\* {3}(.{50}) :\+: {6}:\+: {4}:\+: {3}\*/$"),
    5: re.compile("^/\* {3}By: ([a-z-]{3,8}) <.+@.+> {1,30}\+#\+  \+:\+ \
{7}\+#\+ {8}\*/$"),
    7: re.compile("^/\* {3}Created: \d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} by \
([a-z-]{3,8}) {10,15}#\+# {4}#\+# {13}\*/$"),
    8: re.compile("^/\* {3}Updated: \d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} by \
([a-z-]{3,8}) {9,14}###   ########\.fr {7}\*/$"),
}


def get_header(path):
    source = path.open()
    text = source.read().splitlines()
    header = {}
    header["filename"] = header_regexp[3].findall(text[3])[0].strip()
    header["author"] = header_regexp[5].findall(text[5])[0].strip()
    header["created_by"] = header_regexp[7].findall(text[7])[0].strip()
    header["updated_by"] = header_regexp[8].findall(text[8])[0].strip()
    source.close()
    return header


def check_source(path):
    relative_path = path.relative_to(Path().resolve())
    proc = Popen(["norminette", str(relative_path)], stdout=PIPE)
    while proc.poll() is None:
        sleep(0.1)
    stdin, _ = proc.communicate()
    errors = list(map(lambda x: x.decode("utf-8"), stdin.splitlines()))
    fuck = "Norme: %s" % relative_path
    if fuck in errors:
        errors.remove(fuck)
    if "Error: 42 header not at top of the file" not in errors:
        header = get_header(path)
    else:
        header = None
    result = {"errors": errors, "path": path, "header": header}
    return result


def main(args):
    global folder
    global sources

    color_init(autoreset=True)
    message("Welcome to the Honeybadger Program Checker")

    folder = Path(args["FOLDER"] or ".").resolve()
    message("The folder `%s` will be examinated." % str(folder))

    users = auteur_users(folder) + args["--user"]
    if len(users) > 1:
        message("The authors of this project are: %s." % ", ".join(users))
    elif users:
        message("The author of this project is: %s." % users[0])
    else:
        warning("No usernames availables, headers cannot be checked properly.")

    sources = sorted((s for s in folder.glob("**/*.[ch]") if s.is_file()),
                     key=lambda p: p.stat().st_size,
                     reverse=True)
    amount_sources = len(sources)
    if 0 < amount_sources < 32:
        joined = ", ".join(map(lambda p: str(p.relative_to(folder)), sources))
        message("Found %d source files: %s." % (amount_sources, joined))
        pool_size = amount_sources
    elif sources:
        message("Found %d source files." % amount_sources)
        pool_size = 32
    else:
        error("No source files were found.")
    pool = Pool(pool_size)  # TODO: Make it faster :(
    results = pool.map(check_source, sources)
    pool.close()
    pool.join()
    for result in results:
        if result["header"]:
            message("File %s: (%s | %s | %s)" % (
                result["path"].relative_to(folder),
                result["header"]["author"],
                result["header"]["created_by"],
                result["header"]["updated_by"],
                ))
            if (result["header"]["filename"] != result["path"].name):
                error(" -- The header's filename differs in the header")
            if users and (result["header"]["author"] not in users
                          or result["header"]["created_by"] not in users
                          or result["header"]["updated_by"] not in users):
                error(" -- Login in header differs from allowed authors")
        else:
            message("File %s:" % result["path"].relative_to(folder))
        for error_message in result["errors"]:
            error(" --  " + error_message)
    message("End of script, calling make")
    if folder == Path(".").resolve():
        make_args = ["make"]
    else:
        make_args = ["make", "-C", str(folder.relative_to(Path().resolve()))]
    make = Popen(make_args)
    while make.poll() is None:
        sleep(0.1)
    exit(0)


if __name__ == "__main__":
    arguments = docopt(__doc__, version=__version__)
    if not arguments["--changelog"]:
        main(arguments)
    else:
        print(__changes__)
