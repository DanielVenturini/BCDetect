'''
This class represents a dependency
Dependency has a name, a type - dependencies or devDependencies - and a specify version
'''

class Dependency:

    def __init__(self, name, version, type):
        self.name = name
        self.type = type
        self.version = version

    def __str__(self):
        return self.name + '@' + self.version + '-' + self.type