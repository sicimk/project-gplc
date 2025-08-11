"""
View package for GPLC
Contains all user interface components
"""

from .main_window import MainWindow
from .app_view import AppView
from .premises_panel import PremisesPanel
from .conclusions_panel import ConclusionsPanel
from .proof_steps_panel import ProofStepsPanel
from .button_panel import ButtonPanel
from .truth_table_panel import TruthTablePanel
from .error_display import ErrorDisplay
from .menu_bar import MenuBar
from .instructions_panel import InstructionsPanel

__all__ = [
    'MainWindow',
    'AppView',
    'PremisesPanel',
    'ConclusionsPanel',
    'ProofStepsPanel',
    'ButtonPanel',
    'TruthTablePanel',
    'ErrorDisplay',
    'MenuBar',
    'InstructionsPanel'
]