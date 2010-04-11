class ClientException(Exception):
    """Base class for all client exceptions.

    """
    pass

class ProjectDoesNotExist(ClientException):
    pass

class ProjectDownloadUrlDoesNotExist(ClientException):
    pass
