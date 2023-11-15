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
    parser.add_argument('--icon-names-from-file', action='append', default=[])
    parser.add_argument('source')
    parser.add_argument('dest')

    args = parser.parse_args()
    source = Path(args.source)
    dest = Path(args.dest)

    #: name with no extension => filename with which it is redundant
    already_have: typing.Dict[str, str] = {}
    #: name with no extension, -rtl or -symbolic suffix
    icon_names: typing.Set[str] = set()
    #: basename including extension => name with no extension, -rtl, -symbolic
    wanted: typing.Dict[str, str] = {}

    for name in args.icon_names_from_file:
        with open(name) as reader:
            for line in reader:
                icon_names.add(line.rstrip('\n'))

    for name in icon_names:
        for ext in EXTS:
            wanted[name + ext] = name

    for dirpath, dirnames, filenames in os.walk(dest / 'usr/share/icons'):
        rel = Path(dirpath).relative_to(dest)

        if 'cursors' in dirnames:
            dirnames.remove('cursors')

        for name in filenames:
            # remove up to 2 extensions (.symbolic.png), but do not
            # remove -rtl or -symbolic
            already_have[Path(Path(name).stem).stem] = rel / name

    for dirpath, dirnames, filenames in os.walk(source / 'usr/share/icons'):
        rel = Path(dirpath).relative_to(source)

        for name in filenames:
            if name in wanted:
                stem = Path(Path(name).stem).stem

                if stem in already_have:
                    print('# redundant: discard', name,
                          'in favour of', already_have[stem])
                    (source / rel / name).unlink()
                    icon_names.discard(wanted[name])
                    continue

                target = dest / rel / name

                if target.exists() or target.is_symlink():
                    print('# redundant:', str(rel / name))
                    (source / rel / name).unlink()
                    icon_names.discard(wanted[name])
                else:
                    print(rel / name)
                    icon_names.discard(wanted[name])
                    (dest / rel).mkdir(parents=True, exist_ok=True)
                    (source / rel / name).rename(target)
            else:
                print('# not in list of required icons:', str(rel / name))
                (source / rel / name).unlink()

    for name in icon_names:
        print('# not found:', name)
