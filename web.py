from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import threading
import matrix

import sys
import trace
import time

html = "<html><body>Hello from the Raspberry Pi</body></html>"
alarmthread = None
#kill = False


class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        global alarmthread

        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        elif self.path.startswith("/sc"): # set color
            try:
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                r = query_components["r"]
                g = query_components["g"]
                b = query_components["b"]
                #i = query_components["i"]
                # query_components = { "imsi" : "Hello" }

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #matrix.modes[3]()
                if matrix.MODE != 0 : matrix.modechanged = True
                matrix.MODE = 0
                matrix.fill(matrix.Color(int(r), int(g), int(b)))
                #matrix.LED_BRIGHTNESS = i
                #matrix.init()
                self.wfile.write(f"RGB = {r}, {g}, {b}".encode('utf-8'))
            except:
                pass

        elif self.path.startswith("/sm"): # set mode
            try:
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                modeid = int(query_components["mi"])
                ops = query_components["ops"] # options

                ops = list(ops.split(','))

                #i = query_components["i"]
                # query_components = { "imsi" : "Hello" }

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                #matrix.LED_BRIGHTNESS = i
                #matrix.init()
                self.wfile.write(f"MODE = {modeid}".encode('utf-8'))
                matrix.fill(matrix.Color(0,0,0))
                matrix.modechanged = True
                matrix.MODES_ARGS = ops
                matrix.MODE = modeid
                # for i in range(1000):
                #     matrix.modes[modeid]()

            except:
                pass

        elif self.path.startswith("/se"): # set enable/disable
            try:
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                enable = int(query_components["e"])
                #i = query_components["i"]
                # query_components = { "imsi" : "Hello" }

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                if enable == 1:
                    matrix.fill(matrix.Color(0,100,0))
                elif enable == 0:
                    matrix.fill(matrix.Color(0,0,0))
                #matrix.modes[modeid]()
                #matrix.LED_BRIGHTNESS = i
                #matrix.init()
                self.wfile.write(f"Enabled = {enable}".encode('utf-8'))
            except:
                pass

        elif self.path.startswith("/ss"): # set settings
            try:
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                enable = int(query_components["e"])
                brightness = float(query_components["b"])
                # i = query_components["i"]
                # query_components = { "imsi" : "Hello" }

                if enable == 1:
                    matrix.fill(matrix.Color(0, 100, 0))
                elif enable == 0:
                    matrix.fill(matrix.Color(0, 0, 0))

                matrix.brightness = brightness

                print(brightness)

                # matrix.modes[modeid]()
                # matrix.LED_BRIGHTNESS = i
                # matrix.init()
                self.wfile.write(f"Enabled = {enable}".encode('utf-8'))
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
            except:
                pass

        elif self.path.startswith("/st"): # set time
            try:
                print("Crya")

                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                schedule = query_components["sch"]
                current_time = int(query_components["time"])
                day = int(query_components["day"])
                e = int(query_components["e"])  # Состояние (Вкл/Выкл)

                print(e)

                if e == 0:
                    matrix.sunriseon = False
                    print(matrix.sunriseon)

                else:

                    matrix.sunriseon = True

                    # currenttime = list(map(int, c.split(":")))
                    # currentseconds = currenttime[-1] + currenttime[-2] * 60 + currenttime[-3] * 3600 + currenttime[-4] * 86400
                    #
                    # targettime = list(map(int, t.split(":")))
                    # targetseconds = targettime[-1] + targettime[-2] * 60 + targettime[-3] * 3600 + targettime[-4] * 86400
                    #
                    # schedule = list(map(int, s.split(":")))
                    #
                    # target_day_of_week = targettime[-7]
                    #
                    # print("TARGET = ", targettime)
                    #
                    # duration = list(map(int, d.split(":")))
                    # print(duration)
                    # durationseconds = duration[-1] + duration[-2] * 60 + duration[-3] * 3600
                    # print(durationseconds)

                    # if targetseconds < currentseconds:
                    #     print("TIME IS WRONG")
                    #
                    # else:

                    matrix.MODE = 0
                    if alarmthread != None and alarmthread.is_alive():
                        # threading.Event().set()
                        # alarmthread._stop()
                        # alarmthread.setDaemon(true)
                        alarmthread.kill()
                    #kill = True
                    #alarmthread = threading.Thread(target=matrix.sunrise, args=(schedule, time, day))
                    #alarmthread.start()

                    current_seconds = time.time()

                    alarmthread = thread_with_trace(target=matrix.sunrise, args=(schedule, current_seconds, day))
                    alarmthread.start()

                    # matrix.sunrise(currentseconds, targetseconds, durationseconds)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

            except:
                pass

        else:
            self.send_error(404, "Page Not Found {}".format(self.path))


def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    port = 80
    print("Starting server at port %d" % port)
    x = threading.Thread(target=matrix.process_mode)
    x.start()
    server_thread(port)
    #matrix.fill(matrix.Color(0, 200, 0))
