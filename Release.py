'''
This class represents a release.
The release has a version and some clients
'''

class Release:

    def __init__(self, version, client_timestamp, client_previous_timestamp):
        self.version = version
        self.client_timestamp = client_timestamp
        self.client_previous_timestamp = client_previous_timestamp

        self.dependencies = []

    def addDependency(self, dependency):
        self.dependencies.append(dependency)

    # return one client at time
    def getDependency(self):
        return self.dependencies

    def __str__(self):
        '''print('-------------------{0}--------------------'.format(self.version))
        for dependency in self.dependencies:
            print(dependency)

        return('-------------------{0}--------------------'.format(self.version))'''
        return self.version