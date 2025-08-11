"""
Formula representation and manipulation
Handles the internal representation of logical formulas
"""

import re
from copy import deepcopy
from typing import Dict, Set, Optional, Union, Tuple

class Formula :
	"""
	Represents a propositional logic formula using an Abstract Syntax Tree (AST)
	"""

	def __init__(self, expression_string: str)  -> None:
		"""
		Initialize a formula from a string expression

		Parameters:
			expression_string (str): The formula as entered by user
		"""
		#Trim leading / trailing white space
		self.original_string = expression_string.strip()

		#---------- new test guard ----------
		if not self.original_string :
			raise ValueError("Formula cannot be empty or whitespace-only")
		#------------------------------------

		self.ast = None  # Abstract Syntax Tree representation
		self.atomic_propositions: set[str] = set()  # Set of atomic propositions

		# Parse the expression into AST
		if self.original_string :
			self.ast = self._parse(self.original_string)
			self._collect_atomic_propositions(self.ast)

	def _tokenize(self, expression) :
		"""
		Convert expression string into list of tokens

		Parameters:
			expression (str): Formula string to tokenize

		Returns:
			list: List of tokens
		"""
		tokens = []
		i = 0

		while i < len(expression) :
			char = expression[i]

			# Skip whitespace
			if char.isspace() :
				i += 1
				continue

			# Check for atomic propositions (A-Z)
			if char.isupper() and char.isalpha() :
				tokens.append(('PROP', char))

			# Check for operators
			elif char == '∧' or char == '&' :
				tokens.append(('AND', '∧'))
			elif char == '∨' or char == '|' :
				tokens.append(('OR', '∨'))
			elif char == '¬' or char == '~' :
				tokens.append(('NOT', '¬'))
			elif char == '→' :
				tokens.append(('IMPLIES', '→'))
			elif char == '↔' :
				tokens.append(('IFF', '↔'))
			elif char == '⊕' or char == '^' :
				tokens.append(('XOR', '⊕'))
			elif char == '↑' :
				tokens.append(('NAND', '↑'))
			elif char == '↓' :
				tokens.append(('NOR', '↓'))

			# Check for arrow operator (->)
			elif char == '-' and i + 1 < len(expression) and expression[
				i + 1] == '>' :
				tokens.append(('IMPLIES', '→'))
				i += 1  # Skip the '>'

			# Check for biconditional operator (<->)
			elif char == '<' and i + 2 < len(expression) and expression[
			                                                 i + 1 :i + 3] == '->' :
				tokens.append(('IFF', '↔'))
				i += 2  # Skip the '->'

			# Parentheses
			elif char == '(' :
				tokens.append(('LPAREN', '('))
			elif char == ')' :
				tokens.append(('RPAREN', ')'))

			# Invalid character
			else :
				raise ValueError(f"Invalid character '{char}' at position {i}")

			i += 1

		return tokens

	def _parse(self, expression) :
		"""
		Parse expression into Abstract Syntax Tree using recursive descent

		Parameters:
			expression (str): Formula string to parse

		Returns:
			dict: AST representation
		"""
		tokens = self._tokenize(expression)
		if not tokens :
			raise ValueError("Empty expression")

		# Use recursive descent parser
		result, pos = self._parse_iff(tokens, 0)

		# Check if we consumed all tokens
		if pos < len(tokens) :
			raise ValueError(
				f"Unexpected token at position {pos}: {tokens[pos]}")

		return result

	def _parse_iff(self, tokens, pos) :
		"""Parse biconditional (lowest precedence)"""
		left, pos = self._parse_implies(tokens, pos)

		while pos < len(tokens) and tokens[pos][0] == 'IFF' :
			op = tokens[pos][1]
			pos += 1
			right, pos = self._parse_implies(tokens, pos)
			left = {'type' : 'IFF', 'operator' : op, 'left' : left,
			        'right' : right}

		return left, pos

	def _parse_implies(self, tokens, pos) :
		"""Parse implication (right associative)"""
		left, pos = self._parse_or(tokens, pos)

		if pos < len(tokens) and tokens[pos][0] == 'IMPLIES' :
			op = tokens[pos][1]
			pos += 1
			right, pos = self._parse_implies(tokens, pos)  # Right associative
			left = {'type' : 'IMPLIES', 'operator' : op, 'left' : left,
			        'right' : right}

		return left, pos

	def _parse_or(self, tokens, pos) :
		"""Parse disjunction"""
		left, pos = self._parse_xor(tokens, pos)

		while pos < len(tokens) and tokens[pos][0] in ['OR', 'NOR'] :
			op_type = tokens[pos][0]
			op = tokens[pos][1]
			pos += 1
			right, pos = self._parse_xor(tokens, pos)
			left = {'type' : op_type, 'operator' : op, 'left' : left,
			        'right' : right}

		return left, pos

	def _parse_xor(self, tokens, pos) :
		"""Parse exclusive or"""
		left, pos = self._parse_and(tokens, pos)

		while pos < len(tokens) and tokens[pos][0] == 'XOR' :
			op = tokens[pos][1]
			pos += 1
			right, pos = self._parse_and(tokens, pos)
			left = {'type' : 'XOR', 'operator' : op, 'left' : left,
			        'right' : right}

		return left, pos

	def _parse_and(self, tokens, pos) :
		"""Parse conjunction"""
		left, pos = self._parse_not(tokens, pos)

		while pos < len(tokens) and tokens[pos][0] in ['AND', 'NAND'] :
			op_type = tokens[pos][0]
			op = tokens[pos][1]
			pos += 1
			right, pos = self._parse_not(tokens, pos)
			left = {'type' : op_type, 'operator' : op, 'left' : left,
			        'right' : right}

		return left, pos

	def _parse_not(self, tokens, pos) :
		"""Parse negation (highest precedence)"""
		if pos < len(tokens) and tokens[pos][0] == 'NOT' :
			op = tokens[pos][1]
			pos += 1
			operand, pos = self._parse_not(tokens,
			                               pos)  # Allow multiple negations
			return {'type' : 'NOT', 'operator' : op, 'operand' : operand}, pos

		return self._parse_atom(tokens, pos)

	def _parse_atom(self, tokens, pos) :
		"""Parse atomic proposition or parenthesized expression"""
		if pos >= len(tokens) :
			raise ValueError("Unexpected end of expression")

		token_type, token_value = tokens[pos]

		# Atomic proposition
		if token_type == 'PROP' :
			pos += 1
			return {'type' : 'PROP', 'value' : token_value}, pos

		# Parenthesized expression
		elif token_type == 'LPAREN' :
			pos += 1
			result, pos = self._parse_iff(tokens, pos)
			if pos >= len(tokens) or tokens[pos][0] != 'RPAREN' :
				raise ValueError("Missing closing parenthesis")
			pos += 1
			return result, pos

		else :
			raise ValueError(f"Unexpected token: {token_value}")

	def _collect_atomic_propositions(self, node) :
		"""
		Recursively collect all atomic propositions from AST

		Parameters:
			node (dict): AST node
		"""
		if node['type'] == 'PROP' :
			self.atomic_propositions.add(node['value'])
		elif node['type'] == 'NOT' :
			self._collect_atomic_propositions(node['operand'])
		elif node['type'] in ['AND', 'OR', 'IMPLIES', 'IFF', 'XOR', 'NAND',
		                      'NOR'] :
			self._collect_atomic_propositions(node['left'])
			self._collect_atomic_propositions(node['right'])

	def evaluate(self, truth_values) :
		"""
		Evaluate formula given truth values for atomic propositions

		Parameters:
			truth_values (dict): Mapping of propositions to True/False

		Returns:
			bool: Truth value of the formula
		"""
		if not self.ast :
			raise ValueError("No formula to evaluate")

		# Check that all atomic propositions have values
		for prop in self.atomic_propositions :
			if prop not in truth_values :
				raise ValueError(
					f"No truth value provided for proposition {prop}")

		return self._evaluate_node(self.ast, truth_values)

	def _evaluate_node(self, node, truth_values) :
		"""
		Recursively evaluate an AST node

		Parameters:
			node (dict): AST node to evaluate
			truth_values (dict): Truth value assignments

		Returns:
			bool: Truth value of the node
		"""
		node_type = node['type']

		# Base case: atomic proposition
		if node_type == 'PROP' :
			return truth_values[node['value']]

		# Negation
		elif node_type == 'NOT' :
			return not self._evaluate_node(node['operand'], truth_values)

		# Binary operators
		else :
			left_val = self._evaluate_node(node['left'], truth_values)
			right_val = self._evaluate_node(node['right'], truth_values)

			if node_type == 'AND' :
				return left_val and right_val
			elif node_type == 'OR' :
				return left_val or right_val
			elif node_type == 'IMPLIES' :
				return (not left_val) or right_val
			elif node_type == 'IFF' :
				return left_val == right_val
			elif node_type == 'XOR' :
				return left_val != right_val
			elif node_type == 'NAND' :
				return not (left_val and right_val)
			elif node_type == 'NOR' :
				return not (left_val or right_val)

	def get_atomic_propositions(self) :
		"""
		Get all atomic propositions in the formula

		Returns:
			set: Set of atomic proposition letters (A-Z)
		"""
		return self.atomic_propositions.copy()

	def to_string(self, node=None) :
		"""
		Convert formula back to string representation

		Parameters:
			node (dict): AST node (uses self.ast if None)

		Returns:
			str: String representation of the formula
		"""
		if node is None :
			if not self.ast :
				return ""
			node = self.ast

		node_type = node['type']

		# Atomic proposition
		if node_type == 'PROP' :
			return node['value']

		# Negation
		elif node_type == 'NOT' :
			operand_str = self.to_string(node['operand'])
			# Add parentheses if operand is complex
			if node['operand']['type'] not in ['PROP', 'NOT'] :
				operand_str = f"({operand_str})"
			return f"{node['operator']}{operand_str}"

		# Binary operators
		else :
			left_str = self.to_string(node['left'])
			right_str = self.to_string(node['right'])

			# Add parentheses based on precedence
			if self._needs_parentheses(node['left'], node_type, True) :
				left_str = f"({left_str})"
			if self._needs_parentheses(node['right'], node_type, False) :
				right_str = f"({right_str})"

			return f"{left_str} {node['operator']} {right_str}"

	def _needs_parentheses(self, child_node, parent_type, is_left) :
		"""
		Determine if parentheses are needed based on operator precedence

		Parameters:
			child_node (dict): Child node in AST
			parent_type (str): Parent operator type
			is_left (bool): Whether child is left operand

		Returns:
			bool: True if parentheses are needed
		"""
		if child_node['type'] in ['PROP', 'NOT'] :
			return False

		# Operator precedence (higher number = higher precedence)
		precedence = {
			'IFF' : 1,
			'IMPLIES' : 2,
			'OR' : 3,
			'NOR' : 3,
			'XOR' : 4,
			'AND' : 5,
			'NAND' : 5,
			}

		child_prec = precedence.get(child_node['type'], 0)
		parent_prec = precedence.get(parent_type, 0)

		# always parenthesise a non-atomic child of IMPLIES / IFF
		if parent_type in ('IMPLIES', 'IFF') and child_node['type'] not in (
		'PROP', 'NOT') :
			return True

		# Need parentheses if child has lower precedence
		if child_prec < parent_prec :
			return True

		# For right-associative operators (IMPLIES), need parentheses on left
		if parent_type == 'IMPLIES' and is_left and child_prec == parent_prec :
			return True

		return False

	def get_subformulas(self) :
		"""
		Get all subformulas of this formula

		Returns:
			list: List of all subformulas as Formula objects
		"""
		if not self.ast :
			return []

		subformulas = []
		self._collect_subformulas(self.ast, subformulas)

		# Convert AST nodes back to Formula objects
		result = []
		for node in subformulas :
			sub_str = self.to_string(node)
			result.append(Formula(sub_str))

		return result

	def _collect_subformulas(self, node, subformulas) :
		"""
		Recursively collect all subformulas from AST

		Parameters:
			node (dict): Current AST node
			subformulas (list): List to collect subformulas into
		"""
		# Add current node as subformula
		subformulas.append(node)

		# Recurse based on node type
		if node['type'] == 'NOT' :
			self._collect_subformulas(node['operand'], subformulas)
		elif node['type'] in ['AND', 'OR', 'IMPLIES', 'IFF', 'XOR', 'NAND',
		                      'NOR'] :
			self._collect_subformulas(node['left'], subformulas)
			self._collect_subformulas(node['right'], subformulas)

	def __str__(self) -> str:
		"""String representation of the formula

		• If this Formula was built from a user-supplied expression,
          just echo that text so we preserve any explicit parentheses.
        • Otherwise (e.g. for sub-formulas created from the AST) fall back
          to the precedence-aware pretty-printer.
		"""
		if getattr(self, "original_string", "") :
			s = self.original_string

			# canonicalise ASCII operators
			s = re.sub(r'\s*<->\s*', ' ↔ ', s)
			s = re.sub(r'\s*->\s*', ' → ', s)
			s = s.replace('&', '∧').replace('|',
			                        '∨').replace('^', '⊕')

			# collapse multiple spaces introduced by the substitutions
			s = re.sub(r'\s+', ' ', s).strip()
			return s

		return self.to_string(self.ast)

	def __repr__(self) :
		"""Detailed representation for debugging"""
		return f"Formula('{self.original_string}')"

	def __eq__(self, other) :
		"""Check if two formulas are structurally equal"""
		if not isinstance(other, Formula) :
			return False
		return self._ast_equal(self.ast, other.ast)

	def _ast_equal(self, node1, node2) :
		"""Check if two AST nodes are equal"""
		if node1 is None and node2 is None :
			return True
		if node1 is None or node2 is None :
			return False

		if node1['type'] != node2['type'] :
			return False

		if node1['type'] == 'PROP' :
			return node1['value'] == node2['value']
		elif node1['type'] == 'NOT' :
			return self._ast_equal(node1['operand'], node2['operand'])
		else :
			return (self._ast_equal(node1['left'], node2['left']) and
			        self._ast_equal(node1['right'], node2['right']))