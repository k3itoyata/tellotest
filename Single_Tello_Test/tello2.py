import socket
import threading
import time
from stats import Stats


class Tello:
    def __init__(self, *ip):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        print(self.socket)
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        tello_ips = ip
        print(tello_ips[0])
        for i in range(len(tello_ips)):
            self.tello_ip = tello_ips[i]
            self.tello_port = 8889
            name = "self.tello_adderss{} = {}".format(
                i, (self.tello_ip, self.tello_port))
            exec(name)
            print(name)

            self.log = []

            self.MAX_TIME_OUT = 15.0

    def send_command(self, command):
        """
        Send a command to the ip address. Will be blocked until
        the last command receives an 'OK'.
        If the command fails (either b/c time out or error),
        will try to resend the command
        :param command: (str) the comman
        d to send
        :param ip: (str) the ip of Tello
        :return: The latest command response
        """
        print("--------------------")
        print(command)
        print(self.tello_adderss1)
        print(self.tello_adderss0)
        print("--------------------")

        def test_a():
            self.socket.sendto(command.encode('utf-8'), self.tello_adderss0)

        def test_b():
            self.socket.sendto(command.encode('utf-8'), self.tello_adderss1)

        def test_c():
            self.socket.sendto(command.encode('utf-8'), self.tello_adderss2)

        self.log.append(Stats(command, len(self.log)))

        test_a_thread = threading.Thread(target=test_a)
        test_b_thread = threading.Thread(target=test_b)
        test_c_thread = threading.Thread(target=test_c)

        test_a_thread.start()
        test_b_thread.start()
        test_c_thread.start()

        # print ('sending command: %s to %s' % (command, self.tello_ip))

        # start = time.time()
        # while not self.log[-1].got_response():
        #     now = time.time()
        #     diff = now - start
        #     if diff > self.MAX_TIME_OUT:
        #         print ('Max timeout exceeded... command %s' % command)
        #         # TODO: is timeout considered failure or next command still get executed
        #         # now, next one got executed
        #         return
        # print ('Done!!! sent command: %s to %s' % (command, self.tello_ip))

    def _receive_thread(self):
        """Listen to responses from the Tello.

        Runs as a thread, sets self.response to whatever the Tello last returned.

        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))

                self.log[-1].add_response(self.response)
            except socket.error as exc:
                print("Caught exception socket.error : %s" % exc)

    def on_close(self):
        pass
        # for ip in self.tello_ip_list:
        #     self.socket.sendto('land'.encode('utf-8'), (ip, 8889))
        # self.socket.close()

    def get_log(self):
        return self.log
