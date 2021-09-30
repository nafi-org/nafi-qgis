
class InitializationException(Exception): 

    """
    Exception raised when there is a error during a script initialization.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, *args):
    
        if args:
            self.message = args[0]
        else:
            self.message = "Initialization error"
        return

    def __str__(self):
        return self.message
    

class ProcessingException(Exception): 

    """
    Exception raised when there is a metric processing error.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, *args):
    
        if args:
            self.message = args[0]
        else:
            self.message = "Processing error"
        return

    def __str__(self):
        return self.message


class InvalidFileException(Exception): 

    """
    Exception raised when running into a invalid geotiff file.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, *args):
    
        if args:
            self.message = args[0]
        else:
            self.message = "Invalid GEOTIFF file error"
        return

    def __str__(self):
        return self.message
