from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from db_io import *


def input_restaurant(purpose="added", value="Create"):
    return '''
        <form method='POST' enctype='multipart/form-data'>
            <h2>Enter the name of the restaurant to be {purpose}</h2>
                <input name="restaurant_name" type="text" >
                <input type="submit" value="{value}"> 
        </form>'''.format(purpose=purpose, value=value)


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                _id = self.path.split("/")[-2]
                name = restaurant_id2name(_id)
                output = "<h3>This page is to edit %s</h3>" % name
                output += input_restaurant("updated", "Rename")
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                _id = self.path.split("/")[-2]
                name = restaurant_id2name(_id)
                output = "<h3>Are you sure you want to delete %s</h3>" % name
                output += '''
                <form method='POST' enctype='multipart/form-data'>
                    <input type="submit" value="Delete"> 
                </form>
                '''
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                for doc in session.query(Restaurant).all():
                    output += "<div><font size=4>" + doc.name + "</font><br>"
                    restaurant_id = str(restaurant_name2id(doc.name))
                    output += "<a href='/restaurants/" + restaurant_id + "/edit'>Edit</a><br>"
                    output += "<a href=/restaurants/" + restaurant_id + "/delete>Delete</a>"
                    output += "</div><br><br>"
                output += '''
                <a href=/restaurants/new>Add New Restaurant</a>
                '''
                output += "</body></html>"
                self.wfile.write(output)

                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"

                output += input_restaurant()
                output += '''
                <a href=/restaurants>Back to all Restaurant</a>
                '''
                output += "</body></html>"
                self.wfile.write(output)
                return



        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                # self.send_response(301)
                # self.send_header('Content-type', 'text/html')
                # self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')

                # output = ""
                # output += "<html><body>"
                # output += input_restaurant()
                # output += " <h4> The last restaurant added: </h4>"
                # output += "<h3> %s </h3>" % messagecontent[0]
                # output += '''
                #     <a href=/restaurants>Back to all Restaurant</a>
                #     '''
                # output += "</body></html>"

                InsertRestaurant(messagecontent[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                # self.wfile.write(output)

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')

                _id = self.path.split("/")[-2]
                RenameRestaurant(_id, messagecontent[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                _id = self.path.split("/")[-2]
                DeleteRestaurant(_id)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        except Exception as e:
            print(e)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()