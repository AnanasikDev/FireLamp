from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import threading
import matrix

html = "<html><body>Hello from the Raspberry Pi</body></html>"

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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
