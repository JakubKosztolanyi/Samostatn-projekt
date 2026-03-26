import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from Hra.html_generator import aktualizuj_html

PORT = 8000
admin = False


def get_scores():

    conn = sqlite3.connect("Hra/hramenu.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, jmeno, body, datum FROM score ORDER BY body DESC")

    data = cursor.fetchall()

    conn.close()
    return data


def delete_score(id):

    conn = sqlite3.connect("Hra/hramenu.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM score WHERE id=?", (id,))
    conn.commit()

    conn.close()


class Server(BaseHTTPRequestHandler):

    def do_GET(self):

        global admin

        # CSS
        if self.path == "/style.css":

            with open("Web/style.css", "r", encoding="utf-8") as f:
                css = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()

            self.wfile.write(css.encode())
            return


        # mazání score
        if self.path.startswith("/delete") and admin:

            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)

            delete_score(params["id"][0])

            aktualizuj_html()

            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            return


        scores = get_scores()

        rows = ""

        for i, s in enumerate(scores, start=1):

            delete_button = ""

            if admin:
                delete_button = f'<td><a style="color:red;" href="/delete?id={s[0]}">❌</a></td>'

            rows += f"""
<tr>
<td>{i}</td>
<td>{s[1]}</td>
<td>{s[2]}</td>
<td>{s[3]}</td>
{delete_button}
</tr>
"""


        admin_column = ""

        if admin:
            admin_column = "<th>Smazat</th>"


        # přihlášení
        if not admin:

            login_html = """
<form method="post" action="/login" style="margin-bottom:20px;">
<input type="password" name="heslo" placeholder="Admin heslo">
<button type="submit">Přihlásit</button>
</form>
"""

        else:

            login_html = """
<form method="post" action="/logout" style="margin-bottom:20px;">
<button type="submit">Odhlásit se</button>
</form>
"""


        html = f"""
<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<title>Admin – Score</title>
<link rel="stylesheet" href="/style.css">
</head>

<body>

<div class="container">

<h1>🏆 SCORE TABULKA</h1>
<div class="subtitle">Admin správa výsledků</div>

{login_html}

<table>

<thead>
<tr>
<th>#</th>
<th>Hráč</th>
<th>Skóre</th>
<th>Datum</th>
{admin_column}
</tr>
</thead>

<tbody>

{rows}

</tbody>

</table>

</div>

</body>
</html>
"""

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(html.encode())


    def do_POST(self):

        global admin

        if self.path == "/login":

            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length).decode()

            params = urllib.parse.parse_qs(data)

            if params["heslo"][0] == "admin":
                admin = True


        if self.path == "/logout":

            admin = False


        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()


print("Server běží na:")
print("http://localhost:8000")

server = HTTPServer(("localhost", PORT), Server)

try:
    server.serve_forever()

except KeyboardInterrupt:
    print("\nServer byl ukončen (CTRL+C)")

finally:
    server.server_close()
    print("Server vypnut")