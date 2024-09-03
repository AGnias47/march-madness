# From https://stackoverflow.com/a/38943785/8728749

from waitress import serve

from mmsite.wsgi import application

if __name__ == "__main__":
    serve(application, port="8000")