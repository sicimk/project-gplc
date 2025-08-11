"""
Formula validation utilities
Checks syntax, well-formedness, and semantic properties of formulas
"""

from typing import List, Dict, Optional, Tuple
from itertools import product

from model.formula import Formula

class FormulaValidator:
    """
    Validates formula syntax and semantics
    """

    def __init__(self):
        """
        Initialize validator with validation rules
        """
        # Define valid characters for formulas
        self.valid_props = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.valid_operators = {
            '∧', '&',     # AND
            '∨', '|',     # OR
            '¬', '~',     # NOT
            '→', '-',     # IMPLIES (- is part of ->)
            '↔', '<',     # IFF (< is part of <->)
            '⊕', '^',     # XOR
            '↑',          # NAND
            '↓',          # NOR
            '>', '='      # Parts of -> and <->
        }
        self.valid_parentheses = {'(', ')'}
        self.valid_whitespace = {' ', '\t', '\n', '\r'}

        # All valid characters
        self.all_valid_chars = (self.valid_props |
                               self.valid_operators |
                               self.valid_parentheses |
                               self.valid_whitespace)

    def check_valid_characters(self, expression):
        """
        Check if expression contains only valid characters

        Parameters:
            expression (str): Formula string to check

        Returns:
            tuple: (is_valid, list of invalid characters with positions)
        """
        invalid_chars = []

        for i, char in enumerate(expression):
            if char not in self.all_valid_chars:
                invalid_chars.append((char, i))

        is_valid = len(invalid_chars) == 0
        return is_valid, invalid_chars

    def check_well_formed(self, expression):
        """
        Check if formula is well-formed

        Parameters:
            expression (str): Formula string to check

        Returns:
            tuple: (is_well_formed, error_message)
        """
        # Remove whitespace for easier checking
        expr = expression.strip()

        if not expr:
            return False, "Empty expression"

        # Check parentheses balance
        paren_check = self._check_parentheses_balanced(expr)
        if not paren_check[0]:
            return False, paren_check[1]

        # Try to parse using Formula class
        try:
            from .formula import Formula
            formula = Formula(expr)
            return True, "Well-formed formula"
        except ValueError as e:
            return False, f"Parse error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def _check_parentheses_balanced(self, expression):
        """
        Check if parentheses are properly balanced

        Parameters:
            expression (str): Expression to check

        Returns:
            tuple: (is_balanced, error_message)
        """
        stack = []

        for i, char in enumerate(expression):
            if char == '(':
                stack.append(i)
            elif char == ')':
                if not stack:
                    return False, f"Unmatched closing parenthesis at position {i}"
                stack.pop()

        if stack:
            return False, f"Unmatched opening parenthesis at position {stack[0]}"

        return True, "Parentheses balanced"

    def check_tautology(self, formula):
        """
        Check if formula is a tautology (always true)

        Parameters:
            formula: Formula object to check

        Returns:
            bool: True if formula is always true
        """
        # Get all atomic propositions
        props = list(formula.get_atomic_propositions())
        if not props:
            # No propositions - evaluate directly
            try:
                return formula.evaluate({})
            except:
                return False

        # Generate all possible truth value combinations
        n_props = len(props)

        # Check all 2^n combinations
        for values in product([True, False], repeat=n_props):
            truth_assignment = dict(zip(props, values))

            try:
                if not formula.evaluate(truth_assignment):
                    return False
            except:
                return False

        return True

    def check_contradiction(self, formula):
        """
        Check if formula is a contradiction (always false)

        Parameters:
            formula: Formula object to check

        Returns:
            bool: True if formula is always false
        """
        # Get all atomic propositions
        props = list(formula.get_atomic_propositions())
        if not props:
            # No propositions - evaluate directly
            try:
                return not formula.evaluate({})
            except:
                return False

        # Generate all possible truth value combinations
        n_props = len(props)

        # Check all 2^n combinations
        for values in product([True, False], repeat=n_props):
            truth_assignment = dict(zip(props, values))

            try:
                if formula.evaluate(truth_assignment):
                    return False
            except:
                return False

        return True

    def check_contingent(self, formula):
        """
        Check if formula is contingent (neither tautology nor contradiction)

        Parameters:
            formula: Formula object to check

        Returns:
            bool: True if formula is contingent
        """
        return not (self.check_tautology(formula) or self.check_contradiction(formula))

    def get_formula_type(self, formula):
        """
        Determine the type of formula (tautology, contradiction, or contingent)

        Parameters:
            formula: Formula object to check

        Returns:
            str: "tautology", "contradiction", or "contingent"
        """
        if self.check_tautology(formula):
            return "tautology"
        elif self.check_contradiction(formula):
            return "contradiction"
        else:
            return "contingent"

    def validate_premises_and_conclusion(self, premises, conclusion):
        """
        Validate that premises and conclusion are suitable for proof

        Parameters:
            premises (list): List of Formula objects
            conclusion: Formula object

        Returns:
            tuple: (is_valid, error_message)
        """
        # Check if we have at least one premise
        if not premises:
            return False, "At least one premise is required"

        # Check if conclusion is provided
        if not conclusion:
            return False, "Conclusion is required"

        # Check if conclusion is a tautology
        if self.check_tautology(conclusion):
            return True, "Warning: Conclusion is a tautology (always true)"

        # Check for contradictory premises
        all_props = set()
        for premise in premises:
            all_props.update(premise.get_atomic_propositions())
        all_props.update(conclusion.get_atomic_propositions())

        props_list = list(all_props)

        # Check if premises are consistent (not contradictory)
        has_valid_assignment = False
        for values in product([True, False], repeat=len(props_list)):
            truth_assignment = dict(zip(props_list, values))

            # Check if all premises are true under this assignment
            all_premises_true = True
            try:
                for premise in premises:
                    if not premise.evaluate(truth_assignment):
                        all_premises_true = False
                        break

                if all_premises_true:
                    has_valid_assignment = True
                    break
            except:
                continue

        if not has_valid_assignment:
            return False, "Premises are contradictory (no valid truth assignment)"

        return True, "Valid premises and conclusion"

    def check_logical_equivalence(self, formula1, formula2):
        """
        Check if two formulas are logically equivalent

        Parameters:
            formula1: First Formula object
            formula2: Second Formula object

        Returns:
            bool: True if formulas are logically equivalent
        """
        # Get all atomic propositions from both formulas
        all_props = set()
        all_props.update(formula1.get_atomic_propositions())
        all_props.update(formula2.get_atomic_propositions())

        props_list = list(all_props)

        # If no propositions, evaluate directly
        if not props_list:
            try:
                return formula1.evaluate({}) == formula2.evaluate({})
            except:
                return False

        # Check all truth value combinations
        for values in product([True, False], repeat=len(props_list)):
            truth_assignment = dict(zip(props_list, values))

            try:
                val1 = formula1.evaluate(truth_assignment)
                val2 = formula2.evaluate(truth_assignment)

                if val1 != val2:
                    return False
            except:
                return False

        return True

    def find_counter_example(self, premises, conclusion):
        """
        Find a counter-example where premises are true but conclusion is false

        Parameters:
            premises (list): List of Formula objects
            conclusion: Formula object

        Returns:
            dict or None: Truth assignment that serves as counter-example, or None if valid
        """
        # Get all atomic propositions
        all_props = set()
        for premise in premises:
            all_props.update(premise.get_atomic_propositions())
        all_props.update(conclusion.get_atomic_propositions())

        props_list = list(all_props)

        # Try all truth value combinations
        for values in product([True, False], repeat=len(props_list)):
            truth_assignment = dict(zip(props_list, values))

            try:
                # Check if all premises are true
                all_premises_true = True
                for premise in premises:
                    if not premise.evaluate(truth_assignment):
                        all_premises_true = False
                        break

                # If all premises are true but conclusion is false, we have a counter-example
                if all_premises_true and not conclusion.evaluate(truth_assignment):
                    return truth_assignment
            except:
                continue

        return None