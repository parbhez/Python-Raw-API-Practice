# blog_api.py
import mysql.connector
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# MySQL connection info
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # নিজের পাসওয়ার্ড দাও
    'database': 'blog_db'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

class BlogHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _read_json(self):
        content_length = int(self.headers['Content-Length'])
        return json.loads(self.rfile.read(content_length))

    def do_GET(self):
        if self.path == '/blogs':
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blogs")
            rows = cursor.fetchall()
            blogs = []
            for row in rows:
                blogs.append({
                    'id': row[0],
                    'title': row[1],
                    'slug': row[2],
                    'body': row[3],
                    'image': row[4]
                })
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps(blogs).encode())

    def do_POST(self):
        if self.path == '/blogs':
            data = self._read_json()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO blogs (title, slug, body, image) VALUES (%s, %s, %s, %s)",
                           (data['title'], data['slug'], data.get('body'), data.get('image')))
            conn.commit()
            conn.close()
            self._set_headers(201)
            self.wfile.write(json.dumps({'message': 'Blog created'}).encode())

    def do_PUT(self):
        if self.path.startswith('/blogs/'):
            blog_id = int(self.path.split('/')[-1])
            data = self._read_json()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE blogs SET title=%s, slug=%s, body=%s, image=%s WHERE id=%s",
                           (data['title'], data['slug'], data.get('body'), data.get('image'), blog_id))
            conn.commit()
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps({'message': 'Blog updated'}).encode())

    def do_DELETE(self):
        if self.path.startswith('/blogs/'):
            blog_id = int(self.path.split('/')[-1])
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM blogs WHERE id=%s", (blog_id,))
            conn.commit()
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps({'message': 'Blog deleted'}).encode())

def run(server_class=HTTPServer, handler_class=BlogHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
