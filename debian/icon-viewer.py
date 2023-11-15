#!/usr/bin/python3

import sys
import typing
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from gi.repository import Gtk


class IconViewerWindow(Gtk.Window):
    def __init__(
        self,
        icons: typing.Sequence[str],
    ) -> None:
        super().__init__()

        self.set_default_size(400, 300)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        size_combo = Gtk.ComboBoxText()
        self.__images: typing.List[Gtk.Image] = []

        for size in [8, 16, 22, 24, 32, 48, 64, 96, 128, 256, 512]:
            size_combo.append_text(str(size))

        box.pack_start(size_combo, False, False, 6)

        scrolled = Gtk.ScrolledWindow()
        box.pack_end(scrolled, True, True, 6)
        grid = Gtk.Grid(column_spacing=12, row_spacing=12)
        scrolled.add(grid)
        row = 0

        for icon in icons:
            image = Gtk.Image(icon_name=icon)
            self.__images.append(image)
            grid.attach(image, 0, row, 1, 1)
            label = Gtk.Label.new(icon)
            grid.attach(label, 1, row, 1, 1)
            row += 1

        size_combo.connect('changed', self.__size_changed_cb)
        size_combo.set_active(0)
        self.show_all()

    def __size_changed_cb(
        self,
        combo: Gtk.ComboBoxText,
    ) -> None:
        size = int(combo.get_active_text())

        for image in self.__images:
            image.props.pixel_size = size


class IconViewer(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id='org.debian.packages.adwaita_icon_theme.IconViewer',
            flags=(
                Gio.ApplicationFlags.NON_UNIQUE
                | Gio.ApplicationFlags.HANDLES_OPEN
            ),
        )

    def do_activate(self) -> None:
        pardir = Path(__file__).resolve().parent
        icons: typing.List[str] = []

        with open(pardir / 'legacy-icons-41.txt') as reader:
            for line in reader:
                icons.append(line.strip())

        with open(pardir / 'removed-icons-41.txt') as reader:
            for line in reader:
                icons.append(line.strip())

        self.add_window(IconViewerWindow(icons))

    def do_open(
        self,
        files: typing.Sequence[Gio.File],
        n_files: int,
        hint: str,
    ) -> None:
        assert len(files) == n_files
        pardir = Path(__file__).resolve().parent
        icons = []
        icons: typing.List[str] = []

        for file in files:
            with open(file.get_path()) as reader:
                for line in reader:
                    icons.append(line.strip())

        self.add_window(IconViewerWindow(icons))


if __name__ == '__main__':
    raise SystemExit(IconViewer().run(sys.argv))
