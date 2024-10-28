class InputHandler:
    """
    InputHandler class to manage user input with optional default responses.

    Attributes:
        no_input (bool): Flag to determine if user input should be bypassed.
        default_response (str): Default response to use when no_input is True.

    Methods:
        __init__(no_input=False, default_response='y'):
            Initializes the InputHandler with optional no_input flag and default response.
        
        get_input(prompt):
            Prompts the user for input unless no_input is True, in which case it returns the default response.
            Args:
                prompt (str): The prompt message to display to the user.
            Returns:
                str: The user's input or the default response.
    """
    def __init__(self, no_input=False, default_response='y'):
        self.no_input = no_input
        self.default_response = default_response

    def get_input(self, prompt):
        if not self.no_input:
            return input(prompt).lower().strip()
        return self.default_response
