"""
Panel containing all control buttons
Works with UI elements already created in MainWindow
"""

import tkinter as tk


class ButtonPanel:
    """Manages all button controls in the middle section"""

    def __init__(self, parent_window):
        """Initialize with reference to main window"""
        self.parent_window = parent_window

        # Store button references
        self.rule_buttons = []
        self.action_buttons = {}
        self.proposition_buttons = {}
        self.connective_buttons = {}

    def setup(self):
        """Setup references to UI elements after they're created"""
        # This is called after the main window creates all UI elements
        # We don't need to do much here since MainController handles button connections
        pass

    def enable_rule_buttons(self):
        """Enable rule buttons for manual mode"""
        for btn in self.rule_buttons:
            if btn.winfo_exists():
                btn.config(state=tk.NORMAL)

    def disable_rule_buttons(self):
        """Disable rule buttons for automatic mode"""
        for btn in self.rule_buttons:
            if btn.winfo_exists():
                btn.config(state=tk.DISABLED)

    def add_rule_button(self, button):
        """Add a rule button to the list for enable/disable control"""
        self.rule_buttons.append(button)

    def register_action_button(self, name, button):
        """Register an action button"""
        self.action_buttons[name] = button

    def register_proposition_button(self, letter, button):
        """Register a proposition button"""
        self.proposition_buttons[letter] = button

    def register_connective_button(self, symbol, button):
        """Register a connective button"""
        self.connective_buttons[symbol] = button

    def get_button(self, button_type, identifier):
        """
        Get a specific button

        Parameters:
            button_type (str): 'action', 'proposition', 'connective', or 'rule'
            identifier (str): Button identifier

        Returns:
            tk.Button or None: The button widget if found
        """
        if button_type == 'action':
            return self.action_buttons.get(identifier)
        elif button_type == 'proposition':
            return self.proposition_buttons.get(identifier)
        elif button_type == 'connective':
            return self.connective_buttons.get(identifier)
        return None

    def is_button_enabled(self, button_type, identifier):
        """Check if a button is enabled"""
        button = self.get_button(button_type, identifier)
        if button and button.winfo_exists():
            return button.cget('state') == tk.NORMAL
        return False

    def show_export_dialog(self):
        """Show export format selection dialog"""
        dialog = tk.Toplevel(self.parent_window.root)
        dialog.title("Export Format")
        dialog.geometry("300x150")
        dialog.transient(self.parent_window.root)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 300) // 2
        y = (dialog.winfo_screenheight() - 150) // 2
        dialog.geometry(f"300x150+{x}+{y}")

        result = tk.StringVar()

        tk.Label(dialog, text="Select export format:",
                font=('Arial', 12)).pack(pady=10)

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Text (.txt)", width=15,
                 command=lambda: [result.set("text"), dialog.destroy()]).pack(pady=5)

        tk.Button(btn_frame, text="LaTeX (.tex)", width=15,
                 command=lambda: [result.set("latex"), dialog.destroy()]).pack(pady=5)

        tk.Button(btn_frame, text="Cancel", width=15,
                 command=lambda: [result.set(""), dialog.destroy()]).pack(pady=5)

        dialog.wait_window()
        return result.get() if result.get() else None