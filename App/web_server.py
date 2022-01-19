from http.server import HTTPServer, SimpleHTTPRequestHandler
from sqlite3 import connect
from urllib.parse import urlparse, parse_qs

from matplotlib.cbook import normalize_kwargs
import database.database as db
import cgi
import pyautogui

HOST_NAME = "127.0.0.1"
PORT = 8404

PATH_HTML = "./templates"

def butt_del(table,id):
    table=table[:2]
    return f'''<form method="POST", enctype="multipart/form-data" action="/del_{table}_{id}">
            <input type="submit" value="Usun">
        </form>'''

def butt_mod(table,id):
    table=table[:2]
    return f'''<form method="POST", enctype="multipart/form-data" action="/mod_{table}_{id}">
            <input type="submit" value="Modyfikuj">
        </form>'''

def read_html_template(path):
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file

def print_records(q):
    rows = q.fetchall()
    for row in rows:
        print(row)

class PythonServer(SimpleHTTPRequestHandler):
    def respond(self, file):
        tmp=read_html_template(file)
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(tmp, "utf-8"))
        
    def show_records(self,path,table_name,table_data):
        file = read_html_template(path)

        table_row = ""
        for data in table_data:
            table_row += "<tr>"
            for item in data:
                table_row += "<td>"
                table_row += str(item)
                table_row += "</td>"
                
            #modif butt
            table_row += "<td>"
            #table_row += butt_mod(table_name,str(data[0]))
            table_row += f'<a class="button" href="/mod_{table_name}_{str(data[0])}">Modyfikuj</a><br>'
            table_row += "</td>"
            
            #del butt
            table_row += "<td>"
            table_row += butt_del(table_name,str(data[0]))
            table_row += "</td>"
            
            table_row += "</tr>"
        file = file.replace("{{records}}", table_row)
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(file, "utf-8"))
        
    def do_GET(self):
        if self.path == '/' or self.path == '/?':
            self.respond(PATH_HTML+"/index.html")
        elif self.path=='/show_ProductTypes':
            self.show_records(PATH_HTML+"/show_productTypes.html","RP",db.fetch_records("Rodzaje_produktow"))
        elif self.path=='/show_MaterialTypes':
            self.show_records(PATH_HTML+"/show_materialTypes.html","RM",db.fetch_records("Rodzaje_materialow"))
        elif self.path[:4]=='/mod':
            #mod_??_{id}
            tab=self.path[5:7]
            
            if not '?' in self.path:            
                self.respond(PATH_HTML+f"/mod_{tab}.html")
            else:
                query_components = parse_qs(urlparse(self.path).query)
                id=self.path[8:self.path.index('?')]
                if tab=="RP":
                    nazwa = query_components["prodType"][0]
                    db.Rodzaje_produktow.update_record(id,nazwa)
                    self.path="/show_ProductTypes"
                elif tab=="RM":
                    nazwa = query_components["matType"][0]
                    cena = query_components["matPrice"][0]
                    db.Rodzaje_materialow.update_record(id,nazwa,cena)
                    self.path="/show_MaterialTypes"
                    
                tmp=f'<html><head><meta charset="UTF-8"/><script>window.location.href="{self.path}"</script></head><body></body></html>'
                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(tmp, "utf-8"))

    def do_POST(self):
        if self.path=='/add_new_productType':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                nazwa = fields.get("prodType")[0]
                db.Rodzaje_produktow.insert_record(nazwa)

            self.path="/show_ProductTypes"
            pyautogui.hotkey('f5')
            
        elif self.path=='/add_new_materialType':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                nazwa = fields.get("matType")[0]
                cena = fields.get("matPrice")[0]
                db.Rodzaje_materialow.insert_record(nazwa,cena)

            self.path="/show_MaterialTypes"
            pyautogui.hotkey('f5')
            
        elif self.path[:4]=='/del':
            #del_??_{id}
            tab=self.path[5:7]
            id=self.path[8:]
    
            if tab=="RP":
                table="Rodzaje_produktow"
            elif tab=="RM":
                table="Rodzaje_materialow"
                
            db.del_record_byID(table,id)
            self.path="/show_ProductTypes"
            pyautogui.hotkey('f5')
                        
        
def server_start():
    db.connection = connect(db.DB_NAME)
    db.cursor = db.connection.cursor()
    #db.database_hard_reset()
    db.database_init()
    
    #db.Rodzaje_produktow.insert_record("Palety")
    #db.Rodzaje_produktow.insert_record("Skrzynie")
    #db.MyQuery("Select * from Rodzaje_produktow")
    
    server = HTTPServer((HOST_NAME, PORT), PythonServer)
    print(f"Server started http://{HOST_NAME}:{PORT}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        db.cursor.close()
        db.connection.close()
        server.server_close()
        print("Server stopped successfully")
        
