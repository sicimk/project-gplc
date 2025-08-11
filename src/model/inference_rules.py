"""
Implementation of logical inference rules
Contains the 19 inference rules specified in the GPLC project
"""

from model.formula import Formula


from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod

class InferenceRule :
	"""
	Base class for all inference rules
	"""

	def __init__(self, name, abbreviation, description) :
		"""
		Initialize inference rule

		Parameters:
			name (str): Full rule name
			abbreviation (str): Short form (e.g., "MP", "MT")
			description (str): Human-readable description
		"""
		self.name = name
		self.abbreviation = abbreviation
		self.description = description

	def can_apply(self, formulas) :
		"""
		Check if rule can be applied to given formulas

		Parameters:
			formulas: List of Formula objects

		Returns:
			bool: True if rule can be applied
		"""
		raise NotImplementedError("Subclasses must implement can_apply")

	def apply(self, formulas) :
		"""
		Apply rule to derive new formula

		Parameters:
			formulas: List of Formula objects

		Returns:
			Formula: Derived formula, or None if cannot apply
		"""
		raise NotImplementedError("Subclasses must implement apply")

	def __str__(self) :
		return f"{self.name} ({self.abbreviation})"

	def _formulas_equal(self, ast1, ast2) :
		"""Check if two AST nodes are structurally equal"""
		if ast1['type'] != ast2['type'] :
			return False

		if ast1['type'] == 'PROP' :
			return ast1['value'] == ast2['value']
		elif ast1['type'] == 'NOT' :
			return self._formulas_equal(ast1['operand'], ast2['operand'])
		else :
			return (self._formulas_equal(ast1['left'], ast2['left']) and
			        self._formulas_equal(ast1['right'], ast2['right']))


# 1. MODUS PONENS (MP)
class ModusPonens(InferenceRule) :
	"""
	Modus Ponens: If P→Q and P are true, then Q is true
	"""

	def __init__(self) :
		super().__init__(
			"Modus Ponens",
			"MP",
			"If P→Q and P are true, then Q is true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 2 :
			return False

		# Check both possible orders
		for i in range(2) :
			f1, f2 = formulas[i], formulas[1 - i]

			# Check if f2 is an implication
			if f2.ast and f2.ast['type'] == 'IMPLIES' :
				# Check if f1 matches the antecedent
				if self._formulas_equal(f1.ast, f2.ast['left']) :
					return True

		return False

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		# Find which formula is the implication
		for i in range(2) :
			f1, f2 = formulas[i], formulas[1 - i]

			if f2.ast and f2.ast['type'] == 'IMPLIES' :
				if self._formulas_equal(f1.ast, f2.ast['left']) :
					# Return the consequent
					consequent_str = f2.to_string(f2.ast['right'])
					return Formula(consequent_str)

		return None


# 2. MODUS TOLLENS (MT)
class ModusTollens(InferenceRule) :
	"""
	Modus Tollens: If P→Q and ¬Q are true, then ¬P is true
	"""

	def __init__(self) :
		super().__init__(
			"Modus Tollens",
			"MT",
			"If P→Q and ¬Q are true, then ¬P is true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 2 :
			return False

		# Check both possible orders
		for i in range(2) :
			f1, f2 = formulas[i], formulas[1 - i]

			# Check if f1 is an implication and f2 is a negation
			if (f1.ast and f1.ast['type'] == 'IMPLIES' and
					f2.ast and f2.ast['type'] == 'NOT') :
				# Check if negated part matches consequent
				if self._formulas_equal(f2.ast['operand'], f1.ast['right']) :
					return True

		return False

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		# Find which formula is the implication
		for i in range(2) :
			f1, f2 = formulas[i], formulas[1 - i]

			if (f1.ast and f1.ast['type'] == 'IMPLIES' and
					f2.ast and f2.ast['type'] == 'NOT') :
				if self._formulas_equal(f2.ast['operand'], f1.ast['right']) :
					# Return negation of antecedent
					antecedent_str = f1.to_string(f1.ast['left'])
					if f1.ast['left']['type'] == 'PROP' :
						return Formula(f"¬{antecedent_str}")
					else :
						return Formula(f"¬({antecedent_str})")

		return None


# 3. HYPOTHETICAL SYLLOGISM (HS)
class HypotheticalSyllogism(InferenceRule) :
	"""
	Hypothetical Syllogism: If P→Q and Q→R are true, then P→R is true
	"""

	def __init__(self) :
		super().__init__(
			"Hypothetical Syllogism",
			"HS",
			"If P→Q and Q→R are true, then P→R is true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 2 :
			return False

		# Both must be implications
		if not (formulas[0].ast and formulas[0].ast['type'] == 'IMPLIES' and
		        formulas[1].ast and formulas[1].ast['type'] == 'IMPLIES') :
			return False

		# Check if consequent of one matches antecedent of other
		return (self._formulas_equal(formulas[0].ast['right'],
		                             formulas[1].ast['left']) or
		        self._formulas_equal(formulas[1].ast['right'],
		                             formulas[0].ast['left']))

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		f1, f2 = formulas[0], formulas[1]

		# Find the correct order
		if self._formulas_equal(f1.ast['right'], f2.ast['left']) :
			# f1: P→Q, f2: Q→R
			antecedent = f1.to_string(f1.ast['left'])
			consequent = f2.to_string(f2.ast['right'])
		else :
			# f2: P→Q, f1: Q→R
			antecedent = f2.to_string(f2.ast['left'])
			consequent = f1.to_string(f1.ast['right'])

		return Formula(f"{antecedent} → {consequent}")


# 4. DISJUNCTIVE SYLLOGISM (DS)
class DisjunctiveSyllogism(InferenceRule) :
	"""
	Disjunctive Syllogism: If P∨Q and ¬P are true, then Q is true
	"""

	def __init__(self) :
		super().__init__(
			"Disjunctive Syllogism",
			"DS",
			"If P∨Q and ¬P are true, then Q is true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 2 :
			return False

		# Check both orders
		for i in range(2) :
			f1, f2 = formulas[i], formulas[1 - i]

			# Check if f1 is disjunction and f2 is negation
			if (f1.ast and f1.ast['type'] == 'OR' and
					f2.ast and f2.ast['type'] == 'NOT') :
				# Check if negated part matches either disjunct
				if (self._formulas_equal(f2.ast['operand'], f1.ast['left']) or
						self._formulas_equal(f2.ast['operand'],
						                     f1.ast['right'])) :
					return True

		return False

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		# Find which formula is the disjunction
		for i in range(2) :
			f1, f2 = formulas[i], formulas[1 - i]

			if (f1.ast and f1.ast['type'] == 'OR' and
					f2.ast and f2.ast['type'] == 'NOT') :
				# Check which disjunct is negated
				if self._formulas_equal(f2.ast['operand'], f1.ast['left']) :
					# Return right disjunct
					result_str = f1.to_string(f1.ast['right'])
					return Formula(result_str)
				elif self._formulas_equal(f2.ast['operand'], f1.ast['right']) :
					# Return left disjunct
					result_str = f1.to_string(f1.ast['left'])
					return Formula(result_str)

		return None


# 5. CONJUNCTION INTRODUCTION (CI)
class ConjunctionIntroduction(InferenceRule) :
	"""
	Conjunction Introduction: If P and Q are true, then P∧Q is true
	"""

	def __init__(self) :
		super().__init__(
			"Conjunction Introduction",
			"CI",
			"If P and Q are true, then P∧Q is true"
			)

	def can_apply(self, formulas) :
		return len(formulas) == 2

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		f1_str = str(formulas[0])
		f2_str = str(formulas[1])

		# Add parentheses if needed
		if formulas[0].ast['type'] in ['IMPLIES', 'IFF', 'OR', 'XOR'] :
			f1_str = f"({f1_str})"
		if formulas[1].ast['type'] in ['IMPLIES', 'IFF', 'OR', 'XOR'] :
			f2_str = f"({f2_str})"

		return Formula(f"{f1_str} ∧ {f2_str}")


# 6. CONJUNCTION ELIMINATION (CE)
class ConjunctionElimination(InferenceRule) :
	"""
	Conjunction Elimination: If P∧Q is true, then P and Q are each true individually
	"""

	def __init__(self) :
		super().__init__(
			"Conjunction Elimination",
			"CE",
			"If P∧Q is true, then P and Q are each true individually"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 1 :
			return False

		return formulas[0].ast and formulas[0].ast['type'] == 'AND'

	def apply(self, formulas, which='left') :
		"""
		Apply conjunction elimination

		Parameters:
			formulas: List containing one conjunction formula
			which: 'left' or 'right' - which part to extract
		"""
		if not self.can_apply(formulas) :
			return None

		conjunction = formulas[0]
		if which == 'left' :
			result_str = conjunction.to_string(conjunction.ast['left'])
		else :
			result_str = conjunction.to_string(conjunction.ast['right'])

		return Formula(result_str)


# 7. ADDITION (ADD)
class Addition(InferenceRule) :
	"""
	Addition: If P is true, then P∨Q is true
	"""

	def __init__(self) :
		super().__init__(
			"Addition",
			"ADD",
			"If P is true, then P∨Q is true"
			)

	def can_apply(self, formulas) :
		return len(formulas) == 1

	def apply(self, formulas, **kwargs) :
		"""
		Apply addition (disjunction introduction)

		Parameters:
			formulas: List containing one formula
			**kwargs: Additional parameters (added_formula_str)
		"""
		if not self.can_apply(formulas) :
			return None

		added_formula_str = kwargs.get('added_formula_str',
		                               'B')  # Default to 'B'

		f1_str = str(formulas[0])

		# Add parentheses if needed
		if formulas[0].ast['type'] in ['IMPLIES', 'IFF'] :
			f1_str = f"({f1_str})"

		# Parse the added formula to check if it needs parentheses
		try :
			added = Formula(added_formula_str)
			if added.ast['type'] in ['IMPLIES', 'IFF'] :
				added_formula_str = f"({added_formula_str})"
		except :
			pass

		return Formula(f"{f1_str} ∨ {added_formula_str}")


# 8. SIMPLIFICATION (SIMP)
class Simplification(InferenceRule) :
	"""
	Simplification: If P∧Q is true, then P or Q is true individually
	"""

	def __init__(self) :
		super().__init__(
			"Simplification",
			"SIMP",
			"If P∧Q is true, then P or Q is true individually"
			)
		# This is essentially the same as Conjunction Elimination
		self._conj_elim = ConjunctionElimination()

	def can_apply(self, formulas) :
		return self._conj_elim.can_apply(formulas)

	def apply(self, formulas, which='left') :
		return self._conj_elim.apply(formulas, which)


# 9. BICONDITIONAL INTRODUCTION (BI)
class BiconditionalIntroduction(InferenceRule) :
	"""
	Biconditional Introduction: If P→Q and Q→P are true, then P↔Q is true
	"""

	def __init__(self) :
		super().__init__(
			"Biconditional Introduction",
			"BI",
			"If P→Q and Q→P are true, then P↔Q is true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 2 :
			return False

		# Both must be implications
		if not (formulas[0].ast and formulas[0].ast['type'] == 'IMPLIES' and
		        formulas[1].ast and formulas[1].ast['type'] == 'IMPLIES') :
			return False

		# Check if they are converses of each other
		f1, f2 = formulas[0], formulas[1]
		return (self._formulas_equal(f1.ast['left'], f2.ast['right']) and
		        self._formulas_equal(f1.ast['right'], f2.ast['left']))

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		f1 = formulas[0]
		left = f1.to_string(f1.ast['left'])
		right = f1.to_string(f1.ast['right'])

		return Formula(f"{left} ↔ {right}")


# 10. BICONDITIONAL ELIMINATION (BE)
class BiconditionalElimination(InferenceRule) :
	"""
	Biconditional Elimination: If P↔Q is true, then P→Q and Q→P are true
	"""

	def __init__(self) :
		super().__init__(
			"Biconditional Elimination",
			"BE",
			"If P↔Q is true, then P→Q and Q→P are true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 1 :
			return False

		return formulas[0].ast and formulas[0].ast['type'] == 'IFF'

	def apply(self, formulas, direction='forward') :
		"""
		Apply biconditional elimination

		Parameters:
			formulas: List containing one biconditional
			direction: 'forward' for P→Q, 'backward' for Q→P
		"""
		if not self.can_apply(formulas) :
			return None

		biconditional = formulas[0].ast
		left = formulas[0].to_string(biconditional['left'])
		right = formulas[0].to_string(biconditional['right'])

		if direction == 'forward' :
			return Formula(f"{left} → {right}")
		else :
			return Formula(f"{right} → {left}")


# 11. DOUBLE NEGATION (DN)
class DoubleNegation(InferenceRule) :
	"""
	Double Negation: If ¬¬P is true, then P is true (and vice versa)
	"""

	def __init__(self) :
		super().__init__(
			"Double Negation",
			"DN",
			"If ¬¬P is true, then P is true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 1 :
			return False

		f = formulas[0]
		# Check if it's a double negation or if we can add double negation
		if f.ast and f.ast['type'] == 'NOT' :
			if f.ast['operand']['type'] == 'NOT' :
				return True  # Can eliminate
		return True  # Can always introduce double negation

	def apply(self, formulas, mode='eliminate') :
		"""
		Apply double negation

		Parameters:
			formulas: List containing one formula
			mode: 'eliminate' to remove ¬¬, 'introduce' to add ¬¬
		"""
		if not self.can_apply(formulas) :
			return None

		f = formulas[0]

		if mode == 'eliminate' :
			# Check if it's actually a double negation
			if (f.ast and f.ast['type'] == 'NOT' and
					f.ast['operand']['type'] == 'NOT') :
				# Extract the doubly negated formula
				inner = f.ast['operand']['operand']
				result_str = f.to_string(inner)
				return Formula(result_str)
			else :
				return None
		else :  # introduce
			# Only add parentheses if needed
			if f.ast['type'] == 'PROP' :
				return Formula(f"¬¬{str(f)}")
			else :
				return Formula(f"¬¬({str(f)})")


# 12. DE MORGAN'S LAW 1 (DML1)
class DeMorgansLaw1(InferenceRule) :
	"""
	De Morgan's Law 1: ¬(P∧Q) is equivalent to ¬P∨¬Q
	"""

	def __init__(self) :
		super().__init__(
			"De Morgan's Law 1",
			"DML1",
			"¬(P∧Q) is equivalent to ¬P∨¬Q"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 1 :
			return False

		f = formulas[0]
		# Check if it's negation of conjunction
		if f.ast and f.ast['type'] == 'NOT' :
			if f.ast['operand']['type'] == 'AND' :
				return True
		# Check if it's disjunction of negations
		elif f.ast and f.ast['type'] == 'OR' :
			if (f.ast['left']['type'] == 'NOT' and
					f.ast['right']['type'] == 'NOT') :
				return True

		return False

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		f = formulas[0]

		if f.ast['type'] == 'NOT' :  # ¬(P∧Q) ➜ ¬P∨¬Q
			conj = f.ast['operand']
			left = f.to_string(conj['left'])
			right = f.to_string(conj['right'])
			left_neg = f"¬{left}" if conj['left'][
				                         'type'] == 'PROP' else f"¬({left})"
			right_neg = f"¬{right}" if conj['right'][
				                           'type'] == 'PROP' else f"¬({right})"
			return Formula(f"{left_neg} ∨ {right_neg}")

		elif f.ast['type'] == 'OR' :  # ¬P∨¬Q ➜ ¬(P∧Q)
			left_inner = f.ast['left']['operand']
			right_inner = f.ast['right']['operand']
			l = f.to_string(left_inner)
			r = f.to_string(right_inner)
			return Formula(f"¬({l} ∧ {r})")

		return None


# 13. DE MORGAN'S LAW 2 (DML2)
class DeMorgansLaw2(InferenceRule) :
	"""
	De Morgan's Law 2: ¬(P∨Q) is equivalent to ¬P∧¬Q
	"""

	def __init__(self) :
		super().__init__(
			"De Morgan's Law 2",
			"DML2",
			"¬(P∨Q) is equivalent to ¬P∧¬Q"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 1 :
			return False

		f = formulas[0]
		# Check if it's negation of disjunction
		if f.ast and f.ast['type'] == 'NOT' :
			if f.ast['operand']['type'] == 'OR' :
				return True
		# Check if it's conjunction of negations
		elif f.ast and f.ast['type'] == 'AND' :
			if (f.ast['left']['type'] == 'NOT' and
					f.ast['right']['type'] == 'NOT') :
				return True

		return False

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		f = formulas[0]

		if f.ast['type'] == 'NOT' :  # ¬(P∨Q) ➜ ¬P∧¬Q
			disj = f.ast['operand']
			left = f.to_string(disj['left'])
			right = f.to_string(disj['right'])
			left_neg = f"¬{left}" if disj['left'][
				                         'type'] == 'PROP' else f"¬({left})"
			right_neg = f"¬{right}" if disj['right'][
				                           'type'] == 'PROP' else f"¬({right})"
			return Formula(f"{left_neg} ∧ {right_neg}")

		elif f.ast['type'] == 'AND' :  # ¬P∧¬Q ➜ ¬(P∨Q)
			left_inner = f.ast['left']['operand']
			right_inner = f.ast['right']['operand']
			left_str = f.to_string(left_inner)
			right_str = f.to_string(right_inner)
			return Formula(f"¬({left_str} ∨ {right_str})")

		return None


# 14. TRANSPOSITION (TRANS)
class Transposition(InferenceRule) :
	"""
	Transposition: P→Q is equivalent to ¬Q→¬P
	"""

	def __init__(self) :
		super().__init__(
			"Transposition",
			"TRANS",
			"P→Q is equivalent to ¬Q→¬P"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 1 :
			return False

		f = formulas[0]
		# Must be an implication
		return f.ast and f.ast['type'] == 'IMPLIES'

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		implication = formulas[0].ast
		antecedent = formulas[0].to_string(implication['left'])
		consequent = formulas[0].to_string(implication['right'])

		# Check if already in contrapositive form
		if (implication['left']['type'] == 'NOT' and
				implication['right']['type'] == 'NOT') :  # already ¬Q→¬P
			# Convert ¬Q→¬P back to P→Q
			p = formulas[0].to_string(implication['right']['operand'])
			q = formulas[0].to_string(implication['left']['operand'])
			return Formula(f"{p} → {q}")
		else :  # P→Q ➜ ¬Q→¬P
			neg_conseq = f"¬{consequent}" if implication['right'][
				                       'type'] == 'PROP' else f"¬({consequent})"
			neg_antec = f"¬{antecedent}" if implication['left'][
				                       'type'] == 'PROP' else f"¬({antecedent})"
			return Formula(f"{neg_conseq} → {neg_antec}")


# 15. IMPLICATION (IMPL)
class Implication(InferenceRule) :
	"""
	Implication: P→Q is equivalent to ¬P∨Q
	"""

	def __init__(self) :
		super().__init__(
			"Implication",
			"IMPL",
			"P→Q is equivalent to ¬P∨Q"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 1 :
			return False

		f = formulas[0]
		# Check if it's an implication or a disjunction with negated first part
		if f.ast['type'] == 'IMPLIES' :
			return True
		elif f.ast['type'] == 'OR' and f.ast['left']['type'] == 'NOT' :
			return True

		return False

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		f = formulas[0]

		if f.ast['type'] == 'IMPLIES' :  # P→Q ➜ ¬P∨Q
			p = f.to_string(f.ast['left'])
			q = f.to_string(f.ast['right'])
			neg_p = f"¬{p}" if f.ast['left']['type'] == 'PROP' else f"¬({p})"
			return Formula(f"{neg_p} ∨ {q}")

		elif f.ast['type'] == 'OR' and f.ast['left']['type'] == 'NOT' : # ¬P∨Q ➜ P→Q
			# Convert ¬P∨Q to P→Q
			p = f.to_string(f.ast['left']['operand'])
			q = f.to_string(f.ast['right'])
			return Formula(f"{p} → {q}")

		return None


# 16. EXPORTATION (EXP)
class Exportation(InferenceRule) :
	"""
	Exportation: P→(Q→R) is equivalent to (P∧Q)→R
	"""

	def __init__(self) :
		super().__init__(
			"Exportation",
			"EXP",
			"P→(Q→R) is equivalent to (P∧Q)→R"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 1 :
			return False

		f = formulas[0]
		if not (f.ast and f.ast['type'] == 'IMPLIES') :
			return False

		# Check for P→(Q→R) pattern
		if f.ast['right']['type'] == 'IMPLIES' :
			return True

		# Check for (P∧Q)→R pattern
		if f.ast['left']['type'] == 'AND' :
			return True

		return False

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		f = formulas[0]

		if f.ast['right']['type'] == 'IMPLIES' :
			# Convert P→(Q→R) to (P∧Q)→R
			p = f.to_string(f.ast['left'])
			q = f.to_string(f.ast['right']['left'])
			r = f.to_string(f.ast['right']['right'])
			return Formula(f"({p} ∧ {q}) → {r}")

		elif f.ast['left']['type'] == 'AND' :
			# Convert (P∧Q)→R to P→(Q→R)
			p = f.to_string(f.ast['left']['left'])
			q = f.to_string(f.ast['left']['right'])
			r = f.to_string(f.ast['right'])
			return Formula(f"{p} → ({q} → {r})")

		return None


# 17. RESOLUTION (RES)
class Resolution(InferenceRule) :
	"""
	Resolution: If P∨Q and ¬P∨R are true, then Q∨R is true
	"""

	def __init__(self) :
		super().__init__(
			"Resolution",
			"RES",
			"If P∨Q and ¬P∨R are true, then Q∨R is true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 2 :
			return False

		# Both must be disjunctions
		if not (formulas[0].ast and formulas[0].ast['type'] == 'OR' and
		        formulas[1].ast and formulas[1].ast['type'] == 'OR') :
			return False

		# Check if we have complementary literals
		f1, f2 = formulas[0], formulas[1]

		# Check all combinations for complementary literals
		for i in ['left', 'right'] :
			for j in ['left', 'right'] :
				lit1 = f1.ast[i]
				lit2 = f2.ast[j]

				# Check if one is negation of the other
				if lit1['type'] == 'NOT' and self._formulas_equal(
						lit1['operand'], lit2) :
					return True
				if lit2['type'] == 'NOT' and self._formulas_equal(
						lit2['operand'], lit1) :
					return True

		return False

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		f1, f2 = formulas[0], formulas[1]

		# Find the complementary literals and remaining parts
		for i in ['left', 'right'] :
			for j in ['left', 'right'] :
				lit1 = f1.ast[i]
				lit2 = f2.ast[j]

				# Get the other parts
				other1 = 'right' if i == 'left' else 'left'
				other2 = 'right' if j == 'left' else 'left'

				# Check if lit1 is ¬lit2
				if lit1['type'] == 'NOT' and self._formulas_equal(
						lit1['operand'], lit2) :
					q = f1.to_string(f1.ast[other1])
					r = f2.to_string(f2.ast[other2])
					return Formula(f"{q} ∨ {r}")

				# Check if lit2 is ¬lit1
				if lit2['type'] == 'NOT' and self._formulas_equal(
						lit2['operand'], lit1) :
					q = f1.to_string(f1.ast[other1])
					r = f2.to_string(f2.ast[other2])
					return Formula(f"{q} ∨ {r}")

		return None


# 18. ABSORPTION (ABS)
class Absorption(InferenceRule) :
	"""
	Absorption: If P→Q is true, then P→(P∧Q) is true
	"""

	def __init__(self) :
		super().__init__(
			"Absorption",
			"ABS",
			"If P→Q is true, then P→(P∧Q) is true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 1 :
			return False

		return formulas[0].ast and formulas[0].ast['type'] == 'IMPLIES'

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		implication = formulas[0].ast
		p = formulas[0].to_string(implication['left'])

		# Check if consequent is already P∧Q
		if implication['right']['type'] == 'AND' :
			# Check if it's P∧Q format
			conj = implication['right']
			if self._formulas_equal(conj['left'], implication['left']) :
				# Convert P→(P∧Q) back to P→Q
				q = formulas[0].to_string(conj['right'])
				return Formula(f"{p} → {q}")
			elif self._formulas_equal(conj['right'], implication['left']) :
				# Convert P→(Q∧P) back to P→Q
				q = formulas[0].to_string(conj['left'])
				return Formula(f"{p} → {q}")
		else :
			# Convert P→Q to P→(P∧Q)
			q = formulas[0].to_string(implication['right'])
			return Formula(f"{p} → ({p} ∧ {q})")

		return None


# 19. CONSTRUCTIVE DILEMMA (CD)
class ConstructiveDilemma(InferenceRule) :
	"""
	Constructive Dilemma: If P→Q, R→S and P∨R are true, then Q∨S is true
	"""

	def __init__(self) :
		super().__init__(
			"Constructive Dilemma",
			"CD",
			"If P→Q, R→S and P∨R are true, then Q∨S is true"
			)

	def can_apply(self, formulas) :
		if len(formulas) != 3 :
			return False

		# Need two implications and one disjunction
		implications = []
		disjunction = None

		for f in formulas :
			if f.ast['type'] == 'IMPLIES' :
				implications.append(f)
			elif f.ast['type'] == 'OR' :
				disjunction = f

		if len(implications) != 2 or disjunction is None :
			return False

		# Check if disjunction contains antecedents of implications
		imp1, imp2 = implications[0], implications[1]
		disj_left = disjunction.ast['left']
		disj_right = disjunction.ast['right']

		# Check all possible matches
		return (
				(self._formulas_equal(disj_left, imp1.ast['left']) and
				 self._formulas_equal(disj_right, imp2.ast['left'])) or
				(self._formulas_equal(disj_left, imp2.ast['left']) and
				 self._formulas_equal(disj_right, imp1.ast['left']))
		)

	def apply(self, formulas) :
		if not self.can_apply(formulas) :
			return None

		# Separate implications and disjunction
		implications = []
		disjunction = None

		for f in formulas :
			if f.ast['type'] == 'IMPLIES' :
				implications.append(f)
			elif f.ast['type'] == 'OR' :
				disjunction = f

		imp1, imp2 = implications[0], implications[1]

		# Match antecedents with disjuncts
		if (self._formulas_equal(disjunction.ast['left'], imp1.ast['left']) and
				self._formulas_equal(disjunction.ast['right'],
				                     imp2.ast['left'])) :
			# P∨R matches with P→Q and R→S
			q = imp1.to_string(imp1.ast['right'])
			s = imp2.to_string(imp2.ast['right'])
			return Formula(f"{q} ∨ {s}")
		else :
			# P∨R matches with R→S and P→Q (reversed)
			q = imp2.to_string(imp2.ast['right'])
			s = imp1.to_string(imp1.ast['right'])
			return Formula(f"{q} ∨ {s}")


def get_all_rules() :
	"""
	Get list of all 19 available inference rules

	Returns:
		list: List of InferenceRule instances
	"""
	return [
		ModusPonens(),
		ModusTollens(),
		HypotheticalSyllogism(),
		DisjunctiveSyllogism(),
		ConjunctionIntroduction(),
		ConjunctionElimination(),
		Addition(),
		Simplification(),
		BiconditionalIntroduction(),
		BiconditionalElimination(),
		DoubleNegation(),
		DeMorgansLaw1(),
		DeMorgansLaw2(),
		Transposition(),
		Implication(),
		Exportation(),
		Resolution(),
		Absorption(),
		ConstructiveDilemma()
		]


def get_rule_by_name(name) :
	"""
	Get an inference rule by its name or abbreviation

	Parameters:
		name (str): Name or abbreviation of the rule

	Returns:
		InferenceRule or None: The rule instance if found
	"""
	for rule in get_all_rules() :
		if (rule.name.lower() == name.lower() or
				rule.abbreviation.lower() == name.lower()) :
			return rule
	return None


def get_rule_by_abbreviation(abbrev) :
	"""
	Get an inference rule by its abbreviation

	Parameters:
		abbrev (str): Abbreviation of the rule (e.g., "MP", "MT")

	Returns:
		InferenceRule or None: The rule instance if found
	"""
	for rule in get_all_rules() :
		if rule.abbreviation.upper() == abbrev.upper() :
			return rule
	return None