"""
Fixed main entry point for GPLC application with manual proof support
Fixes recursion and threading issues
"""

import sys
import os
import tkinter as tk
import traceback

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import all modules after setting the path
from view.main_window import MainWindow
from view.app_view import AppView
from controller.main_controller import MainController

# Import all panel classes
from view.premises_panel import PremisesPanel
from view.conclusions_panel import ConclusionsPanel
from view.proof_steps_panel import ProofStepsPanel
from view.button_panel import ButtonPanel
from view.truth_table_panel import TruthTablePanel
from view.error_display import ErrorDisplay
from view.menu_bar import MenuBar


def create_view_wrapper(main_window) :
	"""Create a view wrapper containing all UI panels"""
	# Create all panels
	premises_panel = PremisesPanel(main_window)
	conclusions_panel = ConclusionsPanel(main_window)
	proof_steps_panel = ProofStepsPanel(main_window)
	button_panel = ButtonPanel(main_window)
	truth_table_panel = TruthTablePanel(main_window)
	error_display = ErrorDisplay(main_window)
	menu_bar = MenuBar(main_window)

	# Setup panels after UI is created
	premises_panel.setup()
	conclusions_panel.setup()
	proof_steps_panel.setup()
	button_panel.setup()
	truth_table_panel.setup()
	error_display.setup()
	menu_bar.setup()

	# Create panels dictionary
	panels = {
		'premises_panel' : premises_panel,
		'conclusions_panel' : conclusions_panel,
		'proof_steps_panel' : proof_steps_panel,
		'button_panel' : button_panel,
		'truth_table_panel' : truth_table_panel,
		'error_display' : error_display,
		'menu_bar' : menu_bar
		}

	# Create and return app view
	return AppView(main_window, panels)


def connect_manual_proof_buttons(main_window, main_controller) :
	"""Connect manual proof specific buttons to their handlers"""

	# Connect Send to Proof Panel button - FIX: Use correct handler method
	if hasattr(main_window,
	           'send_to_proof_btn') and main_window.send_to_proof_btn :
		main_window.send_to_proof_btn.config(
			command=main_controller.handle_send_to_proof_panel
			# This is correct
			)
		print("Connected Send to Proof Panel button")

	# Connect Apply Rule button
	if hasattr(main_window, 'apply_rule_btn') and main_window.apply_rule_btn :
		main_window.apply_rule_btn.config(
			command=main_controller.handle_apply_rule
			)
		print("Connected Apply Rule button")

	# Connect rule buttons to rule selection (not direct application)
	if hasattr(main_window, 'rule_buttons') and main_window.rule_buttons :
		print(
			f"Connecting {len(main_window.rule_buttons)} rule buttons to selection handler")
		for rule_abbrev, button in main_window.rule_buttons.items() :
			# Rule buttons now select the rule, Apply Rule button applies it
			button.config(command=lambda
				r=rule_abbrev : main_controller.handle_rule_selection(r))


def setup_fixed_mode_handlers(main_controller) :
	"""Setup handlers for manual mode interactions without recursion"""

	# Set up proof step click handling
	if hasattr(main_controller,
	           'proof_controller') and main_controller.proof_controller :
		print("Manual mode step selection handlers configured")

	# Store trace ID in a container so it can be modified within the nested function
	trace_container = {'trace_id' : None}

	# Create a non-recursive mode change handler
	def safe_mode_change_handler(*args) :
		"""Safe mode change handler that prevents recursion"""
		try :
			# Get the mode directly from the variable
			main_window = main_controller.view.main_window
			mode = main_window.mode_var.get()

			print(f"Mode changing to: {mode}")

			# Only call the main controller's mode change if it's different from current
			if main_controller.current_mode != mode :
				# Temporarily disable the trace to prevent recursion
				if trace_container['trace_id'] :
					main_window.mode_var.trace_vdelete('w', trace_container[
						'trace_id'])

				# Update the controller state
				main_controller.current_mode = mode
				main_controller.proof_controller.set_mode(mode)

				# Update UI controls based on mode
				if mode == "manual" :
					# Enable manual mode controls
					if hasattr(main_window, 'enable_manual_mode_controls') :
						main_window.enable_manual_mode_controls()
					if hasattr(main_window, 'enable_rule_buttons') :
						main_window.enable_rule_buttons()
					if hasattr(main_window, 'show_mode_info') :
						main_window.show_mode_info("manual")

					# Clear any existing derived steps for manual mode
					if hasattr(main_controller.proof_system,
					           'reset_for_manual_mode') :
						main_controller.proof_system.reset_for_manual_mode()
						main_controller.proof_controller.refresh_display()

					main_controller.error_controller.show_info(
						"Manual Mode: Use 'Send to Proof Panel' then build proof step by step"
						)
				else :
					# Disable manual mode controls
					if hasattr(main_window, 'disable_manual_mode_controls') :
						main_window.disable_manual_mode_controls()
					if hasattr(main_window, 'disable_rule_buttons') :
						main_window.disable_rule_buttons()
					if hasattr(main_window, 'show_mode_info') :
						main_window.show_mode_info("automatic")

					# Reset manual mode state
					if hasattr(main_controller,
					           'button_controller') and hasattr(
							main_controller.button_controller,
							'reset_manual_state') :
						main_controller.button_controller.reset_manual_state()

					main_controller.error_controller.show_info(
						"Automatic Mode: System will find proofs automatically"
						)

				# Re-enable the trace
				trace_container['trace_id'] = main_window.mode_var.trace('w',
				                                                         safe_mode_change_handler)

		except Exception as e :
			print(f"Error in safe mode change handler: {e}")
			import traceback
			traceback.print_exc()

	# Set up the safe mode change handler
	main_window = main_controller.view.main_window
	if hasattr(main_window, 'mode_var') and main_window.mode_var :
		# Store the trace ID in the container
		trace_container['trace_id'] = main_window.mode_var.trace('w',
		                                                         safe_mode_change_handler)
		print("Safe mode change handler configured")


def handle_apply_rule(self) :
	"""Handle Apply Rule button click (manual mode only)"""
	print(f"DEBUG: Apply Rule clicked in {self.current_mode} mode")

	if self.current_mode != "manual" :
		self.error_controller.show_error("mode",
		                                 "Apply Rule only available in Manual mode")
		return

	try :
		success, msg = self.proof_controller.apply_selected_rule()
		if success :
			self.error_controller.show_info(f"Rule applied: {msg}")
		else :
			self.error_controller.show_error("rule",
			                                 f"Cannot apply rule: {msg}")
	except Exception as e :
		self.error_controller.show_error("rule",
		                                 f"Error applying rule: {str(e)}")


def main() :
	"""Main application entry point with manual proof support and fixed recursion"""
	try :
		# Create root window
		root = tk.Tk()

		# Create main window
		main_window = MainWindow(root)

		# Create view wrapper with all panels
		view = create_view_wrapper(main_window)

		# Initialize main controller
		main_controller = MainController()

		# Set view BEFORE starting application
		main_controller.set_view(view)

		# Connect standard buttons to controller
		main_window.connect_button_controller(main_controller.button_controller)

		# Connect manual proof specific buttons
		connect_manual_proof_buttons(main_window, main_controller)

		# Setup FIXED manual mode handlers (no recursion)
		setup_fixed_mode_handlers(main_controller)

		# Initialize with automatic mode (without triggering recursion)
		main_controller.current_mode = "automatic"
		main_controller.proof_controller.set_mode("automatic")

		# Set UI to automatic mode
		if hasattr(main_window, 'disable_manual_mode_controls') :
			main_window.disable_manual_mode_controls()
		if hasattr(main_window, 'disable_rule_buttons') :
			main_window.disable_rule_buttons()

		# Start the application
		main_controller.start_application()

		# Print status for debugging
		print("GPLC Application Started Successfully")
		print(f"Mode: {main_controller.current_mode}")
		print("Manual proof functionality enabled")

		# Start the GUI main loop
		root.mainloop()

	except Exception as e :
		print(f"Application error: {e}")
		traceback.print_exc()

		# Show error dialog if possible
		try :
			from tkinter import messagebox
			messagebox.showerror("GPLC Error",
			                     f"Application failed to start:\n\n{str(e)}\n\nSee console for details.")
		except :
			pass


if __name__ == "__main__" :
	main()