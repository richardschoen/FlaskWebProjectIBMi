#----------------------------------------------------------
# This script runs the FlaskWebProjectIBMi application 
# using a development server.
# Don't use development server for production web apps. 
# Prod recommendation: Deploy with Gunicorn/Nginx if possible.
#----------------------------------------------------------

from os import environ
from FlaskWebProjectIBMi import app

if __name__ == '__main__':

    #Work on local PC only with localhost
    #HOST = environ.get('SERVER_HOST', 'localhost')
    #Work on all IP addresses so IP addresses can connect to our app
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '5556'))
    except ValueError:
        PORT = 5556

    #Debug=true will hot reload app, but Visual Studio debugging won't work
    ##app.run(HOST, PORT,debug=True)

    #Debug=None will not hot reload app, but Visual Studio debugging works
    #when developing in Visual Studio.
    ##app.config['SERVER_NAME'] = 'localhost.domain:5556' ## Need on prod server ??
    app.run(HOST, PORT,debug=None)
