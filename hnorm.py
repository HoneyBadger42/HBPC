#!/usr/bin/env python3
# **************************************************************************** #
#                                                                              #
#                    :::    :::  ::::::::  ::::    ::: :::::::::: :::   :::    #
#                   :+:    :+: :+:    :+: :+:+:   :+: :+:        :+:   :+:     #
#                  +:+    +:+ +:+    +:+ :+:+:+  +:+ +:+         +:+ +:+       #
#                 +#++:++#++ +#+    +:+ +#+ +:+ +#+ +#++:++#     +#++:         #
#                +#+    +#+ +#+    +#+ +#+  +#+#+# +#+           +#+           #
#               #+#    #+# #+#    #+# #+#   #+#+# #+#           #+#            #
#              ###    ###  ########  ###    #### ##########    ### -           #
#         #########      ###     #########   ########  ########## #########    #
#        #+#    #+#   #+# #+#   #+#    #+# #+#    #+# #+#        #+#    #+#    #
#       +#+    +#+  +#+   +#+  +#+    +#+ +#+        +#+        +#+    +#+     #
#      +:++#++:+  +:++#++:++# +:+    +#+ #:#        +:++#++:   +:++#++:#       #
#     +:+    +:+ +:+     +:+ +:+    +:+ +:+   +:+: +:+        +:+    +:+       #
#    :+:    :+: :+:     :+: :+:    :+: :+:    :+: :+:        :+:    :+:        #
#   :::::::::  :::     ::: :::::::::   ::::::::  :::::::::: :::    :::.fr      #
#                                                                              #
# **************************************************************************** #


""" Honeybadger Program Checker

Usage:
    hnorm [folder]
    hnorm -h | --help
    hnorm --version

Options:
    -h --help           Show this help screen.
    --version           Display the version.
    -u --user=<name>    Program author's username.
    -v --verbose        Enable verbose.
""" # PS: C'est pas a la norme.


__version__ = "0.1a"


from sys import version_info, stdout
from subprocess import call


def DEBUG(*args, **kwargs):
    pass


if not version_info[:2] == (3, 4):
    print("Installing Py3 using brew.\n")
    call(["brew" , "update"])
    call(["brew" , "install", "python3"])
    print("\nNext time, call this script using:\n./hnorm.py")
    exit(0)


try:
    from docopt import docopt
except ImportError as e:
    print(e, ": installing it.")
    call(["pip3" , "install", "docopt"])


def main(args):
    print(args)


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    main(arguments)
