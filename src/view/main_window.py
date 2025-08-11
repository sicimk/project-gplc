"""
Main application window for GPLC
Manages the overall layout with and coordinates all view components
"""

import tkinter as tk
from tkinter import ttk

class MainWindow :
	"""
	Main application window with proper 40-20-40 layout
	"""

	def __init__(self, root: tk.Tk | None = None) -> None :
		"""Initialize the main window with proper layout"""
		self.root: tk.Tk() = root or tk.Tk()
		self.root.title("Graphical Propositional Logic Calculator")

		# Set window size and position
		self.root.geometry("1200x800")
		self.root.minsize(1000, 700)

		# Center window on screen
		self._center_window()

		# Configure grid weights for proper resizing
		self.root.grid_rowconfigure(0, weight=0)  # Menu bar
		self.root.grid_rowconfigure(1, weight=30)  # Top section (30%)
		self.root.grid_rowconfigure(2, weight=20)  # Middle section (20%)
		self.root.grid_rowconfigure(3, weight=50)  # Bottom section (50%)
		self.root.grid_columnconfigure(0, weight=1)

		# Create all components
		self._create_menu_bar()
		self._create_top_section()
		self._create_middle_section()
		self._create_bottom_section()

		# Store references to panels (will be set by panel classes)
		self.premises_panel = None
		self.conclusions_panel = None
		self.proof_steps_panel = None
		self.button_panel = None
		self.truth_table_panel = None
		self.error_display = None
		self.menu_bar = None

	def _center_window(self) :
		"""Center the window on the screen"""
		self.root.update_idletasks()

		# Get screen dimensions
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()

		# Get window dimensions
		window_width = 1200
		window_height = 800

		# Calculate position
		x = (screen_width - window_width) // 2
		y = (screen_height - window_height) // 2

		self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

	def _create_menu_bar(self) :
		"""Create the menu bar with Options and Instructions"""
		# Create menu frame that looks like buttons
		menu_frame = tk.Frame(self.root, bg='#f0f0f0', height=30)
		menu_frame.grid(row=0, column=0, sticky='ew', padx=2, pady=2)
		menu_frame.grid_propagate(False)

		# Options button
		options_btn = tk.Button(menu_frame, text="Options", relief=tk.FLAT,
		                        bg='#e0e0e0', padx=15, pady=5)
		options_btn.pack(side=tk.LEFT, padx=5)

		# Instructions button
		instructions_btn = tk.Button(menu_frame, text="Instructions",
		                             relief=tk.FLAT,
		                             bg='#e0e0e0', padx=15, pady=5)
		instructions_btn.pack(side=tk.LEFT, padx=5)

		# Store menu reference
		self.menu_frame = menu_frame

	def _create_top_section(self) :
		"""Create the top section with 4 panels (20-20-20-40 ratio)"""
		top_frame = tk.Frame(self.root, bg='#ffffff')
		top_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

		# Configure column weights for 23-23-23-31 ratio
		top_frame.grid_columnconfigure(0, weight=23)  # Instructions
		top_frame.grid_columnconfigure(1, weight=23)  # Add Premises
		top_frame.grid_columnconfigure(2, weight=23)  # Add Conclusions
		top_frame.grid_columnconfigure(3, weight=31)  # View Proof Steps
		top_frame.grid_rowconfigure(0, weight=1)

		# 1. Instructions Panel
		instructions_frame = tk.LabelFrame(top_frame, text="Instructions",
		                                   font=('Arial', 10, 'bold'))
		instructions_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

		instructions_text = tk.Text(instructions_frame, wrap=tk.WORD,
		                            font=('Arial', 9), bg='#f8f8f8')
		instructions_text.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

		# Add sample instructions
		instructions_text.insert('1.0',
		                         "Formula Input Format:\n\n"
		                         "• Use capital letters A-Z for atomic propositions\n"
		                         "• Logical connectives:\n"
		                         "  - AND: ∧ or &\n"
		                         "  - OR: ∨ or |\n"
		                         "  - NOT: ¬ or ~\n"
		                         "  - IMPLIES: → or ->\n"
		                         "  - IFF: ↔ or <->\n"
		                         "  - XOR: ⊕\n"
		                         "  - NAND: ↑\n"
		                         "  - NOR: ↓\n\n"
		                         "• Use parentheses ( ) for grouping\n"
		                         "• Example: (A ∧ B) → C"
		                         )
		instructions_text.config(state=tk.DISABLED)

		# 2. Add Premises Panel
		premises_frame = tk.LabelFrame(top_frame, text="Add Premises",
		                               font=('Arial', 10, 'bold'))
		premises_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

		# Create numbered list for premises
		premises_list_frame = tk.Frame(premises_frame)
		premises_list_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
		premises_frame.grid_rowconfigure(0, weight=1)
		premises_frame.grid_columnconfigure(0, weight=1)

		# Premises listbox with numbers
		premises_listbox = tk.Listbox(premises_list_frame, font=('Arial', 10))
		premises_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		# Sample premises (will be populated dynamically)
		for i in range(1, 8) :
			premises_listbox.insert(tk.END, f"{i}")

		# Input section at bottom
		input_frame = tk.Frame(premises_frame)
		input_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

		add_button = tk.Button(input_frame, text="Add to list", bg='#4CAF50',
		                       fg='white', font=('Arial', 9))
		add_button.pack(fill=tk.X, pady=2)

		premise_entry = tk.Entry(input_frame, font=('Arial', 10))
		premise_entry.pack(fill=tk.X, pady=2)
		premise_entry.insert(0, "Type here")

		# Store references
		self.premises_listbox = premises_listbox
		self.premise_entry = premise_entry

		# 3. Add Conclusions Panel
		conclusions_frame = tk.LabelFrame(top_frame, text="Add Conclusion",
		                                  font=('Arial', 10, 'bold'))
		conclusions_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

		# Create numbered list for conclusions
		conclusions_list_frame = tk.Frame(conclusions_frame)
		conclusions_list_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
		conclusions_frame.grid_rowconfigure(0, weight=1)
		conclusions_frame.grid_columnconfigure(0, weight=1)

		# Conclusions listbox
		conclusions_listbox = tk.Listbox(conclusions_list_frame, font=('Arial', 10))
		conclusions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		# Sample conclusions
		for i in range(1, 8) :
			conclusions_listbox.insert(tk.END, f"{i}")

		# Input section
		conc_input_frame = tk.Frame(conclusions_frame)
		conc_input_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

		conc_add_button = tk.Button(conc_input_frame, text="Add to list",
		                            bg='#2196F3', fg='white', font=('Arial', 9))
		conc_add_button.pack(fill=tk.X, pady=2)

		conclusion_entry = tk.Entry(conc_input_frame, font=('Arial', 10))
		conclusion_entry.pack(fill=tk.X, pady=2)
		conclusion_entry.insert(0, "Type here")

		# Store references
		self.conclusions_listbox = conclusions_listbox
		self.conclusion_entry = conclusion_entry

		# 4. View Proof Steps Panel
		proof_frame = tk.LabelFrame(top_frame, text="View Proof Steps",
		                            font=('Arial', 10, 'bold'))
		proof_frame.grid(row=0, column=3, sticky='nsew', padx=5, pady=5)

		# Proof steps display
		proof_text = tk.Text(proof_frame, font=('Arial', 10), bg='#f8f8f8')
		proof_text.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
		proof_frame.grid_rowconfigure(0, weight=1)
		proof_frame.grid_columnconfigure(0, weight=1)

		# Result section at bottom
		result_frame = tk.Frame(proof_frame)
		result_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

		tk.Label(result_frame, text="Result:", font=('Arial', 10, 'bold')).pack(
			side=tk.LEFT, padx=5)

		result_label = tk.Label(result_frame, text="Conclusion is VALID / FALSE",
		                        font=('Arial', 10), fg='gray')
		result_label.pack(side=tk.LEFT, padx=5)

		# Store references
		self.proof_text = proof_text
		self.result_label = result_label

		# Store top frame reference
		self.top_frame = top_frame


	def _create_middle_section(self) :
		"""Create the middle section with buttons and controls"""
		middle_frame = tk.Frame(self.root, bg='#f0f0f0')
		middle_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)

		# Configure grid
		middle_frame.grid_columnconfigure(0, weight=1)  # Mode selection
		middle_frame.grid_columnconfigure(1, weight=3)  # Atomic propositions
		middle_frame.grid_columnconfigure(2, weight=2)  # Logical connectives
		middle_frame.grid_columnconfigure(3, weight=2)  # Action buttons

		# 1. Mode Selection (Automatic/Manual)
		mode_frame = tk.LabelFrame(middle_frame, text="Mode",
		                           font=('Arial', 9, 'bold'))
		mode_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

		self.mode_var = tk.StringVar(value="automatic")

		auto_radio = tk.Radiobutton(mode_frame, text="Automatic",
		                            variable=self.mode_var, value="automatic",
		                            font=('Arial', 9))
		auto_radio.pack(pady=5)

		manual_radio = tk.Radiobutton(mode_frame, text="Manual",
		                              variable=self.mode_var, value="manual",
		                              font=('Arial', 9))
		manual_radio.pack(pady=5)

		# 2. Atomic Propositions (A-Z)
		props_frame = tk.LabelFrame(middle_frame, text="Atomic Propositions",
		                            font=('Arial', 9, 'bold'))
		props_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

		# Create grid of letter buttons
		letters_frame = tk.Frame(props_frame)
		letters_frame.pack(pady=5)

		# Create A-Z buttons in rows
		for i in range(26) :
			row = i // 13
			col = i % 13
			letter = chr(65 + i)  # A-Z

			btn = tk.Button(letters_frame, text=letter, width=3, height=1,
			                font=('Arial', 10), relief=tk.RAISED)
			btn.grid(row=row, column=col, padx=2, pady=2)

		# 3. Logical Connectives
		connectives_frame = tk.LabelFrame(middle_frame, text="Logical Connectives",
		                                  font=('Arial', 9, 'bold'))
		connectives_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

		# Connectives with their symbols
		connectives = [
			("(", "("), (")", ")"),
			("NOT", "¬"), ("AND", "∧"), ("OR", "∨"),
			("XOR", "⊕"), ("Imp", "→"), ("Bico", "↔"),
			("NAND", "↑"), ("NOR", "↓")
			]

		conn_buttons_frame = tk.Frame(connectives_frame)
		conn_buttons_frame.pack(pady=5)

		for i, (name, symbol) in enumerate(connectives) :
			row = i // 5
			col = i % 5

			btn = tk.Button(conn_buttons_frame, text=symbol, width=4, height=1,
			                font=('Arial', 12), relief=tk.RAISED)
			btn.grid(row=row, column=col, padx=2, pady=2)

		# 4. Action Buttons
		actions_frame = tk.Frame(middle_frame)
		actions_frame.grid(row=0, column=3, sticky='nsew', padx=5, pady=5)

		# Create action buttons
		execute_btn = tk.Button(actions_frame, text="EXECUTE PROOF",
		                        bg='#4CAF50', fg='white',
		                        font=('Arial', 10, 'bold'),
		                        height=2)
		execute_btn.pack(fill=tk.X, pady=5)

		generate_btn = tk.Button(actions_frame, text="Generate Truth Table",
		                         bg='#2196F3', fg='white',
		                         font=('Arial', 10, 'bold'),
		                         height=2)
		generate_btn.pack(fill=tk.X, pady=5)

		export_btn = tk.Button(actions_frame, text="Export truth table to\nfile",
		                       bg='#9C27B0', fg='white', font=('Arial', 9),
		                       height=2)
		export_btn.pack(fill=tk.X, pady=5)

		clear_btn = tk.Button(actions_frame, text="CLEAR ALL",
		                      bg='#f44336', fg='white', font=('Arial', 10, 'bold'),
		                      height=2)
		clear_btn.pack(fill=tk.X, pady=5)

		# Store middle frame reference
		self.middle_frame = middle_frame


	def _create_bottom_section(self) :
		"""Create the bottom section for truth table display"""
		bottom_frame = tk.LabelFrame(self.root, text="Truth Table",
		                             font=('Arial', 10, 'bold'))
		bottom_frame.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)

		# Create scrollable table using Treeview
		table_frame = tk.Frame(bottom_frame)
		table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		# Create Treeview for truth table
		self.truth_table = ttk.Treeview(table_frame, show='headings')

		# Create scrollbars
		v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL,
		                         command=self.truth_table.yview)
		h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL,
		                         command=self.truth_table.xview)

		self.truth_table.configure(yscrollcommand=v_scroll.set,
		                           xscrollcommand=h_scroll.set)

		# Grid layout
		self.truth_table.grid(row=0, column=0, sticky='nsew')
		v_scroll.grid(row=0, column=1, sticky='ns')
		h_scroll.grid(row=1, column=0, sticky='ew')

		table_frame.grid_rowconfigure(0, weight=1)
		table_frame.grid_columnconfigure(0, weight=1)

		# Configure table style
		style = ttk.Style()
		style.configure("Treeview", font=('Arial', 10))
		style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

		# Store bottom frame reference
		self.bottom_frame = bottom_frame


	def show(self) :
		"""Display the main window"""
		self.root.mainloop()


	def get_root(self) :
		"""Get the root window"""
		return self.root

# Test the window
if __name__ == "__main__" :
	window = MainWindow()
	window.show()