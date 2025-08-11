"""
Controller for button actions
Handles all button clicks and coordinates responses
"""


class ButtonController:
    """
    Handles all button interactions in the application
    """

    def __init__(self, button_panel, main_controller):
        """
        Initialize button controller

        Parameters:
            button_panel: ButtonPanel instance
            main_controller: MainController instance
        """
        self.button_panel = button_panel
        self.main_controller = main_controller

    def handle_mode_change(self, mode):
        """
        Handle mode radio button change

        Parameters:
            mode (str): "automatic" or "manual"
        """
        self.main_controller.handle_mode_change(mode)

    def handle_execute_proof(self):
        """Handle Execute Proof button click"""
        self.main_controller.handle_execute_proof()

    def handle_generate_table(self):
        """Handle Generate Truth Table button click"""
        self.main_controller.handle_generate_table()

    def handle_export(self):
        """Handle Export button click"""
        self.main_controller.handle_export()

    def handle_clear_all(self):
        """Handle Clear All button click"""
        self.main_controller.handle_clear_all()

    def handle_proposition_click(self, letter):
        """
        Handle atomic proposition button click

        Parameters:
            letter (str): The proposition letter (A-Z)
        """
        self.main_controller.handle_proposition_click(letter)

    def handle_connective_click(self, symbol):
        """
        Handle logical connective button click

        Parameters:
            symbol (str): The connective symbol
        """
        self.main_controller.handle_connective_click(symbol)

    def enable_rule_buttons(self):
        """Enable rule buttons for manual mode"""
        if hasattr(self.button_panel, 'enable_rule_buttons'):
            self.button_panel.enable_rule_buttons()

    def disable_rule_buttons(self):
        """Disable rule buttons for automatic mode"""
        if hasattr(self.button_panel, 'disable_rule_buttons'):
            self.button_panel.disable_rule_buttons()