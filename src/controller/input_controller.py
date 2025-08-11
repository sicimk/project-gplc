"""
Handles user input validation and processing
"""

from model.formula import Formula


class InputController :
	"""
    Manages input validation and formula processing
    """

	def __init__(self, validator, proof_system, premises_panel,
	             conclusions_panel, error_controller) :
		"""
        Initialize input controller

        Parameters:
            validator: FormulaValidator instance
            proof_system: ProofSystem instance  
            premises_panel: PremisesPanel instance
            conclusions_panel: ConclusionsPanel instance
            error_controller: ErrorController instance
        """
		self.validator = validator
		self.proof_system = proof_system
		self.premises_panel = premises_panel
		self.conclusions_panel = conclusions_panel
		self.error_controller = error_controller

		# Store premises and conclusions for easy access
		self.premises = []
		self.conclusions = []

	def handle_add_premise(self) :
		"""Handle adding a premise from the input field"""
		premise_text = self.premises_panel.get_current_input().strip()

		if not premise_text or premise_text == "Type here" :
			self.error_controller.show_error("input", "Please enter a premise")
			return

		# Validate the premise
		is_valid, errors = self.validator.check_valid_characters(premise_text)
		if not is_valid :
			self.error_controller.show_error("syntax",
			                                 f"Invalid characters: {', '.join([e[0] for e in errors])}")
			return

		# Check if well-formed
		is_wf, error_msg = self.validator.check_well_formed(premise_text)
		if not is_wf :
			self.error_controller.show_error("syntax", error_msg)
			return

		# Create formula and add to proof system
		try :
			formula = Formula(premise_text)

			# Check formula type and show notification
			formula_type = self.validator.get_formula_type(formula)
			if formula_type == "tautology" :
				self.error_controller.show_warning("formula",
				                                   "Formula is a TAUTOLOGY (always true)")
			elif formula_type == "contradiction" :
				self.error_controller.show_warning("formula",
				                                   "Formula is a CONTRADICTION (always false)")
			else :
				self.error_controller.show_info("Formula is CONTINGENT")

			success, msg = self.proof_system.add_premise(formula)

			if success :
				# Add to display
				self.premises_panel.add_premise_to_list(premise_text)
				self.premises.append(formula)
				self.error_controller.show_info("Premise added successfully")
			else :
				self.error_controller.show_error("premise", msg)

		except Exception as e :
			self.error_controller.show_error("formula", str(e))

	def handle_add_conclusion(self) :
		"""Handle adding a conclusion from the input field"""
		conclusion_text = self.conclusions_panel.get_current_input().strip()

		if not conclusion_text or conclusion_text == "Type here" :
			self.error_controller.show_error("input",
			                                 "Please enter a conclusion")
			return

		# Validate the conclusion
		is_valid, errors = self.validator.check_valid_characters(
			conclusion_text)
		if not is_valid :
			self.error_controller.show_error("syntax",
			                                 f"Invalid characters: {', '.join([e[0] for e in errors])}")
			return

		# Check if well-formed
		is_wf, error_msg = self.validator.check_well_formed(conclusion_text)
		if not is_wf :
			self.error_controller.show_error("syntax", error_msg)
			return

		# Create formula and set as conclusion
		try :
			formula = Formula(conclusion_text)

			# Check formula type and show notification
			formula_type = self.validator.get_formula_type(formula)
			if formula_type == "tautology" :
				self.error_controller.show_warning("formula",
				                                   "Formula is a TAUTOLOGY (always true)")
			elif formula_type == "contradiction" :
				self.error_controller.show_warning("formula",
				                                   "Formula is a CONTRADICTION (always false)")
			else :
				self.error_controller.show_info("Formula is CONTINGENT")

			success, msg = self.proof_system.set_conclusion(formula)

			if success :
				# Add to display
				self.conclusions_panel.add_conclusion_to_list(conclusion_text)
				self.conclusions.append(formula)
				self.error_controller.show_info("Conclusion set successfully")
			else :
				self.error_controller.show_error("conclusion", msg)

		except Exception as e :
			self.error_controller.show_error("formula", str(e))

	def get_all_premises(self) :
		"""Get all premise formulas"""
		return self.premises.copy()

	def get_conclusion(self) :
		"""Get the current conclusion formula"""
		return self.conclusions[-1] if self.conclusions else None

	def clear_all(self) :
		"""Clear all premises and conclusions"""
		self.premises.clear()
		self.conclusions.clear()