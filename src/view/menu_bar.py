"""
Menu bar implementation
Works with UI elements already created in MainWindow
"""

import tkinter as tk
from tkinter import messagebox


class MenuBar:
    """Menu bar with Options and Instructions menus"""

    def __init__(self, parent_window):
        """Initialize menu bar"""
        self.parent_window = parent_window

        # References will be set in setup()
        self.menu_frame = None
        self.options_btn = None
        self.instructions_btn = None

        # Callbacks (will be set by controller)
        self.callbacks = {
            'new': None,
            'open': None,
            'save': None,
            'save_as': None,
            'export_proof': None,
            'export_table': None,
            'exit': None,
            'clear_all': None,
            'preferences': None,
            'auto_mode': None,
            'manual_mode': None,
            'help': None,
            'tutorial': None,
            'about': None
        }

    def setup(self):
        """Setup references to UI elements after they're created"""
        self.menu_frame = self.parent_window.menu_frame

        # Get references to buttons created in main window
        if self.menu_frame:
            children = self.menu_frame.winfo_children()
            if len(children) >= 2:
                self.options_btn = children[0]
                self.instructions_btn = children[1]

                # Configure button commands
                self.options_btn.config(command=self._show_options_menu)
                self.instructions_btn.config(command=self._show_instructions_menu)

    def _show_options_menu(self):
        """Show options dropdown menu"""
        if not self.parent_window.root:
            return

        menu = tk.Menu(self.parent_window.root, tearoff=0)

        # File operations
        menu.add_command(label="New", command=self._safe_callback('new'))
        menu.add_command(label="Open...", command=self._safe_callback('open'))
        menu.add_command(label="Save", command=self._safe_callback('save'))
        menu.add_command(label="Save As...", command=self._safe_callback('save_as'))
        menu.add_separator()

        # Export submenu
        export_menu = tk.Menu(menu, tearoff=0)
        export_menu.add_command(label="Export Proof...",
                               command=self._safe_callback('export_proof'))
        export_menu.add_command(label="Export Truth Table...",
                               command=self._safe_callback('export_table'))
        menu.add_cascade(label="Export", menu=export_menu)
        menu.add_separator()

        # Other options
        menu.add_command(label="Clear All", command=self._safe_callback('clear_all'))
        menu.add_command(label="Preferences...", command=self._safe_callback('preferences'))
        menu.add_separator()
        menu.add_command(label="Exit", command=self._safe_callback('exit'))

        # Show menu below button
        if self.options_btn:
            x = self.options_btn.winfo_rootx()
            y = self.options_btn.winfo_rooty() + self.options_btn.winfo_height()
            menu.post(x, y)

    def _show_instructions_menu(self):
        """Show instructions dropdown menu"""
        if not self.parent_window.root:
            return

        menu = tk.Menu(self.parent_window.root, tearoff=0)

        menu.add_command(label="Help", command=self._safe_callback('help'))
        menu.add_command(label="Tutorial", command=self._safe_callback('tutorial'))
        menu.add_separator()
        menu.add_command(label="About GPLC", command=self._safe_callback('about'))

        # Show menu below button
        if self.instructions_btn:
            x = self.instructions_btn.winfo_rootx()
            y = self.instructions_btn.winfo_rooty() + self.instructions_btn.winfo_height()
            menu.post(x, y)

    def _safe_callback(self, action):
        """Return a safe callback that won't crash if not set"""
        def callback():
            if self.callbacks.get(action):
                try:
                    self.callbacks[action]()
                except Exception as e:
                    messagebox.showerror("Error", f"Action failed: {str(e)}")
            else:
                messagebox.showinfo("Not Implemented", f"{action.replace('_', ' ').title()} not yet implemented")
        return callback

    def set_callback(self, action, callback):
        """Set a callback for a menu action"""
        if action in self.callbacks:
            self.callbacks[action] = callback

    # Convenience methods for setting callbacks
    def set_new_callback(self, callback):
        self.callbacks['new'] = callback

    def set_open_callback(self, callback):
        self.callbacks['open'] = callback

    def set_save_callback(self, callback):
        self.callbacks['save'] = callback

    def set_save_as_callback(self, callback):
        self.callbacks['save_as'] = callback

    def set_export_proof_callback(self, callback):
        self.callbacks['export_proof'] = callback

    def set_export_table_callback(self, callback):
        self.callbacks['export_table'] = callback

    def set_exit_callback(self, callback):
        self.callbacks['exit'] = callback

    def set_clear_all_callback(self, callback):
        self.callbacks['clear_all'] = callback

    def set_preferences_callback(self, callback):
        self.callbacks['preferences'] = callback

    def set_auto_mode_callback(self, callback):
        self.callbacks['auto_mode'] = callback

    def set_manual_mode_callback(self, callback):
        self.callbacks['manual_mode'] = callback

    def set_help_callback(self, callback):
        self.callbacks['help'] = callback

    def set_tutorial_callback(self, callback):
        self.callbacks['tutorial'] = callback

    def set_about_callback(self, callback):
        self.callbacks['about'] = callback

    def show_export_format_dialog(self, export_type):
        """Show dialog to select export format"""
        return "text"  # Simplified for now