"""photoframe commands module.
This module handles the execution of any shell commands.
"""

VALID_COMMANDS = ('wake', 'sleep', 'id', 'weather', 'photo', 'exit')

class PhotoFrameCommands(object):

    def is_valid_command(self, cmd):
        return cmd in VALID_COMMANDS

    def execute(self, cmd):
        if self.is_valid_command(cmd):
            getattr(self, cmd)()

    def hello(self):
        print("Hello from photoframe commands!")

    def wake(self):
        print("Performed wake command")

    def sleep(self):
        print("Performed sleep command")

    def id(self):
        print("Performed id command")

    def weather(self):
        print("Performed weather command")

    def photo(self):
        print("Performed photo command")

    def exit(self):
        print("Performed exit command")

