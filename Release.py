'''
This class represents a release.
The release has a version and some clients
'''

class Release:

    def __init__(self, version):
        self.version = version
        self.dependencies = []

    def addDependency(self, dependency):
        self.dependencies.append(dependency)

    # return one client at time
    def getDependency(self):
        for dependency in self.dependencies:
            yield dependency

    def __str__(self):
        print('-------------------{0}--------------------'.format(self.version))
        for dependency in self.dependencies:
            print(dependency)

        return('-------------------{0}--------------------'.format(self.version))