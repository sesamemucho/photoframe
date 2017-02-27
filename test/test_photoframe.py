"""
Tests for `photoframe` module.
"""
import pytest
import pexpect
import sys
import time

from photoframe import mqclient

def send_command(cmd):
    pexpect.run('mosquitto_pub -t /house/things/thing1/cmd -m "{}"'.format(cmd))

def close_command():
    pexpect.run('mosquitto_pub -t /house/things/thing1/cmd -m "exit,0"')

@pytest.fixture(scope="module")
def broker():
    mosq = pexpect.spawn('mosquitto', encoding='utf-8')
    index = mosq.expect(['Opening ipv6 listen socket on port',
                         'Error: Address already in use',
                         pexpect.EOF, pexpect.TIMEOUT], timeout=0.5)
    if index == 0:
        use_this_server = True
        yield mosq
    elif index == 1:
        use_this_server = False
        yield "Already running"
    elif index == 2:
        pytest.fail("EOF from mosquitto invocation?")
    elif index == 3:
        pytest.fail("Timeout from mosquitto invocation?")


    if use_this_server:
        mosq.close(force=True)

@pytest.fixture(scope='session')
def photoframe():
    pf = pexpect.spawn('tstcommands.py', encoding='utf-8')
    index = pf.expect(['Received SUBACK', pexpect.EOF, pexpect.TIMEOUT],
                      timeout=1)
    assert index == 0
    yield pf
    pf.close(force=True)

class TestPhotoframe(object):

    def test_basic_command(self, broker, photoframe):
        pf = photoframe

        send_command('wake,0')
        index = pf.expect(['Performed wake command',
                           pexpect.EOF, pexpect.TIMEOUT], timeout=1)
        assert index == 0

    def test_command_with_delay(self, broker, photoframe):
        pf = photoframe

        send_command('wake,5')
        index = pf.expect(['Performed wake command',
                           pexpect.EOF, pexpect.TIMEOUT], timeout=4)
        assert index == 2

        index = pf.expect(['Performed wake command',
                           pexpect.EOF, pexpect.TIMEOUT], timeout=2)
        assert index == 0

    def test_delay_with_override(self, broker, photoframe):
        pf = photoframe

        send_command('wake,5')
        time.sleep(1)
        send_command('id,0')
        index = pf.expect(['Performed id command',
                           pexpect.EOF, pexpect.TIMEOUT], timeout=1)
        assert index == 0

    def test_bad_command(self, broker, photoframe):
        pf = photoframe

        send_command('badcmd,0')
        index = pf.expect(['Command badcmd is not a valid command',
                           pexpect.EOF, pexpect.TIMEOUT], timeout=1)
        assert index == 0

    def test_bad_delay(self, broker, photoframe):
        pf = photoframe

        send_command('wake,4000')
        index = pf.expect(['Delay 4000 is out of range',
                           pexpect.EOF, pexpect.TIMEOUT], timeout=1)
        assert index == 0
