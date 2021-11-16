class ArgNotFoundError(Exception):
    """
    value not defined in arguments
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{{ ' + str(self.value) + ' }} not defined in arguments'