# src/view/view_interface.py
"""
Interface definition for the view components
This helps with type checking and IDE support
"""

from typing import Protocol
import tkinter as tk

from view import (
	MainWindow,
	PremisesPanel,
	ConclusionsPanel,
	ProofStepsPanel,
	ButtonPanel,
	TruthTablePanel,
	ErrorDisplay,
	MenuBar
	)


class IView(Protocol) :
	"""Interface for the main view wrapper"""

	# Root window
	root: 'tk.Tk'

	# Main window
	main_window: 'MainWindow'

	# Panels
	premises_panel: 'PremisesPanel'
	conclusions_panel: 'ConclusionsPanel'
	proof_steps_panel: 'ProofStepsPanel'
	button_panel: 'ButtonPanel'
	truth_table_panel: 'TruthTablePanel'
	error_display: 'ErrorDisplay'
	menu_bar: 'MenuBar'


# Alternative: Create a concrete ViewWrapper class
class ViewWrapper :
	"""
	Wrapper class that contains all view components
	This is what gets passed to the controller
	"""

	def __init__(self, main_window) :
		"""Initialize with the main window and all its panels"""
		self.root = main_window.root
		self.main_window = main_window

		# These will be set after panel creation
		self.premises_panel = None
		self.conclusions_panel = None
		self.proof_steps_panel = None
		self.button_panel = None
		self.truth_table_panel = None
		self.error_display = None
		self.menu_bar = None