# Flask config file
# https://pythonise.com/series/learning-flask/flask-configuration-files

class Config(object):
    #---------------------------------
    ##General settings
    #---------------------------------
    ## Debug and testing settings not used
    ## You can remove ot use them if desired.
    DEBUG = False
    TESTING = False
    ## Secret key for sessions
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    ## User/password fields. Only use if you 
    ## don't store entire connection string
    APPDB_USERNAME = ""
    APPDB_PASSWORD = ""
    ## General app name/desc and copyright
    APP_NAME = "Flask IBM i App"
    APP_COPYRIGHT = "Mobigogo LLC"
   
    #---------------------------------
    ## Which database type to use ?
    ## ODBC to IBM i or SQLite 
    #---------------------------------
    APP_DBTYPE='SQLITE' # IBMI=Use ODBC/SQLITE=Use SQLite Database

    #---------------------------------
    # PC Connections    
    #---------------------------------  
    #Use this SQLite connection string for PC
    #APPDB_FILE = r"C:\dirname\qiws.db" # with r, don't need double \\
    APPDB_FILE = r"qiws.db" # with r, don't need double \\
    
    #Use this ODBC connection string for PC
    APP_CONNSTRING = 'Driver={Client Access ODBC Driver (32-bit)};System=IBMIHOSTIP;Uid=USERID1;Pwd=PASSWORD1;CommitMode=0;'

    #---------------------------------
    # IBM i Connections    
    #---------------------------------  
    APP_LIBRARY1='QIWS'

    #Use this SQLite connection string for Native IBM i 
    #APPDB_FILE = "/pythonmagic/qiws.db" # with r, don't need double \\
    
    #Use this ODBC connection string for Native IBM i
    ## This string uses the *LOCAL DSN on IBM i. No user/pass needed
    ## It will assume user credentials of user running the application
    #APP_CONNSTRING = 'DSN=*LOCAL;'
    ## Use DSN with specific IBMi user/password
    #APP_CONNSTRING = 'DSN=*LOCAL;UID=USERID1;PWD=PASSWORD1;'
    ## This string uses DSN-less connection with IBMi user/password
    #APP_CONNSTRING = 'Driver={IBM i Access ODBC Driver};System=localhost;Uid=USERID1;Pwd=PASSWORD1;CommitMode=0;'
    
    ## **WARNING: Enabling these settings on unsecure HTTP server will cause sessions
    ## not to work correctly so only enable if using HTTPS only.
    ## Use these 2 settings to only send cookies on HTTPS connections
    ## which should be the default for web servers now anyway.
    #https://blog.miguelgrinberg.com/post/cookie-security-for-flask-applications
    ##SESSION_COOKIE_SECURE = True
    ##REMEMBER_COOKIE_SECURE = True
    
class ProductionConfig(Config):
    pass #Use variables in main section above

class DevelopmentConfig(Config):
    pass #Use variables in main section above

class TestingConfig(Config):
    pass #Use variables in main section above
