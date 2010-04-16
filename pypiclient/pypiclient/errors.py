class ClientError(Exception):
    """Base class for all pypiclient errors

    """
    pass

class ProjectDoesNotExist(ClientError):
    pass

class ProjectDownloadUrlDoesNotExist(ClientError):
    pass
