"""
Export functionality for proofs and truth tables
Handles exporting to text and LaTeX formats
"""

import os
from datetime import datetime
from typing import List, Dict, Optional

from model.formula import Formula
from model.proof_system import ProofSystem, ProofStep
from model.truth_table import TruthTable

class FileExporter :
	"""
	Handles exporting proofs and truth tables to various file formats
	"""

	def __init__(self) :
		"""
		Initialize exporter with default settings
		"""
		self.latex_packages = [
			"amsmath",
			"amssymb",
			"array",
			"booktabs",
			"longtable"
			]

	def export_proof_to_text(self, proof_system, filepath) :
		"""
		Export proof steps to text file

		Parameters:
			proof_system: ProofSystem object
			filepath (str): Output file path

		Returns:
			tuple: (success, message)
		"""
		try :
			# Ensure directory exists
			self._ensure_directory_exists(filepath)

			with open(filepath, 'w', encoding='utf-8') as f :
				# Write header
				f.write("PROPOSITIONAL LOGIC PROOF\n")
				f.write("=" * 60 + "\n")
				f.write(
					f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
				f.write("=" * 60 + "\n\n")

				# Write premises
				f.write("PREMISES:\n")
				premise_count = 0
				for step in proof_system.proof_steps :
					if step.justification == "Premise" :
						f.write(f"  {step.index}. {step.formula}\n")
						premise_count += 1

				if premise_count == 0 :
					f.write("  (No premises)\n")

				# Write conclusion
				f.write(f"\nCONCLUSION TO PROVE:\n")
				if proof_system.conclusion :
					f.write(f"  {proof_system.conclusion}\n")
				else :
					f.write("  (No conclusion set)\n")

				# Write proof steps
				f.write("\nPROOF STEPS:\n")
				f.write("-" * 60 + "\n")

				for step in proof_system.proof_steps :
					# Format step
					step_str = f"{step.index:3d}. {str(step.formula):40s} "

					# Add justification
					if step.dependencies :
						deps_str = ", ".join(map(str, step.dependencies))
						just_str = f"{step.justification} [{deps_str}]"
					else :
						just_str = step.justification

					f.write(f"{step_str} {just_str}\n")

				# Write conclusion status
				f.write("\n" + "=" * 60 + "\n")
				if proof_system.is_complete :
					f.write(
						"✓ PROOF COMPLETE - Conclusion successfully derived!\n")
				else :
					f.write(
						"✗ PROOF INCOMPLETE - Conclusion not yet reached.\n")

			return True, f"Proof exported successfully to {filepath}"

		except Exception as e :
			return False, f"Export failed: {str(e)}"

	def export_proof_to_latex(self, proof_system, filepath) :
		"""
		Export proof to LaTeX format

		Parameters:
			proof_system: ProofSystem object
			filepath (str): Output file path

		Returns:
			tuple: (success, message)
		"""
		try :
			# Ensure directory exists
			self._ensure_directory_exists(filepath)

			with open(filepath, 'w', encoding='utf-8') as f :
				# Write LaTeX preamble
				f.write("\\documentclass[11pt]{article}\n")

				# Add packages
				for package in self.latex_packages :
					f.write(f"\\usepackage{{{package}}}\n")

				# Add custom commands for logical operators
				f.write("\n% Custom commands for logical operators\n")
				f.write("\\newcommand{\\limplies}{\\rightarrow}\n")
				f.write("\\newcommand{\\liff}{\\leftrightarrow}\n")
				f.write("\\newcommand{\\lnot}{\\neg}\n")
				f.write("\\newcommand{\\land}{\\wedge}\n")
				f.write("\\newcommand{\\lor}{\\vee}\n")
				f.write("\\newcommand{\\lxor}{\\oplus}\n")
				f.write("\\newcommand{\\lnand}{\\uparrow}\n")
				f.write("\\newcommand{\\lnor}{\\downarrow}\n")

				f.write("\n\\begin{document}\n\n")

				# Title
				f.write("\\section*{Propositional Logic Proof}\n\n")

				# Premises
				f.write("\\subsection*{Premises}\n")
				f.write("\\begin{enumerate}\n")

				premise_count = 0
				for step in proof_system.proof_steps :
					if step.justification == "Premise" :
						latex_formula = self._convert_to_latex_notation(
							str(step.formula))
						f.write(f"\\item ${latex_formula}$\n")
						premise_count += 1

				if premise_count == 0 :
					f.write("\\item[] (No premises)\n")

				f.write("\\end{enumerate}\n\n")

				# Conclusion
				f.write("\\subsection*{Conclusion to Prove}\n")
				if proof_system.conclusion :
					latex_conclusion = self._convert_to_latex_notation(
						str(proof_system.conclusion))
					f.write(f"${latex_conclusion}$\n\n")
				else :
					f.write("(No conclusion set)\n\n")

				# Proof steps in tabular format
				f.write("\\subsection*{Proof Derivation}\n")
				f.write("\\begin{longtable}{r l l}\n")
				f.write("\\toprule\n")
				f.write("Step & Formula & Justification \\\\\n")
				f.write("\\midrule\n")
				f.write("\\endhead\n")  # For multi-page tables

				for step in proof_system.proof_steps :
					# Convert formula to LaTeX
					latex_formula = self._convert_to_latex_notation(
						str(step.formula))

					# Format justification
					if step.dependencies :
						deps_str = ", ".join(map(str, step.dependencies))
						justification = f"{step.justification} [{deps_str}]"
					else :
						justification = step.justification

					# Escape any remaining special characters in justification
					justification = justification.replace("_", "\\_")

					f.write(
						f"{step.index}. & ${latex_formula}$ & {justification} \\\\\n")

				f.write("\\bottomrule\n")
				f.write("\\end{longtable}\n\n")

				# Result
				f.write("\\subsection*{Result}\n")
				if proof_system.is_complete :
					f.write("\\textbf{\\color{green}✓ Proof Complete} -- ")
					f.write(
						"The conclusion has been successfully derived from the premises.\n")
				else :
					f.write("\\textbf{\\color{red}✗ Proof Incomplete} -- ")
					f.write("The conclusion has not yet been reached.\n")

				f.write("\n\\end{document}\n")

			return True, f"Proof exported to LaTeX: {filepath}"

		except Exception as e :
			return False, f"Export failed: {str(e)}"

	def export_truth_table_to_text(self, truth_table, filepath) :
		"""
		Export truth table to text file

		Parameters:
			truth_table: TruthTable object
			filepath (str): Output file path

		Returns:
			tuple: (success, message)
		"""
		# Delegate to TruthTable's own export method
		return truth_table.export_to_text(filepath)

	def export_truth_table_to_latex(self, truth_table, filepath) :
		"""
		Export truth table to LaTeX format

		Parameters:
			truth_table: TruthTable object
			filepath (str): Output file path

		Returns:
			tuple: (success, message)
		"""
		# Delegate to TruthTable's own export method
		return truth_table.export_to_latex(filepath)

	def _convert_to_latex_notation(self, formula_string) :
		"""
		Convert logical symbols to LaTeX notation

		Parameters:
			formula_string (str): Formula with Unicode symbols

		Returns:
			str: Formula with LaTeX commands
		"""
		# Map Unicode operators to LaTeX commands
		replacements = {
			'∧' : '\\land',
			'∨' : '\\lor',
			'¬' : '\\lnot ',
			'→' : '\\limplies',
			'↔' : '\\liff',
			'⊕' : '\\lxor',
			'↑' : '\\lnand',
			'↓' : '\\lnor'
			}

		result = formula_string
		for symbol, latex_cmd in replacements.items() :
			result = result.replace(symbol, f' {latex_cmd} ')

		# Clean up extra spaces
		while '  ' in result :
			result = result.replace('  ', ' ')

		return result.strip()

	def _ensure_directory_exists(self, filepath) :
		"""
		Ensure the directory for the file exists

		Parameters:
			filepath (str): Full path to the file
		"""
		directory = os.path.dirname(filepath)
		if directory and not os.path.exists(directory) :
			os.makedirs(directory)

	def export_combined_to_latex(self, proof_system, truth_table, filepath) :
		"""
		Export both proof and truth table to a single LaTeX document

		Parameters:
			proof_system: ProofSystem object
			truth_table: TruthTable object
			filepath (str): Output file path

		Returns:
			tuple: (success, message)
		"""
		try :
			# Ensure directory exists
			self._ensure_directory_exists(filepath)

			with open(filepath, 'w', encoding='utf-8') as f :
				# Write LaTeX preamble
				f.write("\\documentclass[11pt]{article}\n")

				# Add packages
				for package in self.latex_packages :
					f.write(f"\\usepackage{{{package}}}\n")

				# Page geometry for better table fitting
				f.write("\\usepackage[margin=1in]{geometry}\n")
				f.write("\\usepackage{color}\n")

				# Custom commands
				f.write("\n% Custom commands for logical operators\n")
				f.write("\\newcommand{\\limplies}{\\rightarrow}\n")
				f.write("\\newcommand{\\liff}{\\leftrightarrow}\n")
				f.write("\\newcommand{\\lnot}{\\neg}\n")
				f.write("\\newcommand{\\land}{\\wedge}\n")
				f.write("\\newcommand{\\lor}{\\vee}\n")
				f.write("\\newcommand{\\lxor}{\\oplus}\n")
				f.write("\\newcommand{\\lnand}{\\uparrow}\n")
				f.write("\\newcommand{\\lnor}{\\downarrow}\n")

				f.write("\n\\begin{document}\n\n")

				# Title
				f.write("\\title{Propositional Logic: Proof and Truth Table}\n")
				f.write("\\date{\\today}\n")
				f.write("\\maketitle\n\n")

				# First section: Proof
				f.write("\\section{Proof Derivation}\n\n")

				# (Include proof content similar to export_proof_to_latex)
				# ... [proof export code here] ...

				# Second section: Truth Table
				f.write("\\section{Truth Table}\n\n")

				if truth_table.is_generated :
					# Get table data
					table_data = truth_table.get_table_data()
					headers = table_data['headers']
					rows = table_data['rows']

					# Determine if we need landscape orientation for large tables
					if len(headers) > 8 :
						f.write("\\begin{landscape}\n")

					# Begin table
					f.write("\\begin{table}[h]\n")
					f.write("\\centering\n")

					# Use smaller font for large tables
					if len(headers) > 10 :
						f.write("\\small\n")

					# Column specification
					col_spec = "|" + "c|" * len(headers)
					f.write(f"\\begin{{tabular}}{{{col_spec}}}\n")
					f.write("\\hline\n")

					# Headers
					header_parts = []
					for h in headers :
						header_parts.append(self._convert_to_latex_notation(h))
					header_line = " & ".join(f"${h}$" for h in header_parts)
					f.write(f"{header_line} \\\\\n")
					f.write("\\hline\\hline\n")

					# Rows
					for row in rows :
						row_parts = []
						for value in row :
							if value == '1' :
								row_parts.append("\\textbf{T}")
							elif value == '0' :
								row_parts.append("\\textbf{F}")
							else :
								row_parts.append(value)
						row_line = " & ".join(row_parts)
						f.write(f"{row_line} \\\\\n")
						f.write("\\hline\n")

					# End table
					f.write("\\end{tabular}\n")
					f.write("\\end{table}\n")

					if len(headers) > 8 :
						f.write("\\end{landscape}\n")
				else :
					f.write("No truth table has been generated.\n")

				f.write("\n\\end{document}\n")

			return True, f"Combined proof and truth table exported to: {filepath}"

		except Exception as e :
			return False, f"Export failed: {str(e)}"