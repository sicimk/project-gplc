"""
Controller package for GPLC
Contains all application control logic and event handlers
"""

# Import all controller classes for easy access
from controller.main_controller import MainController
from controller.input_controller import InputController
from controller.proof_controller import ProofController
from controller.button_controller import ButtonController
from controller.table_controller import TableController
from controller.error_controller import ErrorController
from controller.menu_controller import MenuController

# Define what gets imported with "from controller import *"
__all__ = [
    'MainController',
    'InputController',
    'ProofController',
    'ButtonController',
    'TableController',
    'ErrorController',
    'MenuController'
]