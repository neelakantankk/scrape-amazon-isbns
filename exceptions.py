class InvalidISBNError(Exception):
    '''Raised when len of an ISBN  is neither 13 not 10'''
    pass

class PageNotRetrievedError(Exception):
    '''Raised when call to amazon page fails'''
    pass

class ServiceUnavailableError(Exception):
    '''Raised when call to amazon page returns status code 503'''
    pass
