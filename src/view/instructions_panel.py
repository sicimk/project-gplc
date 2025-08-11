"""
Instructions panel for GPLC
Displays input format instructions and usage guidance for users
"""

import tkinter as tk
from tkinter import scrolledtext


class InstructionsPanel:
    """
    Panel that displays instructions on how to use the GPLC application
    Shows input format, logical operators, and functionality guidance
    """

    def __init__(self, parent):
        """
        Initialize the instructions panel

        Parameters:
            parent: Parent tkinter widget (should be a LabelFrame)
        """
        self.parent = parent
        self.text_widget = None

        self._setup_panel()
        self._load_instruction_content()

    def _setup_panel(self):
        """
        Setup the panel layout with scrollable text widget
        """
        # Configure parent frame
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        # Create scrollable text widget for instructions
        self.text_widget = scrolledtext.ScrolledText(
            self.parent,
            wrap=tk.WORD,           # Wrap at word boundaries
            state='disabled',       # Read-only
            font=('Arial', 9),      # Readable font size
            bg='#f8f8f8',          # Light background
            padx=5,                 # Internal padding
            pady=5
        )
        self.text_widget.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)

    def _load_instruction_content(self):
        """
        Load the instruction text content
        """
        # Define the instruction text
        instructions = """HOW TO USE GPLC

INPUT FORMULAS:
• Use capital letters A-Z for atomic propositions
• Click buttons below to insert symbols into input fields
• Type directly into input fields

LOGICAL CONNECTIVES:
Standard Notation    Alternative
     &                   AND
     |                   OR  
     ~                   NOT, !
     ^                   XOR
     →                   ->, IMP
     ↔                   <->, BICON
     ⊼                   NAND
     ⊽                   NOR

PARENTHESES:
• Use ( and ) to group expressions
• Click parentheses buttons or type directly

INPUT FORMAT:
✓ Valid: A & B
✓ Valid: (A | B) → C
✓ Valid: ~A & (B | C)
✗ Invalid: A &  (missing operand)
✗ Invalid: & B  (missing left operand)

MODES:
• Automatic: System finds proofs automatically
• Manual: Select steps and apply rules yourself

BUTTONS:
• Execute Proof: Find/verify logical proof
• Generate Truth Table: Show all truth values
• Export: Save truth table to file
• Clear All: Reset everything

ERROR FEEDBACK:
• Red highlighting shows invalid characters
• Messages appear in notification area below
• Formula type displayed: Tautology/Contradiction/Contingent

NOTE: Click buttons to insert symbols. Advanced drag-and-drop
will be added in a future version."""

        # Insert the instruction text
        self.text_widget.config(state='normal')
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', instructions)
        self.text_widget.config(state='disabled')

        # Scroll to top
        self.text_widget.see('1.0')

    def update_instructions(self, mode="automatic"):
        """
        Update instructions based on current mode

        Parameters:
            mode (str): Current application mode ("automatic" or "manual")
        """
        # Add mode-specific instructions at the end
        mode_text = f"\n\nCURRENT MODE: {mode.upper()}\n"

        if mode == "automatic":
            mode_text += "• System will automatically find proofs\n"
            mode_text += "• Click 'Execute Proof' to start\n"
            mode_text += "• Results appear in Proof Steps panel"
        else:  # manual mode
            mode_text += "• Click proof steps to select them\n"
            mode_text += "• Choose inference rules manually\n"
            mode_text += "• Build proofs step by step"

        # Update the text widget
        self.text_widget.config(state='normal')

        # Remove any existing mode information (search for "CURRENT MODE:")
        content = self.text_widget.get('1.0', tk.END)
        if "CURRENT MODE:" in content:
            # Find the position of mode info and remove it
            lines = content.split('\n')
            new_lines = []
            skip_mode_section = False

            for line in lines:
                if line.startswith("CURRENT MODE:"):
                    skip_mode_section = True
                    break
                new_lines.append(line)

            # Update content without mode section
            self.text_widget.delete('1.0', tk.END)
            self.text_widget.insert('1.0', '\n'.join(new_lines))

        # Add new mode information
        self.text_widget.insert(tk.END, mode_text)
        self.text_widget.config(state='disabled')

        # Scroll to show the mode information
        self.text_widget.see(tk.END)