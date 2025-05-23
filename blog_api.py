# blog_api.py
from db_config import connect_to_db as get_connection
import json


#Python এর built-in HTTP server module import করা হয়েছে।
from http.server import BaseHTTPRequestHandler, HTTPServer #BaseHTTPRequestHandler দিয়ে HTTP request handle করা হয়, আর HTTPServer দিয়ে সার্ভার চালানো হয়।

# BlogHandler এটি একটি class যা BaseHTTPRequestHandler কে extend করছে, অর্থাৎ HTTP request handle করার জন্য কাস্টম হ্যান্ডলার তৈরি করা হয়েছে।
class BlogHandler(BaseHTTPRequestHandler):
    # _set_headersএটি একটি হেল্পার মেথড যা response এর status code এবং header সেট করার কাজ করে।
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

   
    def _read_json(self):
        content_length = int(self.headers.get('Content-Length', 0))
        print(f"✅ content_length: {content_length}")
        if content_length == 0:
            print(f"✅ No data received in the request")
            self._set_headers(400)
            self.wfile.write(json.dumps({
                'message': 'No data received in the request',
            }).encode())
            return None  # Return None or an appropriate value to indicate failure

        raw_data = self.rfile.read(content_length)
        print(f"✅ raw_data: {raw_data}")
        
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError:
            print(f"✅ Invalid JSON data received in the request")
            self._set_headers(400)
            self.wfile.write(json.dumps({
                'message': 'Invalid JSON data received in the request',
            }).encode())
            return None  # Return None to indicate failure



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
            self.wfile.write(json.dumps(blogs).encode()) #এটি হচ্ছে output stream — এর মাধ্যমে server থেকে ক্লায়েন্টকে ডেটা পাঠানো হয়।

    def do_POST(self):
        if self.path == '/blogs':
            data = self._read_json()
            conn = get_connection()
            cursor = conn.cursor() # ডাটাবেসে SQL চালানোর জন্য একটি cursor object তৈরি করা হচ্ছে।
            cursor.execute("INSERT INTO blogs (title, slug, body, image) VALUES (%s, %s, %s, %s)",
                           (data['title'], data['slug'], data.get('body'), data.get('image'))) # body, image optional হলে .get() ব্যবহার করলে error হবে না যদি না থাকে
            conn.commit()
            conn.close()
            # ✅ Console এ message print
            print(f"✅ New blog created: {data['title']}")
            self._set_headers(201)
            self.wfile.write(json.dumps({'message': f'Blog created: {data["title"]}'}).encode())

    def do_PUT(self):
        if self.path.startswith('/blogs/'):
            blog_id = int(self.path.split('/')[-1])
            # এটা শুধু server এ দেখায়, চাইলে রেখে দাও
            # print(blog_id)
            # এখন client (Postman) এ পাঠানো হবে
            # self._set_headers()
            # self.wfile.write(json.dumps({
            #     'message': 'Received blog ID',
            #     'blog_id': blog_id
            # }).encode())
            # return  # এখানে return রাখলে নিচের update query execute হবে না (শুধু ID দেখাবে)
            data = self._read_json()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE blogs SET title=%s, slug=%s, body=%s, image=%s WHERE id=%s",
                           (data['title'], data['slug'], data.get('body'), data.get('image'), blog_id))
            conn.commit()
            conn.close()
            self._set_headers()
            self.wfile.write(json.dumps({
                'message': 'Blog updated',
                'data': data
                }).encode())

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
