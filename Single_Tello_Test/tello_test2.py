from tello import Tello
import sys
from datetime import datetime
import time

start_time = str(datetime.now())

file_name = sys.argv[1]
print(file_name)

f = open(file_name, "r")
commands = f.readlines()
argv_len = len(sys.argv)  # コマンドラインの数取得
print(argv_len)

try:
    tello = Tello('10.10.4.175', '10.10.4.176', "10.10.4.186")
    print(tello)
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()

            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print

                ('delay %s' % sec)
                time.sleep(sec)
                pass
            else:
                tello.send_command(command)

        log = tello.get_log()

        out = open('log/' + start_time + '.txt', 'w')
        for stat in log:
            stat.print_stats()
            str = stat.return_stats()
            out.write(str)


except KeyboardInterrupt:
    tello.send_command("command")
    # tello.send_command("land")
    tello.send_command("emergency")
