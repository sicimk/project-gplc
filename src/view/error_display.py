"""
Error display overlay or status bar
Works with UI elements already created in MainWindow
"""

import tkinter as tk


class ErrorDisplay:
    """Displays errors and notifications to the user"""

    def __init__(self, parent_window):
        """Initialize error display"""
        self.parent_window = parent_window
        self.current_errors = {}

        # References will be set in setup()
        self.status_bar = None
        self.status_label = None
        self.error_icon = None
        self.error_panel = None

    def setup(self):
        """Create the status bar after main window is created"""
        # Create a status bar at the bottom of the window
        self.status_bar = tk.Frame(self.parent_window.root, bg='#f0f0f0', height=25)
        self.status_bar.grid(row=4, column=0, sticky='ew', padx=2, pady=2)
        self.status_bar.grid_propagate(False)

        # Status label
        self.status_label = tk.Label(self.status_bar, text="Ready",
                                    font=('Arial', 9), bg='#f0f0f0',
                                    anchor='w')
        self.status_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Error icon (initially hidden)
        self.error_icon = tk.Label(self.status_bar, text="⚠",
                                  font=('Arial', 12), fg='red',
                                  bg='#f0f0f0')

    def show_error(self, message, error_type=None):
        """Display an error message"""
        if not self.status_label:
            return

        self.current_errors[error_type] = message

        # Update status bar
        self.status_label.config(text=f"Error: {message}", fg='red')
        if self.error_icon:
            self.error_icon.pack(side=tk.RIGHT, padx=10)

        # Show floating panel for detailed errors
        if len(message) > 50:
            self._show_error_panel(message)

    def show_warning(self, message):
        """Display a warning message"""
        if self.status_label:
            self.status_label.config(text=f"Warning: {message}", fg='orange')

    def show_info(self, message):
        """Display an info message"""
        if self.status_label:
            self.status_label.config(text=message, fg='black')
        if self.error_icon:
            self.error_icon.pack_forget()

    def clear(self, error_type):
        """Clear a specific error"""
        if error_type in self.current_errors:
            del self.current_errors[error_type]

        if not self.current_errors:
            if self.status_label:
                self.status_label.config(text="Ready", fg='black')
            if self.error_icon:
                self.error_icon.pack_forget()
            if self.error_panel:
                self.error_panel.destroy()
                self.error_panel = None

    def clear_all_errors(self):
        """Clear all errors"""
        self.current_errors.clear()
        if self.status_label:
            self.status_label.config(text="Ready", fg='black')
        if self.error_icon:
            self.error_icon.pack_forget()
        if self.error_panel:
            self.error_panel.destroy()
            self.error_panel = None

    def _show_error_panel(self, message):
        """Show floating error panel for detailed messages"""
        if self.error_panel:
            self.error_panel.destroy()

        self.error_panel = tk.Toplevel(self.parent_window.root)
        self.error_panel.title("Error Details")
        self.error_panel.geometry("400x200")
        self.error_panel.transient(self.parent_window.root)

        # Center the panel
        self.error_panel.update_idletasks()
        x = (self.error_panel.winfo_screenwidth() - 400) // 2
        y = (self.error_panel.winfo_screenheight() - 200) // 2
        self.error_panel.geometry(f"400x200+{x}+{y}")

        # Error message
        text = tk.Text(self.error_panel, wrap=tk.WORD, font=('Arial', 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert('1.0', message)
        text.config(state=tk.DISABLED)

        # Close button
        tk.Button(self.error_panel, text="Close",
                 command=self.error_panel.destroy).pack(pady=5)