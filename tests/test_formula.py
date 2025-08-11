"""
Unit tests for the Formula module
Tests parsing, evaluation, and manipulation of logical formulas
"""

import pytest
import os
import sys

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model.formula import Formula


class TestFormula :
	"""Test cases for Formula class"""

	def test_simple_proposition(self) :
		"""Test parsing of simple atomic propositions"""
		f = Formula("A")
		assert str(f) == "A"
		assert f.get_atomic_propositions() == {'A'}

	def test_negation(self) :
		"""Test parsing of negation"""
		f = Formula("¬A")
		assert str(f) == "¬A"
		assert f.get_atomic_propositions() == {'A'}

		# Test double negation
		f2 = Formula("¬¬B")
		assert str(f2) == "¬¬B"
		assert f2.get_atomic_propositions() == {'B'}

	def test_conjunction(self) :
		"""Test parsing of conjunction"""
		f = Formula("A ∧ B")
		assert str(f) == "A ∧ B"
		assert f.get_atomic_propositions() == {'A', 'B'}

		# Test with alternative notation
		f2 = Formula("A & B")
		assert str(f2) == "A ∧ B"
		assert f2.get_atomic_propositions() == {'A', 'B'}

	def test_disjunction(self) :
		"""Test parsing of disjunction"""
		f = Formula("A ∨ B")
		assert str(f) == "A ∨ B"
		assert f.get_atomic_propositions() == {'A', 'B'}

		# Test with alternative notation
		f2 = Formula("A | B")
		assert str(f2) == "A ∨ B"

	def test_implication(self) :
		"""Test parsing of implication"""
		f = Formula("A → B")
		assert str(f) == "A → B"
		assert f.get_atomic_propositions() == {'A', 'B'}

		# Test with alternative notation
		f2 = Formula("A -> B")
		assert str(f2) == "A → B"

	def test_biconditional(self) :
		"""Test parsing of biconditional"""
		f = Formula("A ↔ B")
		assert str(f) == "A ↔ B"
		assert f.get_atomic_propositions() == {'A', 'B'}

		# Test with alternative notation
		f2 = Formula("A <-> B")
		assert str(f2) == "A ↔ B"

	def test_complex_formula(self) :
		"""Test parsing of complex formulas with multiple operators"""
		f = Formula("(A ∧ B) → (C ∨ D)")
		assert f.get_atomic_propositions() == {'A', 'B', 'C', 'D'}

		# Test precedence
		f2 = Formula("A ∧ B → C")
		assert str(f2) == "A ∧ B → C"  # AND has higher precedence than IMPLIES

	def test_evaluation(self) :
		"""Test formula evaluation with truth values"""
		f = Formula("A ∧ B")

		# Test all combinations
		assert f.evaluate({'A' : True, 'B' : True}) == True
		assert f.evaluate({'A' : True, 'B' : False}) == False
		assert f.evaluate({'A' : False, 'B' : True}) == False
		assert f.evaluate({'A' : False, 'B' : False}) == False

	def test_implication_evaluation(self) :
		"""Test implication truth table"""
		f = Formula("A → B")

		assert f.evaluate({'A' : True, 'B' : True}) == True
		assert f.evaluate({'A' : True, 'B' : False}) == False
		assert f.evaluate({'A' : False, 'B' : True}) == True
		assert f.evaluate({'A' : False, 'B' : False}) == True

	def test_complex_evaluation(self) :
		"""Test evaluation of complex formulas"""
		f = Formula("(A ∨ B) ∧ ¬C")

		assert f.evaluate({'A' : True, 'B' : False, 'C' : False}) == True
		assert f.evaluate({'A' : False, 'B' : True, 'C' : False}) == True
		assert f.evaluate({'A' : True, 'B' : True, 'C' : True}) == False
		assert f.evaluate({'A' : False, 'B' : False, 'C' : False}) == False

	def test_parentheses_handling(self) :
		"""Test correct handling of parentheses"""
		f1 = Formula("A ∧ (B ∨ C)")
		f2 = Formula("(A ∧ B) ∨ C")

		# These should evaluate differently
		values = {'A' : True, 'B' : False, 'C' : True}
		assert f1.evaluate(values) == True  # A ∧ (B ∨ C) = T ∧ T = T
		assert f2.evaluate(values) == True  # (A ∧ B) ∨ C = F ∨ T = T

		values2 = {'A' : True, 'B' : False, 'C' : False}
		assert f1.evaluate(values2) == False  # A ∧ (B ∨ C) = T ∧ F = F
		assert f2.evaluate(values2) == False  # (A ∧ B) ∨ C = F ∨ F = F

	def test_invalid_formulas(self) :
		"""Test handling of invalid formulas"""
		# Invalid character
		with pytest.raises(ValueError) :
			Formula("A @ B")

		# Unbalanced parentheses
		with pytest.raises(ValueError) :
			Formula("(A ∧ B")

		with pytest.raises(ValueError) :
			Formula("A ∧ B)")

		# Empty formula
		with pytest.raises(ValueError) :
			Formula("")

		# Missing operand
		with pytest.raises(ValueError) :
			Formula("A ∧")

	def test_xor_operator(self) :
		"""Test exclusive OR operator"""
		f = Formula("A ⊕ B")

		assert f.evaluate({'A' : True, 'B' : True}) == False
		assert f.evaluate({'A' : True, 'B' : False}) == True
		assert f.evaluate({'A' : False, 'B' : True}) == True
		assert f.evaluate({'A' : False, 'B' : False}) == False

		# Alternative notation
		f2 = Formula("A ^ B")
		assert str(f2) == "A ⊕ B"

	def test_nand_nor_operators(self) :
		"""Test NAND and NOR operators"""
		# NAND
		f_nand = Formula("A ↑ B")
		assert f_nand.evaluate({'A' : True, 'B' : True}) == False
		assert f_nand.evaluate({'A' : True, 'B' : False}) == True
		assert f_nand.evaluate({'A' : False, 'B' : True}) == True
		assert f_nand.evaluate({'A' : False, 'B' : False}) == True

		# NOR
		f_nor = Formula("A ↓ B")
		assert f_nor.evaluate({'A' : True, 'B' : True}) == False
		assert f_nor.evaluate({'A' : True, 'B' : False}) == False
		assert f_nor.evaluate({'A' : False, 'B' : True}) == False
		assert f_nor.evaluate({'A' : False, 'B' : False}) == True

	def test_get_subformulas(self) :
		"""Test extraction of subformulas"""
		f = Formula("(A ∧ B) → C")
		subformulas = f.get_subformulas()

		# Should include the full formula and all its parts
		subformula_strings = [str(sf) for sf in subformulas]
		assert "(A ∧ B) → C" in subformula_strings
		assert "A ∧ B" in subformula_strings
		assert "A" in subformula_strings
		assert "B" in subformula_strings
		assert "C" in subformula_strings

	def test_formula_equality(self) :
		"""Test formula equality comparison"""
		f1 = Formula("A ∧ B")
		f2 = Formula("A ∧ B")
		f3 = Formula("B ∧ A")

		assert f1 == f2
		assert f1 != f3  # Different order

		# Test with complex formulas
		f4 = Formula("(A → B) ∧ (B → C)")
		f5 = Formula("(A → B) ∧ (B → C)")
		assert f4 == f5


if __name__ == "__main__" :
	# Run the tests
	pytest.main([__file__, "-v"])