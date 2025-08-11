"""
Application view container that holds all UI components
This provides a clean interface for the controller
"""

import tkinter as tk


class AppView :
	"""
	Container for all view components
	This is what gets passed to the controller
	"""

	def __init__(self, main_window, panels) :
		"""
		Initialize with main window and all panels

		Parameters:
			main_window: MainWindow instance
			panels: dict containing all panel instances
		"""
		self.root = main_window.root
		self.main_window = main_window

		# Extract panels from dictionary
		self.premises_panel = panels['premises_panel']
		self.conclusions_panel = panels['conclusions_panel']
		self.proof_steps_panel = panels['proof_steps_panel']
		self.button_panel = panels['button_panel']
		self.truth_table_panel = panels['truth_table_panel']
		self.error_display = panels['error_display']
		self.menu_bar = panels['menu_bar']

	def get_focused_entry(self) :
		"""Get the currently focused entry widget"""
		focused = self.root.focus_get()
		if focused in [self.premises_panel.entry,
		               self.conclusions_panel.entry] :
			return focused
		return None

	def show_about_dialog(self) :
		"""Show about dialog"""
		from tkinter import messagebox
		messagebox.showinfo(
			"About GPLC",
			"Graphical Propositional Logic Calculator\n\n"
			"Version 1.0.0\n"
			"Created by Silviu Ciobanica-Mkrtchyan\n\n"
			"A tool for learning and applying propositional logic."
			)