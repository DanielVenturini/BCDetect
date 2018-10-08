'''
This class represents a release.
The release has a version and some clients
'''

class Release:

    def __init__(self, version):
        self.version = version
        self.clients = []

    def addClient(self, client):
        self.clients.append(client)

    # return one client at time
    def getClient(self):
        for client in self.clients:
            yield client
