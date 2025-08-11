"""
Panel for entering and managing premises
Works with UI elements already created in MainWindow
"""

import tkinter as tk


class PremisesPanel:
    """Handles the premises input and display logic"""

    def __init__(self, parent_window):
        """Initialize with reference to main window"""
        self.parent_window = parent_window
        self.premises = []  # List of premise formulas

        # References will be set in setup()
        self.listbox = None
        self.entry = None
        self.add_button = None

    def setup(self):
        """Setup references to UI elements after they're created"""
        # Get references from parent window
        self.listbox = self.parent_window.premises_listbox
        self.entry = self.parent_window.premise_entry

        # Find the add button
        for widget in self.entry.master.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget('text') == 'Add to list':
                self.add_button = widget
                break

        # Clear default entries
        if self.listbox:
            self.listbox.delete(0, tk.END)

        # Bind entry events
        if self.entry:
            self.entry.bind('<FocusIn>', self._on_entry_focus)
            self.entry.bind('<FocusOut>', self._on_entry_unfocus)
            # Bind Enter key to add premise
            self.entry.bind('<Return>', lambda e: self._trigger_add_premise())

    def _on_entry_focus(self, event):
        """Clear placeholder text on focus"""
        if self.entry.get() == "Type here":
            self.entry.delete(0, tk.END)
            self.entry.config(fg='black')

    def _on_entry_unfocus(self, event):
        """Restore placeholder if empty"""
        if not self.entry.get():
            self.entry.insert(0, "Type here")
            self.entry.config(fg='gray')

    def _trigger_add_premise(self):
        """Trigger the add premise callback if it exists"""
        if hasattr(self, '_add_callback') and self._add_callback:
            self._add_callback()

    def set_add_callback(self, callback):
        """Set the callback for adding premises"""
        self._add_callback = callback
        if self.add_button:
            self.add_button.config(command=callback)

    def get_current_input(self):
        """Get current text in entry field"""
        if not self.entry:
            return ""
        text = self.entry.get()
        return "" if text == "Type here" else text

    def clear_input(self):
        """Clear the input field"""
        if self.entry:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Type here")
            self.entry.config(fg='gray')

    def add_premise_to_list(self, premise_text):
        """Add premise to the displayed list"""
        if premise_text and premise_text != "Type here" and self.listbox:
            index = len(self.premises) + 1
            self.listbox.insert(tk.END, f"{index}. {premise_text}")
            self.premises.append(premise_text)
            self.clear_input()

    def clear_all(self):
        """Clear all premises"""
        if self.listbox:
            self.listbox.delete(0, tk.END)
        self.premises.clear()
        self.clear_input()

    def get_all_premises(self):
        """Get list of all premises"""
        return self.premises.copy()

    def highlight_premise(self, index):
        """Highlight a specific premise"""
        if self.listbox and 0 <= index < self.listbox.size():
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.see(index)

    def get_premise_count(self):
        """Get number of premises"""
        return len(self.premises)