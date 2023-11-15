#!/usr/bin/python3

import argparse
import os
import typing
from pathlib import Path

EXTS = (
    '.png',
    '-rtl.png',
    '.svg',
    '-symbolic.symbolic.png',
    '-symbolic.svg',
    '-symbolic-rtl.svg',
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sysroot')

    args = parser.parse_args()
    sysroot = Path(args.sysroot)

    #: name with no extension, -rtl or -symbolic suffix
    available: typing.Set[str] = set()

    for dirpath, dirnames, filenames in os.walk(sysroot / 'usr/share/icons'):
        if 'cursors' in dirnames:
            dirnames.remove('cursors')

        for name in filenames:
            # remove up to 2 extensions (.symbolic.png), but do not
            # remove -rtl or -symbolic
            name = Path(Path(name).stem).stem
            available.add(name)

    print(f'# icons in {sysroot}:')

    for name in sorted(available):
        print(name)

    print('')
