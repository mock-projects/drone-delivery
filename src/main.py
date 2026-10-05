from tests.test_suite import run_tests

class Runner:
	def run(self):
		self.print_intro('Drone Delivery')

		run_tests()

	def print_intro(self, codebase_title):
		'''Prints a brief intro to the codebase.'''
		print('\nWelcome to the ' + codebase_title + ' codebase!')
		print('Start by reading through the README file for your instructions,')
		print('then familiarize yourself with the rest of the files in the codebase.')
		print("When you're ready, start tackling the TODOs in the codebase.\n")

if __name__ == '__main__':
	Runner().run()
