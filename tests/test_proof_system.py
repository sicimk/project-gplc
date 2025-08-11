"""
Unit tests for the ProofSystem module
Tests proof construction, rule application, and automatic proving
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model.formula import Formula
from model.proof_system import ProofSystem, ProofStep


class TestProofSystem :
	"""Test cases for ProofSystem class"""

	def setup_method(self) :
		"""Set up test fixtures"""
		self.proof = ProofSystem()

	def test_add_premise(self) :
		"""Test adding premises to proof system"""
		f1 = Formula("A → B")
		success, msg = self.proof.add_premise(f1)
		assert success == True
		assert len(self.proof.premises) == 1
		assert len(self.proof.proof_steps) == 1

		# Test duplicate premise
		success2, msg2 = self.proof.add_premise(f1)
		assert success2 == False
		assert "already exists" in msg2

	def test_set_conclusion(self) :
		"""Test setting conclusion"""
		conclusion = Formula("B")
		success, msg = self.proof.set_conclusion(conclusion)
		assert success == True
		assert self.proof.conclusion == conclusion

	def test_apply_modus_ponens(self) :
		"""Test applying Modus Ponens rule"""
		# Add premises
		f1 = Formula("A → B")
		f2 = Formula("A")
		self.proof.add_premise(f1)
		self.proof.add_premise(f2)

		# Apply Modus Ponens
		success, msg, new_step = self.proof.apply_rule("MP", [1, 2])
		assert success == True
		assert str(new_step.formula) == "B"
		assert new_step.justification == "Modus Ponens"
		assert new_step.dependencies == [1, 2]

	def test_apply_modus_tollens(self) :
		"""Test applying Modus Tollens rule"""
		# Add premises
		f1 = Formula("A → B")
		f2 = Formula("¬B")
		self.proof.add_premise(f1)
		self.proof.add_premise(f2)

		# Apply Modus Tollens
		success, msg, new_step = self.proof.apply_rule("MT", [1, 2])
		assert success == True
		assert str(new_step.formula) == "¬A"

	def test_apply_conjunction_introduction(self) :
		"""Test applying Conjunction Introduction"""
		# Add premises
		f1 = Formula("A")
		f2 = Formula("B")
		self.proof.add_premise(f1)
		self.proof.add_premise(f2)

		# Apply Conjunction Introduction
		success, msg, new_step = self.proof.apply_rule("CI", [1, 2])
		assert success == True
		assert str(new_step.formula) == "A ∧ B"

	def test_apply_conjunction_elimination(self) :
		"""Test applying Conjunction Elimination"""
		# Add premise
		f1 = Formula("A ∧ B")
		self.proof.add_premise(f1)

		# Apply Conjunction Elimination (left)
		success, msg, new_step = self.proof.apply_rule("CE", [1], which='left')
		assert success == True
		assert str(new_step.formula) == "A"

		# Apply Conjunction Elimination (right)
		success2, msg2, new_step2 = self.proof.apply_rule("CE", [1],
		                                                  which='right')
		assert success2 == True
		assert str(new_step2.formula) == "B"

	def test_invalid_rule_application(self) :
		"""Test invalid rule applications"""
		# Add premise
		f1 = Formula("A")
		self.proof.add_premise(f1)

		# Try to apply Modus Ponens with only one premise
		success, msg, new_step = self.proof.apply_rule("MP", [1])
		assert success == False
		assert "cannot be applied" in msg

	def test_unknown_rule(self) :
		"""Test applying unknown rule"""
		f1 = Formula("A")
		self.proof.add_premise(f1)

		success, msg, new_step = self.proof.apply_rule("UNKNOWN", [1])
		assert success == False
		assert "Unknown rule" in msg

	def test_invalid_step_index(self) :
		"""Test referencing invalid step index"""
		f1 = Formula("A")
		self.proof.add_premise(f1)

		success, msg, new_step = self.proof.apply_rule("MP", [1, 99])
		assert success == False
		assert "Step 99 not found" in msg

	def test_proof_completion(self) :
		"""Test proof completion detection"""
		# Set up a simple proof
		f1 = Formula("A → B")
		f2 = Formula("A")
		conclusion = Formula("B")

		self.proof.add_premise(f1)
		self.proof.add_premise(f2)
		self.proof.set_conclusion(conclusion)

		# Initially not complete
		assert self.proof.is_complete == False

		# Apply Modus Ponens
		self.proof.apply_rule("MP", [1, 2])

		# Now should be complete
		assert self.proof.is_complete == True

	def test_auto_prove_simple(self) :
		"""Test automatic proof for simple argument"""
		# Modus Ponens example
		f1 = Formula("A → B")
		f2 = Formula("A")
		conclusion = Formula("B")

		self.proof.add_premise(f1)
		self.proof.add_premise(f2)
		self.proof.set_conclusion(conclusion)

		success, msg = self.proof.auto_prove(max_steps=10)
		assert success == True
		assert self.proof.is_complete == True

	def test_auto_prove_chain(self) :
		"""Test automatic proof with chain of implications"""
		# A → B, B → C, A ⊢ C
		f1 = Formula("A → B")
		f2 = Formula("B → C")
		f3 = Formula("A")
		conclusion = Formula("C")

		self.proof.add_premise(f1)
		self.proof.add_premise(f2)
		self.proof.add_premise(f3)
		self.proof.set_conclusion(conclusion)

		success, msg = self.proof.auto_prove(max_steps=10)
		assert success == True
		assert self.proof.is_complete == True

	def test_auto_prove_no_solution(self) :
		"""Test automatic proof when no solution exists"""
		# Invalid argument
		f1 = Formula("A")
		conclusion = Formula("B")

		self.proof.add_premise(f1)
		self.proof.set_conclusion(conclusion)

		success, msg = self.proof.auto_prove(max_steps=5)
		assert success == False
		assert "Could not complete proof" in msg

	def test_get_dependencies(self) :
		"""Test dependency tracking"""
		# Build a proof with dependencies
		f1 = Formula("A → B")
		f2 = Formula("B → C")
		f3 = Formula("A")

		self.proof.add_premise(f1)  # Step 1
		self.proof.add_premise(f2)  # Step 2
		self.proof.add_premise(f3)  # Step 3

		# Apply MP to get B (depends on 1, 3)
		self.proof.apply_rule("MP", [1, 3])  # Step 4

		# Apply MP to get C (depends on 2, 4, and transitively on 1, 3)
		self.proof.apply_rule("MP", [2, 4])  # Step 5

		# Check dependencies
		deps = self.proof.get_dependencies(5)
		assert 2 in deps  # Direct dependency
		assert 4 in deps  # Direct dependency
		assert 1 in deps  # Transitive dependency
		assert 3 in deps  # Transitive dependency

	def test_validate_proof(self) :
		"""Test proof validation"""
		# Valid proof
		f1 = Formula("A → B")
		f2 = Formula("A")
		conclusion = Formula("B")

		self.proof.add_premise(f1)
		self.proof.add_premise(f2)
		self.proof.set_conclusion(conclusion)
		self.proof.apply_rule("MP", [1, 2])

		is_valid, msg = self.proof.validate_proof()
		assert is_valid == True

		# Incomplete proof
		self.proof.is_complete = False
		is_valid2, msg2 = self.proof.validate_proof()
		assert is_valid2 == False
		assert "incomplete" in msg2.lower()

	def test_proof_to_string(self) :
		"""Test string representation of proof"""
		f1 = Formula("A")
		f2 = Formula("B")
		conclusion = Formula("A ∧ B")

		self.proof.add_premise(f1)
		self.proof.add_premise(f2)
		self.proof.set_conclusion(conclusion)

		proof_str = self.proof.to_string()
		assert "PROOF DERIVATION" in proof_str
		assert "Premises:" in proof_str
		assert "1. A" in proof_str
		assert "2. B" in proof_str
		assert "Conclusion to prove: A ∧ B" in proof_str

	def test_clear_proof(self) :
		"""Test clearing proof system"""
		# Add some content
		f1 = Formula("A")
		self.proof.add_premise(f1)
		self.proof.set_conclusion(Formula("B"))

		# Clear
		self.proof.clear()

		assert len(self.proof.premises) == 0
		assert len(self.proof.proof_steps) == 0
		assert self.proof.conclusion is None
		assert self.proof.is_complete == False

	def test_duplicate_formula_detection(self) :
		"""Test that duplicate formulas are not added"""
		f1 = Formula("A → B")
		f2 = Formula("A")

		self.proof.add_premise(f1)
		self.proof.add_premise(f2)

		# Apply MP to get B
		success1, _, _ = self.proof.apply_rule("MP", [1, 2])
		assert success1 == True

		# Try to apply MP again - should fail as B already exists
		success2, msg, _ = self.proof.apply_rule("MP", [1, 2])
		assert success2 == False
		assert "already exists" in msg

	def test_proof_step_string(self) :
		"""Test ProofStep string representation"""
		formula = Formula("A → B")
		step = ProofStep(1, formula, "Premise")

		assert str(step) == "1. A → B (Premise)"

		# With dependencies
		step2 = ProofStep(3, Formula("B"), "Modus Ponens", [1, 2])
		assert str(step2) == "3. B (Modus Ponens [1, 2])"


if __name__ == "__main__" :
	pytest.main([__file__, "-v"])