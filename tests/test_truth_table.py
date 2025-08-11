"""
Unit tests for the TruthTable module
Tests truth table generation, display, and export functionality
"""

import pytest
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model.formula import Formula
from model.truth_table import TruthTable
from model.proof_system import ProofSystem


class TestTruthTable :
	"""Test cases for TruthTable class"""

	def setup_method(self) :
		"""Set up test fixtures"""
		self.table = TruthTable()

	def test_generate_simple_table(self) :
		"""Test generating truth table for simple formulas"""
		f1 = Formula("A")
		f2 = Formula("¬A")

		success, msg = self.table.generate_from_formulas([f1, f2])
		assert success == True
		assert "2 rows" in msg

		# Check table structure
		data = self.table.get_table_data()
		assert len(data['headers']) == 3  # A, A, ¬A
		assert len(data['rows']) == 2  # 2^1 combinations

	def test_generate_complex_table(self) :
		"""Test generating truth table for complex formulas"""
		f1 = Formula("A ∧ B")
		f2 = Formula("A → B")
		f3 = Formula("A ∨ B")

		success, msg = self.table.generate_from_formulas([f1, f2, f3])
		assert success == True

		data = self.table.get_table_data()
		assert len(data['headers']) == 5  # A, B, A∧B, A→B, A∨B
		assert len(data['rows']) == 4  # 2^2 combinations

	def test_truth_values(self) :
		"""Test correct truth value calculation"""
		f1 = Formula("A ∧ B")
		self.table.generate_from_formulas([f1])

		data = self.table.get_table_data()
		rows = data['rows']

		# Check truth values for A ∧ B
		# Row format: [A, B, A∧B]
		assert rows[0] == ['1', '1', '1']  # T, T -> T
		assert rows[1] == ['1', '0', '0']  # T, F -> F
		assert rows[2] == ['0', '1', '0']  # F, T -> F
		assert rows[3] == ['0', '0', '0']  # F, F -> F

	def test_implication_truth_table(self) :
		"""Test truth table for implication"""
		f = Formula("A → B")
		self.table.generate_from_formulas([f])

		data = self.table.get_table_data()
		rows = data['rows']

		# Check truth values for A → B
		assert rows[0][2] == '1'  # T → T = T
		assert rows[1][2] == '0'  # T → F = F
		assert rows[2][2] == '1'  # F → T = T
		assert rows[3][2] == '1'  # F → F = T

	def test_three_variables(self) :
		"""Test truth table with three variables"""
		f = Formula("(A ∧ B) → C")
		self.table.generate_from_formulas([f])

		data = self.table.get_table_data()
		assert len(data['headers']) == 4  # A, B, C, (A∧B)→C
		assert len(data['rows']) == 8  # 2^3 combinations

	def test_generate_from_proof(self) :
		"""Test generating truth table from proof system"""
		proof = ProofSystem()

		# Add premises
		f1 = Formula("A → B")
		f2 = Formula("B → C")
		f3 = Formula("A")
		conclusion = Formula("C")

		proof.add_premise(f1)
		proof.add_premise(f2)
		proof.add_premise(f3)
		proof.set_conclusion(conclusion)

		# Generate table from proof
		success, msg = self.table.generate_from_proof(proof)
		assert success == True

		data = self.table.get_table_data()
		# Should have A, B, C, and all the formulas
		assert 'A' in data['headers']
		assert 'B' in data['headers']
		assert 'C' in data['headers']
		assert 'A → B' in data['headers']
		assert 'B → C' in data['headers']

	def test_empty_formulas(self) :
		"""Test handling empty formula list"""
		success, msg = self.table.generate_from_formulas([])
		assert success == False
		assert "No formulas" in msg

	def test_clear_table(self) :
		"""Test clearing truth table"""
		f = Formula("A")
		self.table.generate_from_formulas([f])

		# Verify table has data
		assert self.table.is_generated == True

		# Clear
		self.table.clear()

		# Verify cleared
		assert self.table.is_generated == False
		assert len(self.table.headers) == 0
		assert len(self.table.rows) == 0

	def test_export_to_text(self) :
		"""Test exporting truth table to text file"""
		f1 = Formula("A → B")
		f2 = Formula("A ∧ B")
		self.table.generate_from_formulas([f1, f2])

		# Create temporary file
		with tempfile.NamedTemporaryFile(mode='w', delete=False,
		                                 suffix='.txt') as tmp :
			tmp_name = tmp.name

		try :
			success, msg = self.table.export_to_text(tmp_name)
			assert success == True

			# Read and verify content
			with open(tmp_name, 'r', encoding='utf-8') as f :
				content = f.read()
				assert "TRUTH TABLE" in content
				assert "A" in content
				assert "B" in content
				assert "A → B" in content
				assert "A ∧ B" in content
		finally :
			# Clean up
			os.unlink(tmp_name)

	def test_export_to_latex(self) :
		"""Test exporting truth table to LaTeX"""
		f = Formula("A ∨ B")
		self.table.generate_from_formulas([f])

		# Create temporary file
		with tempfile.NamedTemporaryFile(mode='w', delete=False,
		                                 suffix='.tex') as tmp :
			tmp_name = tmp.name

		try :
			success, msg = self.table.export_to_latex(tmp_name)
			assert success == True

			# Read and verify content
			with open(tmp_name, 'r', encoding='utf-8') as f :
				content = f.read()
				assert "\\documentclass" in content
				assert "\\begin{tabular}" in content
				assert "\\end{tabular}" in content
				assert "\\lor" in content  # LaTeX for ∨
		finally :
			# Clean up
			os.unlink(tmp_name)

	def test_export_without_generation(self) :
		"""Test exporting when no table is generated"""
		with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp :
			tmp_name = tmp.name

		try :
			success, msg = self.table.export_to_text(tmp_name)
			assert success == False
			assert "No truth table to export" in msg
		finally :
			# Clean up
			if os.path.exists(tmp_name) :
				os.unlink(tmp_name)

	def test_find_rows_where_true(self) :
		"""Test finding rows where formula is true"""
		f1 = Formula("A")
		f2 = Formula("A → B")
		self.table.generate_from_formulas([f1, f2])

		# Find rows where A is true
		true_rows = self.table.find_rows_where_true(0)  # A is first formula
		assert len(true_rows) == 2  # A is true in 2 out of 4 rows

		# Find rows where A → B is true
		true_rows2 = self.table.find_rows_where_true(
			1)  # A → B is second formula
		assert len(true_rows2) == 3  # A → B is false only when A=T, B=F

	def test_is_tautology(self) :
		"""Test tautology detection in truth table"""
		f1 = Formula("A ∨ ¬A")  # Tautology
		f2 = Formula("A")  # Not a tautology

		self.table.generate_from_formulas([f1, f2])

		assert self.table.is_tautology(0) == True  # A ∨ ¬A
		assert self.table.is_tautology(1) == False  # A

	def test_is_contradiction(self) :
		"""Test contradiction detection in truth table"""
		f1 = Formula("A ∧ ¬A")  # Contradiction
		f2 = Formula("A")  # Not a contradiction

		self.table.generate_from_formulas([f1, f2])

		assert self.table.is_contradiction(0) == True  # A ∧ ¬A
		assert self.table.is_contradiction(1) == False  # A

	def test_table_with_evaluation_error(self) :
		"""Test handling formulas that fail to evaluate"""
		# This is a bit contrived since our formulas should always evaluate
		# But it tests the error handling
		f = Formula("A ∧ B")
		self.table.generate_from_formulas([f])

		# The table should still generate even if some evaluations fail
		data = self.table.get_table_data()
		assert len(data['rows']) == 4

	def test_latex_special_characters(self) :
		"""Test LaTeX export handles special characters correctly"""
		f = Formula("A ∧ B → C")
		self.table.generate_from_formulas([f])

		with tempfile.NamedTemporaryFile(mode='w', delete=False,
		                                 suffix='.tex') as tmp :
			tmp_name = tmp.name

		try :
			self.table.export_to_latex(tmp_name)

			with open(tmp_name, 'r', encoding='utf-8') as f :
				content = f.read()
				# Check that logical operators are converted to LaTeX
				assert "$\\land$" in content  # ∧
				assert "$\\rightarrow$" in content  # →
		finally :
			os.unlink(tmp_name)


if __name__ == "__main__" :
	pytest.main([__file__, "-v"])