import  json
from http.server import  HTTPServer, BaseHTTPRequestHandler

class RequestHandle(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path !='/helloworld':
            self.send_error(404, "page not found")
            return

        data = {
            'result_code': '200',
            "data": "hello world"
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        req_datas = self.rfile.read(int(self.headers['content-length']))
        print(req_datas.decode())
        data = {
            'result_code': '200',
            'data': req_datas.decode()
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


if __name__ == '__main__':
    host = ('localhost', 8090)
    server = HTTPServer(host, RequestHandle)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

