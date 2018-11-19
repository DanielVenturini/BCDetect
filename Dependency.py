'''
This class represents a dependency
Dependency has a name, a type - dependencies or devDependencies - and a specify version
'''

class Dependency:

    def __init__(self, name, version, type, change_type):
        self.name = name
        self.type = type
        self.version = version
        self.change_type = change_type

    def __str__(self):
        return self.name + '@' + self.version + '-' + self.type + '-' + self.change_type

    def changed(self):
    	return self.change_type.__eq__('upgrade') or self.change_type.__eq__('')