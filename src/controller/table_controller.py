"""
Controller for truth table generation and display
Manages truth table operations and export functionality
"""


class TableController:
    """
    Controls truth table generation, display, and export
    """

    def __init__(self, truth_table, truth_table_panel, file_exporter, error_controller):
        """
        Initialize truth table controller

        Parameters:
            truth_table: TruthTable instance from model
            truth_table_panel: TruthTablePanel instance from view
            file_exporter: FileExporter instance
            error_controller: ErrorController instance
        """
        self.truth_table = truth_table
        self.truth_table_panel = truth_table_panel
        self.file_exporter = file_exporter
        self.error_controller = error_controller

    def generate_from_proof(self, proof_system):
        """Generate truth table from proof system"""
        try:
            success, msg = self.truth_table.generate_from_proof(proof_system)
            if success:
                self._update_view()
            return success, msg
        except Exception as e:
            return False, str(e)

    def generate_from_formulas(self, formulas):
        """Generate truth table from list of formulas"""
        try:
            success, msg = self.truth_table.generate_from_formulas(formulas)
            if success:
                self._update_view()
            return success, msg
        except Exception as e:
            return False, str(e)

    def _update_view(self):
        """Update the view with current table data"""
        # Get table data
        data = self.truth_table.get_table_data()

        if data['is_empty']:
            self.truth_table_panel.clear()
            return

        # Display the table
        self.truth_table_panel.populate_table(data['headers'], data['rows'])

    def export_to_text(self, filepath=None):
        """Export truth table to text file"""
        if not filepath:
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

        if filepath:
            try:
                success, msg = self.truth_table.export_to_text(filepath)
                return success, msg
            except Exception as e:
                return False, str(e)

        return False, "Export cancelled"

    def export_to_latex(self, filepath=None):
        """Export truth table to LaTeX file"""
        if not filepath:
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".tex",
                filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")]
            )

        if filepath:
            try:
                success, msg = self.truth_table.export_to_latex(filepath)
                return success, msg
            except Exception as e:
                return False, str(e)

        return False, "Export cancelled"

    def clear(self):
        """Clear the truth table display"""
        self.truth_table.clear()
        self.truth_table_panel.clear()

    def is_empty(self):
        """Check if truth table is empty"""
        return not self.truth_table.is_generated

    def get_table_info(self):
        """
        Get information about the current table

        Returns:
            dict: Table information
        """
        if not self.truth_table.is_generated:
            return {
                'is_generated': False,
                'num_variables': 0,
                'num_rows': 0,
                'num_formulas': 0
            }

        data = self.truth_table.get_table_data()

        # Count atomic propositions
        num_vars = len(self.truth_table.atomic_props)

        # Count formulas (total columns minus atomic props)
        num_formulas = len(data['headers']) - num_vars

        return {
            'is_generated': True,
            'num_variables': num_vars,
            'num_rows': len(data['rows']),
            'num_formulas': num_formulas
        }