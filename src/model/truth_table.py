"""
Truth table generation and manipulation
Generates truth tables for logical formulas and proof systems
"""

from itertools import product
from typing import List, Dict, Optional, Tuple


from model.formula import Formula

class TruthTable :
	"""
	Generates and manages truth tables for logical formulas
	"""

	def __init__(self) :
		"""
		Initialize truth table generator
		"""
		self.headers = []  # Column headers
		self.rows = []  # Table rows
		self.formulas = []  # Formula objects
		self.atomic_props = []  # List of atomic propositions
		self.is_generated = False

	def clear(self) :
		"""Clear all table data"""
		self.headers = []
		self.rows = []
		self.formulas = []
		self.atomic_props = []
		self.is_generated = False

	def generate_from_proof(self, proof_system) :
		"""
		Generate truth table from a proof system

		Parameters:
			proof_system: ProofSystem object with premises and steps

		Returns:
			tuple: (success, message)
		"""
		# Clear existing data
		self.clear()

		# Collect all unique formulas from the proof
		formula_strings = set()
		formulas_list = []

		# Add premises
		for premise in proof_system.premises :
			formula_str = str(premise)
			if formula_str not in formula_strings :
				formula_strings.add(formula_str)
				formulas_list.append(premise)

		# Add formulas from proof steps (excluding premises to avoid duplicates)
		for step in proof_system.proof_steps :
			if step.justification != "Premise" :
				formula_str = str(step.formula)
				if formula_str not in formula_strings :
					formula_strings.add(formula_str)
					formulas_list.append(step.formula)

		# Add conclusion if set and not already included
		if proof_system.conclusion :
			conclusion_str = str(proof_system.conclusion)
			if conclusion_str not in formula_strings :
				formula_strings.add(conclusion_str)
				formulas_list.append(proof_system.conclusion)

		# Generate table from formulas
		return self.generate_from_formulas(formulas_list)

	def generate_from_formulas(self, formulas) :
		"""
		Generate truth table from a list of formulas

		Parameters:
			formulas: List of Formula objects

		Returns:
			tuple: (success, message)
		"""
		if not formulas :
			return False, "No formulas provided"

		# Clear existing data
		self.clear()

		self.formulas = formulas.copy()

		# Collect all atomic propositions
		all_props = set()
		for formula in formulas :
			all_props.update(formula.get_atomic_propositions())

		# Sort propositions alphabetically
		self.atomic_props = sorted(list(all_props))

		if not self.atomic_props :
			# Handle case with no atomic propositions (e.g., tautologies/contradictions)
			# Still need to evaluate the formulas
			self._generate_headers()
			# Single row with empty truth assignment
			self._add_row({})
		else :
			# Generate headers
			self._generate_headers()

			# Generate all possible truth value combinations
			n_props = len(self.atomic_props)

			# Generate 2^n rows
			for values in product([True, False], repeat=n_props) :
				truth_assignment = dict(zip(self.atomic_props, values))
				self._add_row(truth_assignment)

		self.is_generated = True
		return True, f"Generated truth table with {len(self.rows)} rows"

	def _generate_headers(self) :
		"""Generate column headers for the table"""
		# Start with atomic propositions
		self.headers = self.atomic_props.copy()

		# Add formula columns
		for formula in self.formulas :
			self.headers.append(str(formula))

	def _add_row(self, truth_assignment) :
		"""
		Add a row to the truth table

		Parameters:
			truth_assignment (dict): Mapping of propositions to truth values
		"""
		row = []

		# Add atomic proposition values
		for prop in self.atomic_props :
			row.append(truth_assignment.get(prop, True))

		# Evaluate each formula
		for formula in self.formulas :
			try :
				value = formula.evaluate(truth_assignment)
				row.append(value)
			except Exception :
				# If evaluation fails, use None
				row.append(None)

		self.rows.append(row)

	def get_table_data(self) :
		"""
		Get truth table data for display

		Returns:
			dict: Headers and rows for display
		"""
		if not self.is_generated :
			return {
				'headers' : [],
				'rows' : [],
				'is_empty' : True
				}

		# Convert boolean values to display format (0/1 or T/F)
		display_rows = []
		for row in self.rows :
			display_row = []
			for value in row :
				if value is True :
					display_row.append('1')
				elif value is False :
					display_row.append('0')
				elif value is None :
					display_row.append('-')
				else :
					display_row.append(str(value))
			display_rows.append(display_row)

		return {
			'headers' : self.headers.copy(),
			'rows' : display_rows,
			'is_empty' : False
			}

	def export_to_text(self, filename) :
		"""
		Export truth table to text file

		Parameters:
			filename (str): Output file path

		Returns:
			tuple: (success, message)
		"""
		if not self.is_generated :
			return False, "No truth table to export"

		try :
			with open(filename, 'w', encoding='utf-8') as f :
				# Write title
				f.write("TRUTH TABLE\n")
				f.write("=" * 80 + "\n\n")

				# Calculate column widths
				col_widths = []
				for i, header in enumerate(self.headers) :
					max_width = len(header)
					for row in self.rows :
						cell_str = self._format_value(row[i])
						max_width = max(max_width, len(cell_str))
					col_widths.append(max_width + 2)  # Add padding

				# Write headers
				header_line = "|"
				for i, header in enumerate(self.headers) :
					header_line += f" {header:^{col_widths[i] - 2}} |"
				f.write(header_line + "\n")

				# Write separator
				separator = "+"
				for width in col_widths :
					separator += "-" * width + "+"
				f.write(separator + "\n")

				# Write rows
				for row in self.rows :
					row_line = "|"
					for i, value in enumerate(row) :
						cell_str = self._format_value(value)
						row_line += f" {cell_str:^{col_widths[i] - 2}} |"
					f.write(row_line + "\n")

				# Write footer
				f.write(separator + "\n")

			return True, f"Truth table exported to {filename}"

		except Exception as e :
			return False, f"Export failed: {str(e)}"

	def export_to_latex(self, filename) :
		"""
		Export truth table to LaTeX format

		Parameters:
			filename (str): Output file path

		Returns:
			tuple: (success, message)
		"""
		if not self.is_generated :
			return False, "No truth table to export"

		try :
			with open(filename, 'w', encoding='utf-8') as f :
				# Write LaTeX document header
				f.write("\\documentclass{article}\n")
				f.write("\\usepackage{array}\n")
				f.write("\\usepackage{booktabs}\n")
				f.write("\\begin{document}\n\n")

				# Begin table
				f.write("\\begin{table}[h]\n")
				f.write("\\centering\n")
				f.write("\\caption{Truth Table}\n")

				# Column specification
				col_spec = "|" + "c|" * len(self.headers)
				f.write(f"\\begin{{tabular}}{{{col_spec}}}\n")
				f.write("\\hline\n")

				# Headers
				header_line = " & ".join(
					self._latex_escape(h) for h in self.headers)
				f.write(f"{header_line} \\\\\n")
				f.write("\\hline\\hline\n")

				# Rows
				for row in self.rows :
					row_values = []
					for value in row :
						row_values.append(self._format_value_latex(value))
					row_line = " & ".join(row_values)
					f.write(f"{row_line} \\\\\n")
					f.write("\\hline\n")

				# End table
				f.write("\\end{tabular}\n")
				f.write("\\end{table}\n\n")
				f.write("\\end{document}\n")

			return True, f"Truth table exported to {filename}"

		except Exception as e :
			return False, f"Export failed: {str(e)}"

	def _format_value(self, value) :
		"""Format a truth value for display"""
		if value is True :
			return "T"
		elif value is False :
			return "F"
		elif value is None :
			return "-"
		else :
			return str(value)

	def _format_value_latex(self, value) :
		"""Format a truth value for LaTeX"""
		if value is True :
			return "$\\mathbf{T}$"
		elif value is False :
			return "$\\mathbf{F}$"
		elif value is None :
			return "-"
		else :
			return str(value)

	def _latex_escape(self, text) :
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
			'∧' : '$\\land$',
			'∨' : '$\\lor$',
			'¬' : '$\\neg$',
			'→' : '$\\rightarrow$',
			'↔' : '$\\leftrightarrow$',
			'⊕' : '$\\oplus$',
			'↑' : '$\\uparrow$',
			'↓' : '$\\downarrow$'
			}

		result = text
		for old, new in replacements.items() :
			result = result.replace(old, new)

		return result

	def find_rows_where_true(self, formula_index) :
		"""
		Find all rows where a specific formula evaluates to true

		Parameters:
			formula_index (int): Index of formula in formulas list

		Returns:
			list: List of row indices where formula is true
		"""
		if not self.is_generated or formula_index >= len(self.formulas) :
			return []

		true_rows = []
		# Account for atomic propositions in columns
		col_index = len(self.atomic_props) + formula_index

		for i, row in enumerate(self.rows) :
			if row[col_index] is True :
				true_rows.append(i)

		return true_rows

	def is_tautology(self, formula_index) :
		"""Check if a formula in the table is a tautology"""
		if not self.is_generated or formula_index >= len(self.formulas) :
			return False

		col_index = len(self.atomic_props) + formula_index
		return all(row[col_index] is True for row in self.rows)

	def is_contradiction(self, formula_index) :
		"""Check if a formula in the table is a contradiction"""
		if not self.is_generated or formula_index >= len(self.formulas) :
			return False

		col_index = len(self.atomic_props) + formula_index
		return all(row[col_index] is False for row in self.rows)