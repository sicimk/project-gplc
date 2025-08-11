"""
Shared mix-ins and tiny helpers used by several panels so we don’t
repeat ourselves.
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk


class FocusEntryMixin:
    """Mixin giving a panel: has_focus(), insert_at_cursor(text)."""

    _input: tk.Entry  # subclasses must create self._input

    # ------------------------------------------------------------------ #
    # called by InputController.handle_*_insert() to know where to paste #
    # ------------------------------------------------------------------ #
    def has_focus(self) -> bool:
        return self._input == self._input.focus_get()

    def insert_at_cursor(self, text: str):
        """Insert *text* at the current cursor position of the entry."""
        self._input.insert(self._input.index("insert"), text)


def labelled_frame(master: tk.Misc, title: str, **grid_opts):
    """
    Tiny convenience wrapper – returns a ttk.LabelFrame pre-gridded.
    """
    lf = ttk.LabelFrame(master, text=title)
    lf.grid(**grid_opts, sticky="nsew", padx=2, pady=2)
    return lf