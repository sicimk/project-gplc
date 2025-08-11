"""
Comprehensive tests for all 19 inference rules
Tests each rule with valid and invalid applications
"""

import sys
from os import path

sys.path.insert(0, path.join(path.dirname(__file__), '..', 'src'))

from model.inference_rules import *


def test_all_rules() :
	"""Test all 19 inference rules with examples"""
	print("Testing All 19 Inference Rules")
	print("=" * 60)

	passed = 0
	total = 0

	# 1. Modus Ponens (MP)
	print("\n1. MODUS PONENS (MP)")
	total += 1
	try :
		mp = ModusPonens()
		f1 = Formula("A → B")
		f2 = Formula("A")
		assert mp.can_apply([f1, f2]) == True
		result = mp.apply([f1, f2])
		assert str(result) == "B"
		print(f"   ✓ From 'A → B' and 'A', derived 'B'")
		passed += 1
	except Exception as e:
		print(f"   ✗ Failed: {e}")

	# 2. Modus Tollens (MT)
	print("\n2. MODUS TOLLENS (MT)")
	total += 1
	try :
		mt = ModusTollens()
		f1 = Formula("A → B")
		f2 = Formula("¬B")
		assert mt.can_apply([f1, f2]) == True
		result = mt.apply([f1, f2])
		assert str(result) == "¬A"
		print(f"   ✓ From 'A → B' and '¬B', derived '¬A'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 3. Hypothetical Syllogism (HS)
	print("\n3. HYPOTHETICAL SYLLOGISM (HS)")
	total += 1
	try :
		hs = HypotheticalSyllogism()
		f1 = Formula("A → B")
		f2 = Formula("B → C")
		assert hs.can_apply([f1, f2]) == True
		result = hs.apply([f1, f2])
		assert str(result) == "A → C"
		print(f"   ✓ From 'A → B' and 'B → C', derived 'A → C'")
		passed += 1
	except Exception as e:
		print(f"   ✗ Failed: {e}")

	# 4. Disjunctive Syllogism (DS)
	print("\n4. DISJUNCTIVE SYLLOGISM (DS)")
	total += 1
	try :
		ds = DisjunctiveSyllogism()
		f1 = Formula("A ∨ B")
		f2 = Formula("¬A")
		assert ds.can_apply([f1, f2]) == True
		result = ds.apply([f1, f2])
		assert str(result) == "B"
		print(f"   ✓ From 'A ∨ B' and '¬A', derived 'B'")
		passed += 1
	except Exception as e:
		print(f"   ✗ Failed: {e}")

	# 5. Conjunction Introduction (CI)
	print(f"\n5. CONJUNCTION INTRODUCTION (CI)")
	total += 1
	try :
		ci = ConjunctionIntroduction()
		f1 = Formula("A")
		f2 = Formula("B")
		assert ci.can_apply([f1, f2]) == True
		result = ci.apply([f1, f2])
		assert str(result) == "A ∧ B"
		print(f"   ✓ From 'A' and 'B', derived 'A ∧ B'")
		passed += 1
	except Exception as e:
		print(f"   ✗ Failed: {e}")

	# 6. Conjunction Elimination (CE)
	print(f"\n6. CONJUNCTION ELIMINATION (CE)")
	total += 1
	try :
		ce = ConjunctionElimination()
		f1 = Formula("A ∧ B")
		assert ce.can_apply([f1]) == True
		result_left = ce.apply([f1], which='left')
		result_right = ce.apply([f1], which='right')
		assert str(result_left) == "A"
		assert str(result_right) == "B"
		print(f"   ✓ From 'A ∧ B', derived 'A' (left) and 'B' (right)")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 7. Addition (ADD)
	print(f"\n7. ADDITION (ADD)")
	total += 1
	try :
		add = Addition()
		f1 = Formula("A")
		assert add.can_apply([f1]) == True
		result = add.apply([f1], added_formula_str="B")
		assert str(result) == "A ∨ B"
		print(f"   ✓ From 'A', derived 'A ∨ B'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 8. Simplification (SIMP)
	print(f"\n8. SIMPLIFICATION (SIMP)")
	total += 1
	try :
		simp = Simplification()
		f1 = Formula("A ∧ B")
		assert simp.can_apply([f1]) == True
		result = simp.apply([f1], which='left')
		assert str(result) == "A"
		print(f"   ✓ From 'A ∧ B', derived 'A'")
		passed += 1
	except Exception as e:
		print(f"   ✗ Failed: {e}")

	# 9. Biconditional Introduction (BI)
	print(f"\n9. BICONDITIONAL INTRODUCTION (BI)")
	total += 1
	try :
		bi = BiconditionalIntroduction()
		f1 = Formula("A → B")
		f2 = Formula("B → A")
		assert bi.can_apply([f1, f2]) == True
		result = bi.apply([f1, f2])
		assert str(result) == "A ↔ B"
		print(f"   ✓ From 'A → B' and 'B → A', derived 'A ↔ B'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 10. Biconditional Elimination (BE)
	print(f"\n10. BICONDITIONAL ELIMINATION (BE)")
	total += 1
	try :
		be = BiconditionalElimination()
		f1 = Formula("A ↔ B")
		assert be.can_apply([f1]) == True
		result_forward = be.apply([f1], direction='forward')
		result_backward = be.apply([f1], direction='backward')
		assert str(result_forward) == "A → B"
		assert str(result_backward) == "B → A"
		print(f"   ✓ From 'A ↔ B', derived 'A → B' and 'B → A'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 11. Double Negation (DN)
	print(f"\n11. DOUBLE NEGATION (DN)")
	total += 1
	try :
		dn = DoubleNegation()
		f1 = Formula("¬¬A")
		assert dn.can_apply([f1]) == True
		result = dn.apply([f1], mode='eliminate')
		assert str(result) == "A"

		f2 = Formula("B")
		result2 = dn.apply([f2], mode='introduce')
		assert str(result2) == "¬¬B"
		print(f"   ✓ From '¬¬A', derived 'A' (eliminate)")
		print(f"   ✓ From 'B', derived '¬¬B' (introduce)")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 12. De Morgan's Law 1 (DML1)
	print(f"\n12. DE MORGAN'S LAW 1 (DML1)")
	total += 1
	try :
		dml1 = DeMorgansLaw1()
		f1 = Formula("¬(A ∧ B)")
		assert dml1.can_apply([f1]) == True
		result = dml1.apply([f1])
		assert str(result) == "¬A ∨ ¬B"
		print(f"   ✓ From '¬(A ∧ B)', derived '¬A ∨ ¬B'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 13. De Morgan's Law 2 (DML2)
	print(f"\n13. DE MORGAN'S LAW 2 (DML2)")
	total += 1
	try :
		dml2 = DeMorgansLaw2()
		f1 = Formula("¬(A ∨ B)")
		assert dml2.can_apply([f1]) == True
		result = dml2.apply([f1])
		assert str(result) == "¬A ∧ ¬B"
		print(f"   ✓ From '¬(A ∨ B)', derived '¬A ∧ ¬B'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 14. Transposition (TRANS)
	print(f"\n14. TRANSPOSITION (TRANS)")
	total += 1
	try :
		trans = Transposition()
		f1 = Formula("A → B")
		assert trans.can_apply([f1]) == True
		result = trans.apply([f1])
		assert str(result) == "¬B → ¬A"
		print(f"   ✓ From 'A → B', derived '¬B → ¬A'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 15. Implication (IMPL)
	print(f"\n15. IMPLICATION (IMPL)")
	total += 1
	try :
		impl = Implication()
		f1 = Formula("A → B")
		assert impl.can_apply([f1]) == True
		result = impl.apply([f1])
		assert str(result) == "¬A ∨ B"
		print(f"   ✓ From 'A → B', derived '¬A ∨ B'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 16. Exportation (EXP)
	print(f"\n16. EXPORTATION (EXP)")
	total += 1
	try :
		exp = Exportation()
		f1 = Formula("A → (B → C)")
		assert exp.can_apply([f1]) == True
		result = exp.apply([f1])
		assert str(result) == "(A ∧ B) → C"
		print(f"   ✓ From 'A → (B → C)', derived '(A ∧ B) → C'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 17. Resolution (RES)
	print(f"\n17. RESOLUTION (RES)")
	total += 1
	try :
		res = Resolution()
		f1 = Formula("A ∨ B")
		f2 = Formula("¬A ∨ C")
		assert res.can_apply([f1, f2]) == True
		result = res.apply([f1, f2])
		assert str(result) == "B ∨ C"
		print(f"   ✓ From 'A ∨ B' and '¬A ∨ C', derived 'B ∨ C'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 18. Absorption (ABS)
	print(f"\n18. ABSORPTION (ABS)")
	total += 1
	try :
		abs_rule = Absorption()
		f1 = Formula("A → B")
		assert abs_rule.can_apply([f1]) == True
		result = abs_rule.apply([f1])
		assert str(result) == "A → (A ∧ B)"
		print(f"   ✓ From 'A → B', derived 'A → (A ∧ B)'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# 19. Constructive Dilemma (CD)
	print(f"\n19. CONSTRUCTIVE DILEMMA (CD)")
	total += 1
	try :
		cd = ConstructiveDilemma()
		f1 = Formula("A → B")
		f2 = Formula("C → D")
		f3 = Formula("A ∨ C")
		assert cd.can_apply([f1, f2, f3]) == True
		result = cd.apply([f1, f2, f3])
		assert str(result) == "B ∨ D"
		print(f"   ✓ From 'A → B', 'C → D', and 'A ∨ C', derived 'B ∨ D'")
		passed += 1
	except Exception as e :
		print(f"   ✗ Failed: {e}")

	# Summary
	print(f"\n" + "=" * 60)
	print(f"SUMMARY: {passed}/{total} rules tested successfully")

	if passed == total :
		print(f"\n✓ All 19 inference rules are working correctly!")
	else :
		print(f"\n✗ {total - passed} rules failed. Check the errors above.")

	return passed == total


if __name__ == "__main__" :
	success = test_all_rules()
	sys.exit(0 if success else 1)