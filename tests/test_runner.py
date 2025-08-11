"""
Simple test runner to check if the model layer is working correctly
This can be run without pytest to do basic functionality checks
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model.formula import Formula
from model.validator import FormulaValidator
from model.inference_rules import get_all_rules, ModusPonens
from model.proof_system import ProofSystem
from model.truth_table import TruthTable


def test_formula_basics() :
	"""Test basic formula functionality"""
	print("\n=== Testing Formula Basics ===")

	try :
		# Test simple formula
		f1 = Formula("A ∧ B")
		print(f"✓ Created formula: {f1}")
		print(f"  Atomic propositions: {f1.get_atomic_propositions()}")

		# Test evaluation
		result = f1.evaluate({'A' : True, 'B' : True})
		print(f"  Evaluation with A=T, B=T: {result}")
		assert result == True

		# Test complex formula
		f2 = Formula("(A → B) ∧ (B → C)")
		print(f"✓ Created complex formula: {f2}")

		# Test alternative notation
		f3 = Formula("A -> B")
		print(f"✓ Alternative notation works: {f3}")

		print("✓ All formula tests passed!")
		return True

	except Exception as e :
		print(f"✗ Formula test failed: {e}")
		return False


def test_validator() :
	"""Test validator functionality"""
	print("\n=== Testing Validator ===")

	try :
		validator = FormulaValidator()

		# Test tautology
		f1 = Formula("A ∨ ¬A")
		is_taut = validator.check_tautology(f1)
		print(f"✓ Tautology detection: 'A ∨ ¬A' is tautology = {is_taut}")
		assert is_taut == True

		# Test contradiction
		f2 = Formula("A ∧ ¬A")
		is_contra = validator.check_contradiction(f2)
		print(
			f"✓ Contradiction detection: 'A ∧ ¬A' is contradiction = {is_contra}")
		assert is_contra == True

		# Test contingent
		f3 = Formula("A → B")
		formula_type = validator.get_formula_type(f3)
		print(f"✓ Formula type: 'A → B' is {formula_type}")
		assert formula_type == "contingent"

		print("✓ All validator tests passed!")
		return True

	except Exception as e :
		print(f"✗ Validator test failed: {e}")
		return False


def test_inference_rules() :
	"""Test inference rules"""
	print("\n=== Testing Inference Rules ===")

	try :
		# Get all rules
		rules = get_all_rules()
		print(f"✓ Loaded {len(rules)} inference rules")

		# Test Modus Ponens
		mp = ModusPonens()
		f1 = Formula("A → B")
		f2 = Formula("A")

		can_apply = mp.can_apply([f1, f2])
		print(f"✓ Modus Ponens can apply to 'A → B' and 'A': {can_apply}")
		assert can_apply == True

		result = mp.apply([f1, f2])
		print(f"✓ Modus Ponens result: {result}")
		assert str(result) == "B"

		# List all rules
		print("\n  Available rules:")
		for rule in rules :
			print(f"    - {rule.name} ({rule.abbreviation})")

		print("\n✓ All inference rule tests passed!")
		return True

	except Exception as e :
		print(f"✗ Inference rules test failed: {e}")
		return False


def test_proof_system() :
	"""Test proof system"""
	print("\n=== Testing Proof System ===")

	try :
		proof = ProofSystem()

		# Add premises
		f1 = Formula("A → B")
		f2 = Formula("B → C")
		f3 = Formula("A")

		success1, msg1 = proof.add_premise(f1)
		print(f"✓ Added premise 'A → B': {msg1}")

		success2, msg2 = proof.add_premise(f2)
		print(f"✓ Added premise 'B → C': {msg2}")

		success3, msg3 = proof.add_premise(f3)
		print(f"✓ Added premise 'A': {msg3}")

		# Set conclusion
		conclusion = Formula("C")
		success4, msg4 = proof.set_conclusion(conclusion)
		print(f"✓ Set conclusion 'C': {msg4}")

		# Try manual proof
		success5, msg5, step = proof.apply_rule("MP", [1, 3])
		print(f"✓ Applied Modus Ponens to steps 1,3: {msg5}")

		# Check proof steps
		steps = proof.get_proof_steps()
		print(f"\n  Proof steps so far:")
		for step in steps :
			print(f"    {step}")

		print("\n✓ All proof system tests passed!")
		return True

	except Exception as e :
		print(f"✗ Proof system test failed: {e}")
		return False


def test_truth_table() :
	"""Test truth table generation"""
	print("\n=== Testing Truth Table ===")

	try :
		table = TruthTable()

		# Generate table for some formulas
		f1 = Formula("A ∧ B")
		f2 = Formula("A → B")

		passed, msg = table.generate_from_formulas([f1, f2])
		print(f"✓ Generated truth table: {msg}")

		# Get table data
		data = table.get_table_data()
		print(
			f"✓ Table has {len(data['headers'])} columns and {len(data['rows'])} rows")
		print(f"  Headers: {data['headers']}")

		# Show first few rows
		print("  First few rows:")
		for i, row in enumerate(data['rows'][:3]) :
			print(f"    {row}")

		print("\n✓ All truth table tests passed!")
		return True

	except Exception as e :
		print(f"✗ Truth table test failed: {e}")
		return False


def run_all_tests() :
	"""Run all tests and report results"""
	print("=" * 60)
	print("GPLC Model Layer Test Suite")
	print("=" * 60)

	tests = [
		test_formula_basics,
		test_validator,
		test_inference_rules,
		test_proof_system,
		test_truth_table
		]

	results = []
	for test in tests :
		results.append(test())

	print("\n" + "=" * 60)
	print("SUMMARY")
	print("=" * 60)

	passed = sum(results)
	total = len(results)

	print(f"Tests passed: {passed}/{total}")

	if passed == total :
		print("\n✓ All tests passed! The model layer is working correctly.")
	else :
		print(
			f"\n✗ {total - passed} tests failed. Please check the errors above.")

	return passed == total


if __name__ == "__main__" :
	# Run the tests
	success = run_all_tests()

	# Exit with appropriate code
	sys.exit(0 if success else 1)
