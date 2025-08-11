"""
Controller for error handling and display
Manages all error messages and user notifications
"""

import time
from threading import Timer


class ErrorController:
    """
    Manages error messages and user notifications
    """

    def __init__(self, error_display):
        """
        Initialize error controller

        Parameters:
            error_display: ErrorDisplay instance
        """
        self.error_display = error_display

        # Timer for auto-clearing messages
        self.clear_timer = None

        # Message history for debugging
        self.message_history = []
        self.max_history = 100

    def show_error(self, error_type, message):
        """
        Display an error message

        Parameters:
            error_type (str): Type of error (syntax, validation, etc.)
            message (str): Error message to display
        """
        # Cancel any pending clear
        self._cancel_clear_timer()

        # Add to history
        self._add_to_history("error", f"{error_type}: {message}")

        # Display error
        self.error_display.show_error(error_type, message)

    def show_warning(self, warning_type, message):
        """
        Show warning message

        Parameters:
            warning_type (str): Type of warning
            message (str): Warning message to display
        """
        # Cancel any pending clear
        self._cancel_clear_timer()

        # Add to history
        self._add_to_history("warning", f"{warning_type}: {message}")

        # Display warning
        self.error_display.show_warning(warning_type, message)

        # Auto-clear after 4 seconds
        self._set_clear_timer(4.0)

    def show_info(self, message):
        """
        Show informational message

        Parameters:
            message (str): Info message to display
        """
        # Cancel any pending clear
        self._cancel_clear_timer()

        # Add to history
        self._add_to_history("info", message)

        # Display info
        self.error_display.show_info(message)

        # Auto-clear after 3 seconds
        self._set_clear_timer(3.0)

    def clear_messages(self):
        """Clear all messages"""
        self._cancel_clear_timer()
        self.error_display.clear_all_errors()

    def clear_all_errors(self):
        """Clear all errors"""
        self.clear_messages()

    def _add_to_history(self, msg_type, message):
        """
        Add message to history

        Parameters:
            msg_type (str): Type of message
            message (str): The message
        """
        timestamp = time.strftime("%H:%M:%S")
        self.message_history.append({
            'time': timestamp,
            'type': msg_type,
            'message': message
        })

        # Keep history size limited
        if len(self.message_history) > self.max_history:
            self.message_history.pop(0)

    def _set_clear_timer(self, delay):
        """
        Set timer to clear message

        Parameters:
            delay (float): Delay in seconds
        """
        self._cancel_clear_timer()
        self.clear_timer = Timer(delay, self.clear_messages)
        self.clear_timer.start()

    def _cancel_clear_timer(self):
        """Cancel any pending clear timer"""
        if self.clear_timer and self.clear_timer.is_alive():
            self.clear_timer.cancel()

    def get_history(self):
        """Get message history"""
        return self.message_history.copy()

    def clear_history(self):
        """Clear message history"""
        self.message_history = []