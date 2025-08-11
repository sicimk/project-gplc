"""
Main controller coordinating all application logic
Manages the interaction between model and view components
"""

import tkinter as tk
from model.validator import FormulaValidator
from model.proof_system import ProofSystem
from model.truth_table import TruthTable
from model.file_exporter import FileExporter
from model.formula import Formula


class MainController:
    """
    Main controller that coordinates all application components
    """

    def __init__(self):
        """Initialize main controller"""
        # Model layer components
        self.validator = FormulaValidator()
        self.proof_system = ProofSystem()
        self.truth_table = TruthTable()
        self.file_exporter = FileExporter()

        # View reference (will be set by main.py)
        self.view = None

        # Sub-controllers (will be initialized after view is set)
        self.input_controller = None
        self.proof_controller = None
        self.button_controller = None
        self.table_controller = None
        self.error_controller = None
        self.menu_controller = None

        # Application state
        self.current_mode = "automatic"  # automatic or manual

    def set_view(self, view):
        """
        Set the main view and initialize sub-controllers

        Parameters:
            view: ViewWrapper instance containing all panels
        """
        self.view = view

        # Import here to avoid circular dependencies
        from controller.input_controller import InputController
        from controller.proof_controller import ProofController
        from controller.button_controller import ButtonController
        from controller.table_controller import TableController
        from controller.error_controller import ErrorController
        from controller.menu_controller import MenuController

        # Initialize sub-controllers
        self.error_controller = ErrorController(view.error_display)

        self.input_controller = InputController(
            self.validator,
            self.proof_system,
            view.premises_panel,
            view.conclusions_panel,
            view.error_display
        )

        self.proof_controller = ProofController(
            self.proof_system,
            view.proof_steps_panel,
            view.error_display
        )

        self.button_controller = ButtonController(
            view.button_panel,
            self
        )

        self.table_controller = TableController(
            self.truth_table,
            view.truth_table_panel,
            self.file_exporter,
            self.error_controller,
        )

        self.menu_controller = MenuController(
            view.menu_bar,
            self
        )

        # Connect button callbacks
        self._connect_button_callbacks()
        self._connect_add_buttons()

        # Set initial mode
        self.handle_mode_change(self.current_mode)

    def _connect_button_callbacks(self):
        """Connect all button callbacks to their handlers"""
        # Get the main window to access actual buttons
        main_window = self.view.main_window

        # Connect atomic proposition buttons (A-Z)
        # These are created in main_window.py in the middle section
        try:
            # Find all letter buttons in the atomic propositions section
            for widget in main_window.middle_frame.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for button in child.winfo_children():
                                if isinstance(button, tk.Button):
                                    text = button.cget('text')
                                    if len(text) == 1 and text.isupper() and text.isalpha():
                                        button.config(command=lambda t=text: self.handle_proposition_click(t))
        except:
            pass

        # Connect logical connective buttons
        try:
            connective_map = {
                '∧': '∧', '∨': '∨', '¬': '¬', '→': '→', '↔': '↔',
                '⊕': '⊕', '↑': '↑', '↓': '↓', '(': '(', ')': ')'
            }

            for widget in main_window.middle_frame.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for button in child.winfo_children():
                                if isinstance(button, tk.Button):
                                    text = button.cget('text')
                                    if text in connective_map:
                                        button.config(command=lambda t=text: self.handle_connective_click(t))
        except:
            pass

        # Connect main action buttons
        try:
            for widget in main_window.middle_frame.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for button in widget.winfo_children():
                        if isinstance(button, tk.Button):
                            text = button.cget('text')
                            if 'EXECUTE PROOF' in text:
                                button.config(command=self.handle_execute_proof)
                            elif 'Generate Truth Table' in text:
                                button.config(command=self.handle_generate_table)
                            elif 'Export truth table' in text:
                                button.config(command=self.handle_export)
                            elif 'CLEAR ALL' in text:
                                button.config(command=self.handle_clear_all)
        except:
            pass

        # Connect premise and conclusion add buttons
        try:
            # Find and connect premise add button
            for widget in main_window.top_frame.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Button) and child.cget('text') == 'Add to list':
                            # Check if this is the premise button (by looking at parent)
                            parent_text = child.master.master.cget('text') if hasattr(child.master.master, 'cget') else ''
                            if 'Premises' in parent_text:
                                child.config(command=self.input_controller.handle_add_premise)
                            elif 'Conclusion' in parent_text:
                                child.config(command=self.input_controller.handle_add_conclusion)
        except:
            pass

        # Connect mode radio buttons
        if hasattr(main_window, 'mode_var'):
            main_window.mode_var.trace('w', lambda *args: self.handle_mode_change(main_window.mode_var.get()))

    def _connect_add_buttons(self) :
        """Connect the Add to list buttons for premises and conclusions"""
        # Connect premise add button
        self.view.premises_panel.set_add_callback(
            self.input_controller.handle_add_premise)

        # Connect conclusion add button
        self.view.conclusions_panel.set_add_callback(
            self.input_controller.handle_add_conclusion)

    def handle_mode_change(self, mode):
        """
        Handle switching between automatic and manual modes

        Parameters:
            mode (str): "automatic" or "manual"
        """
        self.current_mode = mode
        self.proof_controller.set_mode(mode)

        if mode == "automatic":
            self.error_controller.show_info("Switched to Automatic mode")
        else:
            self.error_controller.show_info("Switched to Manual mode")

    def handle_execute_proof(self):
        """Handle Execute Proof button click"""
        try:
            if not self.proof_system.premises:
                self.error_controller.show_error("proof", "No premises provided")
                return

            if not self.proof_system.conclusion:
                self.error_controller.show_error("proof", "No conclusion set")
                return

            if self.current_mode == "automatic":
                success, msg = self.proof_controller.execute_automatic_proof()
                if success:
                    self.error_controller.show_info("Proof complete!")
                    self.view.proof_steps_panel.set_result("Conclusion is VALID", "green")
                else:
                    self.error_controller.show_error("proof", msg)
                    self.view.proof_steps_panel.set_result("Conclusion is FALSE", "red")
            else:
                self.proof_controller.refresh_display()
                self.error_controller.show_info("Manual mode: Select steps and apply rules")

        except Exception as e:
            self.error_controller.show_error("execution", str(e))

    def handle_generate_table(self):
        """Handle Generate Truth Table button click"""
        try:
            if self.proof_system.proof_steps:
                success, msg = (
                    self.table_controller.generate_from_proof(self.proof_system))
            else:
                # Generate from premises and conclusion
                formulas = list(self.proof_system.premises)
                if self.proof_system.conclusion:
                    formulas.append(self.proof_system.conclusion)

                if not formulas:
                    self.error_controller.show_error("validation",
                                                     "No formulas to generate table from")
                    return

                success, msg = self.table_controller.generate_from_formulas(formulas)

            if success:
                self.error_controller.show_info(msg)
            else:
                self.error_controller.show_error("table", msg)

        except Exception as e:
            self.error_controller.show_error("table", str(e))

    def handle_export(self):
        """Handle Export button click"""
        try:
            if self.table_controller.is_empty():
                self.error_controller.show_error("export", "No truth table to export")
                return

            # Show simple export dialog
            from tkinter import filedialog, messagebox

            # Ask for format
            format_choice = messagebox.askyesno("Export Format",
                                                "Export as LaTeX? (No = Text format)")

            if format_choice:
                # LaTeX export
                filename = filedialog.asksaveasfilename(
                    defaultextension=".tex",
                    filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")]
                )
                if filename:
                    success, msg = self.table_controller.export_to_latex(filename)
            else:
                # Text export
                filename = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
                if filename:
                    success, msg = self.table_controller.export_to_text(filename)

                    if filename:
                        if success:
                            self.error_controller.show_info(msg)
                        else:
                            self.error_controller.show_error("export", msg)

        except Exception as e:
            self.error_controller.show_error("export", str(e))

    def handle_clear_all(self):
        """Handle Clear All button click"""
        from tkinter import messagebox

        if messagebox.askyesno("Clear All", "Are you sure you want to clear all data?"):
            # Clear model
            self.proof_system.clear()
            self.truth_table.clear()

            # Clear views
            self.view.premises_panel.clear_all()
            self.view.conclusions_panel.clear_all()
            self.view.proof_steps_panel.clear_all()
            self.view.truth_table_panel.clear()

            # Clear input controller state
            self.input_controller.clear_all()

            self.error_controller.show_info("All data cleared")

    def handle_proposition_click(self, letter):
        """Handle atomic proposition button click"""
        focused = self.view.root.focus_get()

        if focused == self.view.premises_panel.entry:
            if focused.get() == "Type here":
                focused.delete(0, tk.END)
                focused.config(fg='black')
            focused.insert(tk.INSERT, letter)
        elif focused == self.view.conclusions_panel.entry:
            if focused.get() == "Type here":
                focused.delete(0, tk.END)
                focused.config(fg='black')
            focused.insert(tk.INSERT, letter)

    def handle_connective_click(self, symbol):
        """Handle logical connective button click"""
        focused = self.view.root.focus_get()

        if focused == self.view.premises_panel.entry:
            if focused.get() == "Type here":
                focused.delete(0, tk.END)
                focused.config(fg='black')
            if symbol not in ['(', ')']:
                focused.insert(tk.INSERT, f" {symbol} ")
            else:
                focused.insert(tk.INSERT, symbol)
        elif focused == self.view.conclusions_panel.entry:
            if focused.get() == "Type here":
                focused.delete(0, tk.END)
                focused.config(fg='black')
            if symbol not in ['(', ')']:
                focused.insert(tk.INSERT, f" {symbol} ")
            else:
                focused.insert(tk.INSERT, symbol)

    def start_application(self):
        """Start the application"""
        if not self.view:
            raise RuntimeError("View not set. Call set_view() first.")

        self.error_controller.show_info("Welcome to GPLC! Enter premises and conclusions to begin.")
        self.view.root.update_idletasks()

    def shutdown(self):
        """Clean shutdown of the application"""
        pass