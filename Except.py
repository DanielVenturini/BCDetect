# file with Exceptions

class MyGenericErr(Exception):

	def __init__(self, code=-1):
		self.code = code

	@property
	def code(self):
		return self._code

	@code.setter
	def code(self, code):
		self._code = code

class TestErr(MyGenericErr):

	def __str__(self):
		return 'npm test err with code ' + str(self.code)

class InstallErr(MyGenericErr):

	def __str__(self):
		return 'npm install err with code ' + str(self.code)

class ScriptTestErr(MyGenericErr):

	# code 1 if package.json hasn't scripts->test
	# code 0 if package.json doesn't specified test: 'echo \"Error: no test specified\" && exit 1'
	def __str__(self):
		if self._code:
			return 'script test hasn\'t key test'
		else:
			return 'script test hasn\'t specify test'

class NoDependencyChange(MyGenericErr):

	def __str__(self):
		return 'None dependency has changed ' + str(self.code)