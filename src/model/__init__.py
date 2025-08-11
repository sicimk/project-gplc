"""
Model package for GPLC
Contains all business logic and data structures
"""

# Use relative imports to avoid circular dependencies
from .formula import Formula
from .validator import FormulaValidator
from .proof_system import ProofSystem, ProofStep
from .truth_table import TruthTable
from .inference_rules import (
    get_all_rules,
    get_rule_by_name,
    get_rule_by_abbreviation,
    InferenceRule
)
from .file_exporter import FileExporter

__all__ = [
    'Formula',
    'FormulaValidator',
    'ProofSystem',
    'ProofStep',
    'TruthTable',
    'get_all_rules',
    'get_rule_by_name',
    'get_rule_by_abbreviation',
    'InferenceRule',
    'FileExporter'
]