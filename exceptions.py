class SiteLoadException(Exception):
    def __init__(self, message): 
        super().__init__(message)
class SiteDOMException(Exception):
    def __init__(self, message): 
        super().__init__(message)
class NetworkingException(Exception):
    def __init__(self, message): 
        super().__init__(message)
        
class UtilsException(Exception):
    def __init__(self, message): 
        super().__init__(message)
        
class ParametersException(Exception):
    def __init__(self, message): 
        super().__init__(message)

class PlaywrightException(Exception):
    def __init__(self, message): 
        super().__init__(message)

class AddressException(Exception):
    def __init__(self, message): 
        super().__init__(message)
        
class CaptchaException(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class WrongInputException(Exception):
    def __init__(self, message):
        super().__init__(message)