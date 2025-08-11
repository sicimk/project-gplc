"""
Panel for displaying truth tables
Works with UI elements already created in MainWindow
"""

import tkinter as tk
from tkinter import ttk


class TruthTablePanel :
	"""Displays truth tables using Treeview widget"""

	def __init__(self, parent_window) :
		"""Initialize with reference to main window"""
		self.parent_window = parent_window
		self.headers = []
		self.rows = []

		# Reference will be set in setup()
		self.tree = None

	def setup(self) :
		"""Setup references to UI elements after they're created"""
		self.tree = self.parent_window.truth_table

	def clear(self) :
		"""Clear the truth table"""
		if not self.tree :
			return

		# Delete all items
		for item in self.tree.get_children() :
			self.tree.delete(item)

		# Clear columns
		self.tree['columns'] = []
		self.headers = []
		self.rows = []

	def set_headers(self, headers) :
		"""Set the column headers"""
		if not self.tree :
			return

		self.headers = headers
		self.tree['columns'] = headers

		# Configure columns
		for header in headers :
			self.tree.heading(header, text=header)
			# Auto-adjust column width based on header length
			width = max(80, len(header) * 10)
			self.tree.column(header, width=width, anchor='center')

	def add_row(self, values) :
		"""Add a row to the truth table"""
		if not self.tree :
			return

		# Convert boolean values to 1/0
		display_values = []
		for val in values :
			if isinstance(val, bool) :
				display_values.append('1' if val else '0')
			else :
				display_values.append(str(val))

		self.tree.insert('', 'end', values=display_values)
		self.rows.append(display_values)

	def populate_table(self, headers, rows) :
		"""Populate the entire table at once"""
		self.clear()
		self.set_headers(headers)

		for row in rows :
			self.add_row(row)

	def get_table_data(self) :
		"""Get the current table data"""
		return {
			'headers' : self.headers.copy(),
			'rows' : self.rows.copy()
			}

	def highlight_row(self, index) :
		"""Highlight a specific row"""
		if not self.tree :
			return

		items = self.tree.get_children()
		if 0 <= index < len(items) :
			self.tree.selection_set(items[index])
			self.tree.see(items[index])

	def export_to_text(self, filepath) :
		"""Export truth table to text file"""
		if not self.headers or not self.rows :
			raise ValueError("No truth table data to export")

		with open(filepath, 'w', encoding='utf-8') as f :
			# Write headers
			header_line = " | ".join(self.headers)
			f.write(header_line + "\n")
			f.write("-" * len(header_line) + "\n")

			# Write rows
			for row in self.rows :
				row_line = " | ".join(str(val) for val in row)
				f.write(row_line + "\n")

	def export_to_latex(self, filepath) :
		"""Export truth table to LaTeX format"""
		if not self.headers or not self.rows :
			raise ValueError("No truth table data to export")

		with open(filepath, 'w', encoding='utf-8') as f :
			# LaTeX table header
			f.write("\\begin{table}[h]\n")
			f.write("\\centering\n")
			f.write("\\begin{tabular}{" + "|c" * len(self.headers) + "|}\n")
			f.write("\\hline\n")

			# Headers
			header_line = " & ".join(
				self._escape_latex(h) for h in self.headers)
			f.write(header_line + " \\\\\n")
			f.write("\\hline\n")

			# Rows
			for row in self.rows :
				row_line = " & ".join(
					self._escape_latex(str(val)) for val in row)
				f.write(row_line + " \\\\\n")

			# Table footer
			f.write("\\hline\n")
			f.write("\\end{tabular}\n")
			f.write("\\caption{Truth Table}\n")
			f.write("\\label{tab:truth_table}\n")
			f.write("\\end{table}\n")

	def _escape_latex(self, text) :
		"""Escape special LaTeX characters"""
		replacements = {
			'&' : '\\&',
			'%' : '\\%',
			'$' : '\\$',
			'#' : '\\#',
			'_' : '\\_',
			'{' : '\\{',
			'}' : '\\}',
			'~' : '\\textasciitilde{}',
			'^' : '\\textasciicircum{}',
			'\\' : '\\textbackslash{}',
			'∧' : '\\land',
			'∨' : '\\lor',
			'¬' : '\\neg',
			'→' : '\\rightarrow',
			'↔' : '\\leftrightarrow',
			'⊕' : '\\oplus',
			'↑' : '\\uparrow',
			'↓' : '\\downarrow'
			}

		result = text
		for old, new in replacements.items() :
			result = result.replace(old, new)

		return result

	def get_selected_row(self) :
		"""Get the currently selected row index"""
		if not self.tree :
			return None

		selection = self.tree.selection()
		if selection :
			# Get the index of the selected item
			item = selection[0]
			items = self.tree.get_children()
			return items.index(item)

		return None

	def set_column_widths(self, widths) :
		"""Set specific column widths"""
		if not self.tree or not self.headers :
			return

		for i, (header, width) in enumerate(zip(self.headers, widths)) :
			self.tree.column(header, width=width)

	def auto_resize_columns(self) :
		"""Automatically resize columns to fit content"""
		if not self.tree or not self.headers :
			return

		for header in self.headers :
			# Get the maximum width needed
			max_width = len(header) * 10  # Header width

			# Check all row values
			col_index = self.headers.index(header)
			for row in self.rows :
				if col_index < len(row) :
					value_width = len(str(row[col_index])) * 10
					max_width = max(max_width, value_width)

			# Set column width with some padding
			self.tree.column(header, width=max_width + 20)

	def is_empty(self) :
		"""Check if the truth table is empty"""
		return len(self.rows) == 0

	def get_row_count(self) :
		"""Get the number of rows in the table"""
		return len(self.rows)

	def get_column_count(self) :
		"""Get the number of columns in the table"""
		return len(self.headers)
