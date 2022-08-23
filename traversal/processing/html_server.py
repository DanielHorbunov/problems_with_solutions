import cgi
import os
import pickle as pkl


with open(r"./data/output_data/wb_graph.pkl", "rb") as f:
    wb_graph = pkl.load(f)


from wsgiref.simple_server import make_server

START_PAGE = os.path.join(os.getcwd(), 'visualization.html')

FOLDER = os.path.join(os.getcwd(), 'stories')


class ServerApp:

    def __init__(self):

        self.commands = {
            '':             self.start,
        }

    def __call__(self, environ, start_response):

        command = environ.get('PATH_INFO', '').lstrip('/')

        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        body = None

        error = False

        if command in self.commands:

            body = self.commands[command](form)

            if body:

                start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

            else:

                error = True

        if error:

            start_response('404 NOT FOUND', [('Content-type', 'text/plain')])

            body = 'Error'

        return [bytes(body, encoding='utf-8')]

    def start(self, form=None):

        with open(START_PAGE) as f:

           lines = f.readlines()

        opt_pattern = '<option id="{k}">{v}</option>\n'

        value = '\n'.join([
            opt_pattern.format(k=vertex.get_key(), v=vertex.get_name())
            for vertex in wb_graph
        ])

        key = "{id_names}"

        for i in range(len(lines)):

            if key in lines[i]:

                lines[i] = lines[i].format(id_names=value)

        return ''.join(lines)



if __name__ == '__main__':

    print('SERVER')

    controller = ServerApp()

    server = make_server('localhost', 7777, controller)

    server.serve_forever()