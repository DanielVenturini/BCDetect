'''
This class represents a release.
The release has a version and some clients
'''

from Except import NoDependencyChange

class Release:

    def __init__(self, version, client_timestamp, client_previous_timestamp):
        self.version = version
        self.client_timestamp = client_timestamp
        self.client_previous_timestamp = client_previous_timestamp

        self.dependencies = []

    def addDependency(self, dependency):
        self.dependencies.append(dependency)

    # insertionSort: http://interactivepython.org/courselib/static/pythonds/SortSearch/TheInsertionSort.html
    def sort(self):
        for index in range(1, len(self.dependencies)):

            currentvalue = self.dependencies[index]
            position = index

            # compare 'abc@x.y.z' to 'acb@x.y.z'
            while position > 0 and self.dependencies[position-1].__str__() > currentvalue.__str__():
                self.dependencies[position] = self.dependencies[position-1]
                position = position-1

            self.dependencies[position] = currentvalue

    # return one client at time
    def getDependency(self):
        return self.dependencies

    def __str__(self):
        return self.version

    # if any dependency is changed to 'upgrade' or add, then need to install and test
    def verifyDependencyChange(self, onlyVersion):

        # force install and test even if hasnt change
        if onlyVersion:
            return
            
        for dependency in self.dependencies:
            if dependency.changed():
                return

        raise NoDependencyChange()