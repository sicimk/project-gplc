"""
Controller for menu actions
Handles all menu bar interactions
"""

import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import webbrowser
import os


class MenuController:
    """
    Handles all menu bar actions
    """

    def __init__(self, menu_bar, main_controller):
        """
        Initialize menu controller

        Parameters:
            menu_bar: MenuBar instance
            main_controller: MainController instance
        """
        self.menu_bar = menu_bar
        self.main_controller = main_controller

        # Connect callbacks
        self._connect_callbacks()

    def _connect_callbacks(self) :
        """Connect menu callbacks"""
        # File menu
        self.menu_bar.set_new_callback(self.handle_new)
        self.menu_bar.set_open_callback(self.handle_open)
        self.menu_bar.set_save_callback(self.handle_save)
        self.menu_bar.set_save_as_callback(self.handle_save_as)
        self.menu_bar.set_export_proof_callback(self.handle_export_proof)
        self.menu_bar.set_export_table_callback(self.handle_export_table)
        self.menu_bar.set_exit_callback(self.handle_exit)

        # Edit menu
        self.menu_bar.set_clear_all_callback(
            self.main_controller.handle_clear_all)

        # Tools menu
        self.menu_bar.set_auto_mode_callback(
            lambda : self.handle_mode_change("automatic")
            )
        self.menu_bar.set_manual_mode_callback(
            lambda : self.handle_mode_change("manual")
            )

        # Help menu
        self.menu_bar.set_help_callback(self.handle_help)
        self.menu_bar.set_tutorial_callback(self.handle_tutorial)
        self.menu_bar.set_about_callback(self.handle_about)

    def handle_new(self):
        """Handle File > New"""
        # Check if there's unsaved work
        if self._check_unsaved_changes():
            self.main_controller.handle_clear_all()
            self.main_controller.current_file = None
            self.main_controller.error_controller.show_info("New project created")

    def handle_open(self):
        """Handle File > Open"""
        filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All files", "*.*")]
        )

        if filename:
            self.main_controller.handle_load_project(filename)

    def handle_save(self):
        """Handle File > Save"""
        if self.main_controller.current_file:
            self.main_controller.handle_save_project(
                self.main_controller.current_file
                )
        else:
            self.handle_save_as()

    def handle_save_as(self):
        """Handle File > Save As"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("All files", "*.*")]
        )
        if filename:
            self.main_controller.handle_save_project(filename)

    def handle_export_proof(self) :
        """Handle export proof"""
        # TODO: Implement proof export
        messagebox.showinfo("Export Proof",
                            "Proof export not yet implemented")

    def handle_export_table(self):
        """Handle File > Export > Truth Table"""
        # Check if table exists
        if self.main_controller.truth_table_panel.is_empty():
            self.main_controller.error_controller.show_error(
                "export", "No truth table to export. Generate a table first."
            )
            return

        # Show format selection dialog
        format_choice = self.menu_bar.show_export_format_dialog("table")

        if format_choice == "text" :
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
            if filename :
                self._export_table_text(filename)

        elif format_choice == "latex" :
            filename = filedialog.asksaveasfilename(
                defaultextension=".tex",
                filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")]
                )
            if filename :
                self._export_table_latex(filename)

    def handle_exit(self):
        """Handle File > Exit"""
        if self._check_unsaved_changes():
            self.main_controller.shutdown()
            self.main_controller.view.root.quit()

    def handle_clear_all(self):
        """Handle Edit > Clear All"""
        if messagebox.askyesno("Clear All",
                            "Are you sure you want to clear all data?"):
            self.main_controller.handle_clear_all()

    def handle_preferences(self):
        """Handle Edit > Preferences"""
        # Show preferences dialog
        prefs = self.menu_bar.show_preferences_dialog()

        if prefs:
            # Apply preferences
            # For now, we'll just show what was selected
            self.main_controller.error_controller.show_info(
                f"Preferences updated: Theme={prefs.get('theme', 'default')}, "
                f"Notation={prefs.get('notation', 'standard')}"
            )

    def handle_mode_change(self, mode):
        """Handle Tools > Mode Change"""
        self.main_controller.handle_mode_change(mode)

    def handle_help(self):
        """Handle Help > Help Documentation"""
        # Open help file or URL
        help_file = os.path.join(os.path.dirname(__file__), "..", "..",
                                 "docs", "user_manual.html")
        if os.path.exists(help_file):
            webbrowser.open(f"file://{os.path.abspath(help_file)}")
        else:
            self.main_controller.error_controller.show_info(
                "Help documentation can be found in the docs folder"
            )

    def handle_tutorial(self):
        """Handle Help > Tutorial"""
        # TODO: Launch tutorial
        messagebox.showinfo("Tutorial",
                           "Interactive tutorial coming soon!")

    def handle_about(self) :
        """Handle Help > About"""
        messagebox.showinfo(
            "About GPLC",
            "Graphical Propositional Logic Calculator\n\n"
            "Version 1.0.0\n"
            "Created by Silviu Ciobanica-Mkrtchyan\n"
            "Part of a final year, university project in Computer Science\n\n"
            "A tool for learning and applying propositional logic.\n\n"
            "Built with Python and Tkinter"
            )
    def _check_unsaved_changes(self):
        """
        Check if there are unsaved changes

        Returns:
            bool: True if ok to proceed, False to cancel
        """
        # For now, always return True
        # TODO: Implement change tracking
        return True

    def _export_table_text(self, filename):
        """Export truth table to text file"""
        try:
            self.main_controller.table_controller.export_to_text(filename)
            self.main_controller.error_controller.show_info(
                f"Truth table exported to {filename}"
            )
        except Exception as e:
            self.main_controller.error_controller.show_error(
                "export", f"Export failed: {str(e)}"
            )

    def _export_table_latex(self, filename):
        """Export truth table to LaTeX file"""
        try:
            self.main_controller.table_controller.export_to_latex(filename)
            self.main_controller.error_controller.show_info(
                f"Truth table exported to {filename}"
            )
        except Exception as e:
            self.main_controller.error_controller.show_error(
                "export", f"Export failed: {str(e)}"
            )