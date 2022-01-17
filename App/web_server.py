from http.server import HTTPServer, SimpleHTTPRequestHandler
from sqlite3 import connect
import database.database as db

HOST_NAME = "127.0.0.1"
PORT = 8404

PATH_HTML = "./templates"

def read_html_template(path):
    # function to read HTML file
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file

class PythonServer(SimpleHTTPRequestHandler):
    def respond(self, file):
        tmp=read_html_template(file)
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(tmp, "utf-8"))
        
    def do_GET(self):
        global game_is_on, game_time, game_finished, player_status, match_id, players, game_start
        if self.path == '/':
            self.respond(PATH_HTML+"/index.html")

def server_start():
    db.connection = connect(db.DB_NAME)
    db.cursor = db.connection.cursor()
    
    server = HTTPServer((HOST_NAME, PORT), PythonServer)
    print(f"Server started http://{HOST_NAME}:{PORT}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        db.cursor.close()
        db.connection.close()
        server.server_close()
        print("Server stopped successfully")