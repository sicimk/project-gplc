"""
Panel for entering and managing conclusions
Works with UI elements already created in MainWindow
"""

import tkinter as tk


class ConclusionsPanel:
    """Handles the conclusions input and display logic"""

    def __init__(self, parent_window):
        """Initialize with reference to main window"""
        self.parent_window = parent_window
        self.conclusions = []

        # References will be set in setup()
        self.listbox = None
        self.entry = None
        self.add_button = None

    def setup(self):
        """Setup references to UI elements after they're created"""
        # Get references from parent window
        self.listbox = self.parent_window.conclusions_listbox
        self.entry = self.parent_window.conclusion_entry

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
            # Bind Enter key to add conclusion
            self.entry.bind('<Return>', lambda e: self._trigger_add_conclusion())

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

    def _trigger_add_conclusion(self):
        """Trigger the add conclusion callback if it exists"""
        if hasattr(self, '_add_callback') and self._add_callback:
            self._add_callback()

    def set_add_callback(self, callback):
        """Set the callback for adding conclusions"""
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

    def add_conclusion_to_list(self, conclusion_text):
        """Add conclusion to the displayed list"""
        if conclusion_text and conclusion_text != "Type here" and self.listbox:
            index = len(self.conclusions) + 1
            self.listbox.insert(tk.END, f"{index}. {conclusion_text}")
            self.conclusions.append(conclusion_text)
            self.clear_input()

    def clear_all(self):
        """Clear all conclusions"""
        if self.listbox:
            self.listbox.delete(0, tk.END)
        self.conclusions.clear()
        self.clear_input()

    def get_conclusion(self):
        """Get the current conclusion (last one added)"""
        return self.conclusions[-1] if self.conclusions else None

    def get_all_conclusions(self):
        """Get list of all conclusions"""
        return self.conclusions.copy()

    def get_conclusion_count(self):
        """Get number of conclusions"""
        return len(self.conclusions)