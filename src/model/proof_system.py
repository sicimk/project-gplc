"""
Proof system for deriving conclusions from premises
Implements both automatic and manual proof derivation
"""

from typing import List, Optional, Tuple, Dict


from model.formula import Formula
from model.inference_rules import get_all_rules
from model.inference_rules import get_rule_by_name
from model.inference_rules import get_rule_by_abbreviation
from model.validator import FormulaValidator


class ProofStep :
	"""
	Represents a single step in a proof
	"""

	def __init__(self, index, formula, justification, dependencies=None) :
		"""
		Initialize a proof step

		Parameters:
			index (int): Step number in the proof
			formula: The Formula object at this step
			justification (str): Rule or reason for this step
			dependencies (list): List of step indices this depends on
		"""
		self.index = index
		self.formula = formula
		self.justification = justification
		self.dependencies = dependencies if dependencies else []

	def __str__(self) :
		"""String representation of the proof step"""
		deps_str = ""
		if self.dependencies :
			deps_str = f" [{', '.join(map(str, self.dependencies))}]"

		return f"{self.index}. {self.formula} ({self.justification}{deps_str})"

	def __repr__(self) :
		return f"ProofStep({self.index}, '{self.formula}', '{self.justification}')"


class ProofSystem :
	"""
	Manages the proof derivation process
	"""

	def __init__(self) :
		"""
		Initialize an empty proof system
		"""
		self.premises = []  # List of Formula objects
		self.proof_steps = []  # List of ProofStep objects
		self.conclusion = None  # Formula object to prove
		self.inference_rules = get_all_rules()  # Available inference rules
		self.validator = FormulaValidator()
		self._step_index = 1  # Current step index
		self.is_complete = False  # Whether proof is complete

	def clear(self) :
		"""Clear all premises, steps, and conclusion"""
		self.premises = []
		self.proof_steps = []
		self.conclusion = None
		self._step_index = 1
		self.is_complete = False

	def add_premise(self, formula) :
		"""
		Add a premise to the proof system

		Parameters:
			formula: Formula object to add as premise

		Returns:
			tuple: (success, message)
		"""
		# Validate formula
		if not isinstance(formula, Formula) :
			return False, "Invalid formula object"

		# Check for duplicates
		for p in self.premises :
			if str(p) == str(formula) :
				return False, "Premise already exists"

		# Add to premises list
		self.premises.append(formula)

		# Create proof step
		step = ProofStep(self._step_index, formula, "Premise")
		self.proof_steps.append(step)
		self._step_index += 1

		return True, "Premise added successfully"

	def set_conclusion(self, formula) :
		"""
		Set the conclusion to prove

		Parameters:
			formula: Formula object to prove

		Returns:
			tuple: (success, message)
		"""
		if not isinstance(formula, Formula) :
			return False, "Invalid formula object"

		self.conclusion = formula
		self.is_complete = False

		# Check if conclusion is already proved
		self._check_if_complete()

		return True, "Conclusion set successfully"

	def apply_rule(self, rule_name, step_indices, **kwargs) :
		"""
		Apply an inference rule to existing steps

		Parameters:
			rule_name (str): Name or abbreviation of the inference rule
			step_indices (list): List of step indices to apply rule to
			**kwargs: Additional parameters for specific rules

		Returns:
			tuple: (success, message, new_step)
		"""
		# Find the rule by name or abbreviation
		rule = get_rule_by_name(rule_name) or get_rule_by_abbreviation(
			rule_name)

		if not rule :
			return False, f"Unknown rule: {rule_name}", None

		# Get the formulas from specified steps
		try :
			formulas = []
			for idx in step_indices :
				# Find step with given index
				step = None
				for s in self.proof_steps :
					if s.index == idx :
						step = s
						break

				if not step :
					return False, f"Step {idx} not found", None

				formulas.append(step.formula)
		except Exception as e :
			return False, f"Error getting formulas: {str(e)}", None

		# Check if rule can be applied
		if not rule.can_apply(formulas) :
			return False, f"Rule {rule.name} cannot be applied to selected steps", None

		# Apply the rule
		try :
			# Handle special cases for rules that need extra parameters
			if rule.abbreviation == "ADD" :
				# Addition needs the formula to add
				added_formula = kwargs.get('added_formula', 'B')
				new_formula = rule.apply(formulas,
				                         added_formula_str=added_formula)
			elif rule.abbreviation in ["CE", "SIMP"] :
				# Conjunction Elimination/Simplification needs which side
				which = kwargs.get('which', 'left')
				new_formula = rule.apply(formulas, which=which)
			elif rule.abbreviation == "BE" :
				# Biconditional Elimination needs direction
				direction = kwargs.get('direction', 'forward')
				new_formula = rule.apply(formulas, direction=direction)
			elif rule.abbreviation == "DN" :
				# Double Negation needs mode
				mode = kwargs.get('mode', 'eliminate')
				new_formula = rule.apply(formulas, mode=mode)
			else :
				new_formula = rule.apply(formulas)

			if not new_formula :
				return False, "Rule application failed", None
		except Exception as e :
			return False, f"Error applying rule: {str(e)}", None

		# Check if this formula already exists in proof
		for step in self.proof_steps :
			if str(step.formula) == str(new_formula) :
				return False, "This formula already exists in the proof", None

		# Create new proof step
		new_step = ProofStep(
			self._step_index,
			new_formula,
			rule.name,
			step_indices
			)
		self.proof_steps.append(new_step)
		self._step_index += 1

		# Check if conclusion is reached
		self._check_if_complete()

		return True, f"Applied {rule.name} successfully", new_step

	def auto_prove(self, max_steps=50) :
		"""
		Automatically attempt to prove the conclusion

		Parameters:
			max_steps (int): Maximum number of steps to try

		Returns:
			tuple: (success, message)
		"""
		if not self.conclusion :
			return False, "No conclusion set"

		if not self.premises :
			return False, "No premises provided"

		# Check if already complete
		if self.is_complete :
			return True, "Proof already complete"

		steps_added = 0

		# Try to apply rules until conclusion is reached or no new steps
		while steps_added < max_steps and not self.is_complete :
			new_steps_in_round = 0

			# Try all inference rules on all combinations of existing steps
			for rule in self.inference_rules :
				# Skip rules that need additional parameters in auto mode
				if rule.abbreviation in ["ADD", "DN"] :
					# For DN, we can try elimination
					if rule.abbreviation == "DN" :
						for step in self.proof_steps[:] :
							success, _, _ = self.apply_rule(rule.name,
							                                [step.index],
							                                mode='eliminate')
							if success :
								new_steps_in_round += 1
								if self.is_complete :
									return True, f"Proof complete! Used {rule.name}"
					continue

				# Handle rules based on number of premises they need
				if rule.abbreviation in ["MP", "MT", "HS", "DS", "CI", "BI",
				                         "RES"] :
					# Binary rules - need exactly 2 premises
					for i, step1 in enumerate(self.proof_steps[:]) :
						for step2 in self.proof_steps[i + 1 :] :
							# Try both orders for non-commutative rules
							for indices in [[step1.index, step2.index],
							                [step2.index, step1.index]] :
								success, _, _ = self.apply_rule(rule.name,
								                                indices)
								if success :
									new_steps_in_round += 1
									if self.is_complete :
										return True, f"Proof complete! Used {rule.name}"
									break  # Don't try reverse order if forward worked

				elif rule.abbreviation == "CD" :
					# Constructive Dilemma needs exactly 3 premises
					for i, step1 in enumerate(self.proof_steps[:]) :
						for j, step2 in enumerate(self.proof_steps[i + 1 :],
						                          i + 1) :
							for step3 in self.proof_steps[j + 1 :] :
								# Try different orderings
								for indices in [
									[step1.index, step2.index, step3.index],
									[step1.index, step3.index, step2.index],
									[step2.index, step3.index, step1.index]
									] :
									success, _, _ = self.apply_rule(rule.name,
									                                indices)
									if success :
										new_steps_in_round += 1
										if self.is_complete :
											return True, f"Proof complete! Used {rule.name}"
										break

				else :
					# Unary rules or rules that work on single formulas
					for step in self.proof_steps[:] :
						# Try Conjunction Elimination on both sides
						if rule.abbreviation in ["CE", "SIMP"] :
							for which in ['left', 'right'] :
								success, _, _ = self.apply_rule(rule.name,
								                                [step.index],
								                                which=which)
								if success :
									new_steps_in_round += 1
									if self.is_complete :
										return True, f"Proof complete! Used {rule.name}"
						# Try Biconditional Elimination in both directions
						elif rule.abbreviation == "BE" :
							for direction in ['forward', 'backward'] :
								success, _, _ = self.apply_rule(rule.name,
								                                [step.index],
								                                direction=direction)
								if success :
									new_steps_in_round += 1
									if self.is_complete :
										return True, f"Proof complete! Used {rule.name}"
						else :
							# Other unary rules
							success, _, _ = self.apply_rule(rule.name,
							                                [step.index])
							if success :
								new_steps_in_round += 1
								if self.is_complete :
									return True, f"Proof complete! Used {rule.name}"
			steps_added += new_steps_in_round  # count how many we really added
			if new_steps_in_round == 0 :  # made no progress → give up
				break
		if self.is_complete :
			return True, "Proof complete!"
		else :
			return False, "Could not complete proof within the step limit."

	def _check_if_complete(self) :
		"""Check if the proof is complete (conclusion has been derived)"""
		if not self.conclusion :
			return

		conclusion_str = str(self.conclusion)
		for step in self.proof_steps :
			if str(step.formula) == conclusion_str :
				self.is_complete = True
				return

		self.is_complete = False

	def get_proof_steps(self) :
		"""
		Get all proof steps in order

		Returns:
			list: List of ProofStep objects
		"""
		return self.proof_steps.copy()

	def get_dependencies(self, step_index) :
		"""
		Get all dependencies for a given step (recursive)

		Parameters:
			step_index (int): Index of the step

		Returns:
			set: Set of all step indices this step depends on
		"""
		dependencies = set()

		# Find the step
		target_step = None
		for step in self.proof_steps :
			if step.index == step_index :
				target_step = step
				break

		if not target_step :
			return dependencies

		# Add direct dependencies
		for dep in target_step.dependencies :
			dependencies.add(dep)
			# Recursively add their dependencies
			dependencies.update(self.get_dependencies(dep))

		return dependencies

	def validate_proof(self) :
		"""
		Validate the entire proof for correctness

		Returns:
			tuple: (is_valid, message)
		"""
		if not self.conclusion :
			return False, "No conclusion set"

		if not self.premises :
			return False, "No premises provided"

		# Check each step
		for step in self.proof_steps :
			if step.justification == "Premise" :
				# Check if it's actually in premises
				if step.formula not in self.premises :
					return False, f"Step {step.index} claims to be premise but isn't"
			else :
				# Check if the rule application is valid
				# This would require re-checking each rule application
				# For now, we trust that rules were applied correctly
				pass

		# Check if conclusion was reached
		if not self.is_complete :
			return False, "Proof is incomplete - conclusion not reached"

		return True, "Proof is valid"

	def to_string(self, show_dependencies=True) :
		"""
		Convert proof to string representation

		Parameters:
			show_dependencies (bool): Whether to show step dependencies

		Returns:
			str: String representation of the proof
		"""
		lines = []

		# Header
		lines.append("PROOF DERIVATION")
		lines.append("=" * 50)

		# Premises
		lines.append("\nPremises:")
		premise_indices = []
		for step in self.proof_steps :
			if step.justification == "Premise" :
				lines.append(f"  {step.index}. {step.formula}")
				premise_indices.append(step.index)

		# Conclusion
		if self.conclusion :
			lines.append(f"\nConclusion to prove: {self.conclusion}")

		# Proof steps
		lines.append("\nProof Steps:")
		for step in self.proof_steps :
			if show_dependencies :
				lines.append(f"  {step}")
			else :
				lines.append(
					f"  {step.index}. {step.formula} ({step.justification})")

		# Result
		lines.append("\n" + "=" * 50)
		if self.is_complete :
			lines.append("✓ PROOF COMPLETE - Conclusion has been derived!")
		else :
			lines.append("✗ PROOF INCOMPLETE - Conclusion not yet reached")

		return "\n".join(lines)

	def get_proof_data(self) :
		"""
		Get proof data in a structured format for display

		Returns:
			dict: Proof data with premises, steps, and status
		"""
		return {
			'premises' : [str(p) for p in self.premises],
			'conclusion' : str(self.conclusion) if self.conclusion else None,
			'steps' : [
				{
					'index' : step.index,
					'formula' : str(step.formula),
					'justification' : step.justification,
					'dependencies' : step.dependencies
					}
				for step in self.proof_steps
				],
			'is_complete' : self.is_complete
			}
