"""
Controller for proof execution and management
Handles both automatic and manual proof modes
"""


class ProofController:
    """
    Manages proof derivation and display
    """

    def __init__(self, proof_system, proof_steps_panel, error_controller):
        """
        Initialize proof controller

        Parameters:
            proof_system: ProofSystem instance
            proof_steps_panel: ProofStepsPanel instance
            error_controller: ErrorController instance
        """
        self.proof_system = proof_system
        self.proof_steps_panel = proof_steps_panel
        self.error_controller = error_controller

        # Current mode
        self.mode = "automatic"

        # Selected steps for manual mode
        self.selected_steps = []

    def set_mode(self, mode):
        """
        Set proof mode

        Parameters:
            mode (str): "automatic" or "manual"
        """
        self.mode = mode
        self.selected_steps = []

    def execute_automatic_proof(self):
        """Execute automatic proof"""
        try:
            success, msg = self.proof_system.auto_prove()
            if success:
                self.refresh_display()
            return success, msg
        except Exception as e:
            return False, str(e)

    def apply_rule_manual(self, rule_name, step_indices):
        """Apply a rule manually"""
        success, msg, new_step = self.proof_system.apply_rule(rule_name, step_indices)
        if success:
            self.refresh_display()
        return success, msg

    def refresh_display(self):
        """Refresh the proof steps display"""
        self.proof_steps_panel.clear_all()

        # Display all proof steps
        for step in self.proof_system.proof_steps:
            self.proof_steps_panel.add_step(
                step.index,
                str(step.formula),
                step.justification,
                step.dependencies
            )

        # Show completion status
        if self.proof_system.is_complete:
            self.proof_steps_panel.set_result("Conclusion is VALID", "green")
        else:
            self.proof_steps_panel.set_result("Proof incomplete", "gray")

    def clear(self):
        """Clear the proof"""
        self.proof_system.clear()
        self.proof_steps_panel.clear_all()

    def get_proof_summary(self):
        """
        Get a summary of the current proof

        Returns:
            dict: Summary information
        """
        steps = self.proof_system.get_proof_steps()

        return {
            'total_steps': len(steps),
            'premises_count': len([s for s in steps if s.justification == "Premise"]),
            'is_complete': self.proof_system.is_complete,
            'conclusion': str(self.proof_system.conclusion) if self.proof_system.conclusion else None
        }