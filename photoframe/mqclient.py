
import queue
import paho.mqtt.client as mqtt
import threading
import time

from photoframe import shared


def worker(q, cmd_obj, publish_func):
    need_command = True
    cmd_obj.hello()
    while True:
        if need_command:
            cmd, delay = q.get()

        if cmd == "exit":
            break

        # print("Processing {} with delay of {} seconds".format(cmd, delay))
        need_command = True

        # Check it again
        timer = min(abs(delay), 3600)
        while((timer > 0) and need_command):
            try:
                cmd, delay = q.get_nowait()
                need_command = False
                # print("Got command \"{}\" during sleep".format(cmd))
            except queue.Empty:
                time.sleep(0.1)
                timer -= 0.1

        cmd_obj.execute(cmd)
        publish_func(shared.LOG_TOPIC, "Done with stuff", 0, False)


class MqttClient(mqtt.Client):

    def __init__(self, cmd_obj, **kwargs):
        """
        :param kwargs: Passed to the superclass constructor.

        """
        super(MqttClient, self).__init__(**kwargs)
        self.do_run = True
        self.cmd_queue = queue.Queue(4)
        self.cmds = cmd_obj

    def on_connect(self, mqclient, userdata, flags, rc):
        self.do_run = True
        print("on_connect, rc is \"{}\"".format(rc))

    def on_subscribe(self, mqclient, userdata, mid, granted_qos):
        print("on_subscribe: mid {}  qos {}".format(mid, granted_qos))

    def on_message(self, mqclient, userdata, message):
        # print("Received message '" + str(message.payload) + "' on topic '"
        #    + message.topic + "' with QoS " + str(message.qos))
        (cmd, delay) = message.payload.split(b",")
        delay = int(delay)
        cmd = str(cmd, encoding='utf-8', errors='strict')
        # print("cmd is {}, delay is {}".format(cmd, delay))
        if (delay < 0) or (delay > 3600):
            print("Delay {} is out of range (0, 3600)".format(delay))
        elif not self.cmds.is_valid_command(cmd):
            print("Command {} is not a valid command".format(cmd))
        else:
            # print("Processing cmd {}".format(cmd))
            try:
                self.cmd_queue.put_nowait((cmd, delay))
            except queue.Full:
                print("Queue full, ignoring")
            except:
                print("Wierd exception")
                self.do_run = False

    def on_log(self, mqclient, userdata, level, buf):
        print("log: \"{}\"".format(buf))

    def run(self):
        self.connect(shared.MQTT_BROKER)
        self.subscribe(shared.CMD_TOPIC, 2)
        t = threading.Thread(target=worker,
                             args=(self.cmd_queue, self.cmds, self.publish))
        t.start()

        self.loop_start()
        print("Starting do_run loop: {}".format(self.do_run))

        t.join()
        print("Exiting")
