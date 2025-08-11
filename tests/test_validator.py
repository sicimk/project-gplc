"""
Unit tests for the FormulaValidator module
Tests validation, type checking, and logical properties
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model.formula import Formula
from model.validator import FormulaValidator


class TestFormulaValidator :
    """Test cases for FormulaValidator class"""

    def setup_method(self) :
        """Set up test fixtures"""
        self.validator = FormulaValidator()

    def test_valid_characters(self) :
        """Test character validation"""
        # Valid formulas
        is_valid, invalid = self.validator.check_valid_characters("A ∧ B")
        assert is_valid == True
        assert invalid == []

        is_valid, invalid = self.validator.check_valid_characters(
            "(A → B) ∨ ¬C")
        assert is_valid == True

        # Invalid characters
        is_valid, invalid = self.validator.check_valid_characters("A @ B")
        assert is_valid == False
        assert len(invalid) > 0
        assert invalid[0][0] == '@'

    def test_well_formed_check(self) :
        """Test well-formedness checking"""
        # Well-formed formulas
        assert self.validator.check_well_formed("A")[0] == True
        assert self.validator.check_well_formed("A ∧ B")[0] == True
        assert self.validator.check_well_formed("(A → B) ∧ (B → C)")[0] == True
        assert self.validator.check_well_formed("¬¬A")[0] == True

        # Not well-formed
        assert self.validator.check_well_formed("")[0] == False
        assert self.validator.check_well_formed("A ∧")[0] == False
        assert self.validator.check_well_formed("(A ∧ B")[0] == False
        assert self.validator.check_well_formed("A ∧ B)")[0] == False

    def test_tautology_detection(self) :
        """Test tautology detection"""
        # Tautologies
        f1 = Formula("A ∨ ¬A")  # Law of excluded middle
        assert self.validator.check_tautology(f1) == True

        f2 = Formula("A → A")  # Self-implication
        assert self.validator.check_tautology(f2) == True

        f3 = Formula("(A → B) ∨ (B → A)")  # Always true
        assert self.validator.check_tautology(f3) == True

        # Not tautologies
        f4 = Formula("A")
        assert self.validator.check_tautology(f4) == False

        f5 = Formula("A ∧ B")
        assert self.validator.check_tautology(f5) == False

    def test_contradiction_detection(self) :
        """Test contradiction detection"""
        # Contradictions
        f1 = Formula("A ∧ ¬A")
        assert self.validator.check_contradiction(f1) == True

        f2 = Formula("(A → B) ∧ A ∧ ¬B")
        assert self.validator.check_contradiction(f2) == True

        # Not contradictions
        f3 = Formula("A")
        assert self.validator.check_contradiction(f3) == False

        f4 = Formula("A ∨ B")
        assert self.validator.check_contradiction(f4) == False

    def test_contingent_detection(self) :
        """Test contingent formula detection"""
        # Contingent formulas
        f1 = Formula("A")
        assert self.validator.check_contingent(f1) == True

        f2 = Formula("A → B")
        assert self.validator.check_contingent(f2) == True

        # Not contingent (tautology)
        f3 = Formula("A ∨ ¬A")
        assert self.validator.check_contingent(f3) == False

        # Not contingent (contradiction)
        f4 = Formula("A ∧ ¬A")
        assert self.validator.check_contingent(f4) == False

    def test_formula_type(self) :
        """Test formula type determination"""
        f1 = Formula("A ∨ ¬A")
        assert self.validator.get_formula_type(f1) == "tautology"

        f2 = Formula("A ∧ ¬A")
        assert self.validator.get_formula_type(f2) == "contradiction"

        f3 = Formula("A → B")
        assert self.validator.get_formula_type(f3) == "contingent"

    def test_logical_equivalence(self) :
        """Test logical equivalence checking"""
        # Equivalent formulas
        f1 = Formula("A → B")
        f2 = Formula("¬A ∨ B")
        assert self.validator.check_logical_equivalence(f1, f2) == True

        # De Morgan's Law
        f3 = Formula("¬(A ∧ B)")
        f4 = Formula("¬A ∨ ¬B")
        assert self.validator.check_logical_equivalence(f3, f4) == True

        # Not equivalent
        f5 = Formula("A ∧ B")
        f6 = Formula("A ∨ B")
        assert self.validator.check_logical_equivalence(f5, f6) == False

    def test_validate_premises_and_conclusion(self) :
        """Test validation of premises and conclusion"""
        p1 = Formula("A → B")
        p2 = Formula("B → C")
        c = Formula("A → C")

        # Valid set
        is_valid, msg = self.validator.validate_premises_and_conclusion(
            [p1, p2], c)
        assert is_valid == True

        # No premises
        is_valid, msg = self.validator.validate_premises_and_conclusion([], c)
        assert is_valid == False
        assert "premise" in msg.lower()

        # No conclusion
        is_valid, msg = self.validator.validate_premises_and_conclusion(
            [p1, p2], None)
        assert is_valid == False
        assert "conclusion" in msg.lower()

        # Contradictory premises
        p3 = Formula("A")
        p4 = Formula("¬A")
        is_valid, msg = self.validator.validate_premises_and_conclusion(
            [p3, p4], c)
        assert is_valid == False
        assert "contradictory" in msg.lower()

    def test_find_counter_example(self) :
        """Test counter-example finding"""
        # Valid argument - no counter-example
        p1 = Formula("A → B")
        p2 = Formula("A")
        c = Formula("B")

        counter = self.validator.find_counter_example([p1, p2], c)
        assert counter is None

        # Invalid argument - has counter-example
        p3 = Formula("A ∨ B")
        c2 = Formula("A")

        counter = self.validator.find_counter_example([p3], c2)
        assert counter is not None
        # Counter-example should make premise true but conclusion false
        assert p3.evaluate(counter) == True
        assert c2.evaluate(counter) == False


if __name__ == "__main__" :
    pytest.main([__file__, "-v"])
