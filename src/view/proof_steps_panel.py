"""
Panel for displaying proof steps
Works with UI elements already created in MainWindow
"""

import tkinter as tk


class ProofStepsPanel:
    """Displays the proof derivation steps"""

    def __init__(self, parent_window):
        """Initialize with reference to main window"""
        self._step_click_callback = None
        self.parent_window = parent_window
        self.steps = []

        # References will be set in setup()
        self.proof_text = None
        self.result_label = None

    def set_step_click_callback(self, callback) :
        """Set callback for when a proof step is clicked"""
        self._step_click_callback = callback

    def setup(self):
        """Setup references to UI elements after they're created"""
        self.proof_text = self.parent_window.proof_text
        self.result_label = self.parent_window.result_label

        # Configure text widget
        if self.proof_text:
            self.proof_text.config(state=tk.DISABLED)

            # Configure tags for highlighting
            self.proof_text.tag_configure("premise", foreground="blue")
            self.proof_text.tag_configure("conclusion", foreground="green",
                                         font=('Arial', 10, 'bold'))
            self.proof_text.tag_configure("rule", foreground="purple")
            self.proof_text.tag_configure("highlight", background="yellow")

    def add_step(self, step_number, formula, justification, dependencies=None):
        """Add a proof step to the display"""
        if not self.proof_text:
            return

        self.proof_text.config(state=tk.NORMAL)

        # Format the step
        if dependencies:
            dep_str = f" [{', '.join(map(str, dependencies))}]"
        else:
            dep_str = ""

        step_text = f"{step_number}. {formula} ({justification}{dep_str})\n"

        # Add with appropriate tag
        if justification == "Premise":
            self.proof_text.insert(tk.END, step_text, "premise")
        else:
            self.proof_text.insert(tk.END, step_text, "rule")

        self.proof_text.config(state=tk.DISABLED)
        self.proof_text.see(tk.END)

        # Store step info
        self.steps.append({
            'number': step_number,
            'formula': formula,
            'justification': justification,
            'dependencies': dependencies or []
        })

    def clear_all(self):
        """Clear all proof steps"""
        if self.proof_text:
            self.proof_text.config(state=tk.NORMAL)
            self.proof_text.delete(1.0, tk.END)
            self.proof_text.config(state=tk.DISABLED)
        self.steps.clear()
        self.set_result("", "gray")

    def set_result(self, result_text, color="green"):
        """Update the result label"""
        if self.result_label:
            self.result_label.config(text=result_text, fg=color)
