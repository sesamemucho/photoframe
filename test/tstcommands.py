#! /usr/bin/env python

"""photoframe testing commands module.
This module handles the execution of any shell commands.
"""

from photoframe import mqclient

VALID_COMMANDS = ('wake', 'sleep', 'id', 'weather', 'photo', 'exit')

class PhotoFrameCommands(object):

    def is_valid_command(self, cmd):
        return cmd in VALID_COMMANDS

    def execute(self, cmd):
        if self.is_valid_command(cmd):
            getattr(self, cmd)()

    def hello(self):
        print("tst Hello from photoframe commands!")

    def wake(self):
        print("tst Performed wake command")

    def sleep(self):
        print("tst Performed sleep command")

    def id(self):
        print("tst Performed id command")

    def weather(self):
        print("tst Performed weather command")

    def photo(self):
        print("tst Performed photo command")

    def exit(self):
        print("tst Performed exit command")

if __name__ == "__main__":

    my_cmds = PhotoFrameCommands()
    client = mqclient.MqttClient(my_cmds)
    client.run()


