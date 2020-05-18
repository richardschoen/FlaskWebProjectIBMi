#-------------------------------------------------------
# Module: dbsqlite.py
# Desc: This module contains our database class
#-------------------------------------------------------
#
#https://www.sqlitetutorial.net/sqlite-python/
#https://www.sqlitetutorial.net/sqlite-python/create-tables/
#https://stackabuse.com/python-modules-creating-importing-and-sharing/
#https://www.w3schools.com/python/python_classes.asp
# Environment setup
# pip install --upgrade pysqlite
# pip install --upgrade pysqlite3-binary
# pip install --upgrade pysqlite3

#-------------------------------------------------------
# Class: DbSqlite
# Desc: This class is a wrapper class around SQLite DB functions
#-------------------------------------------------------
import uuid
import sqlite3
from sqlite3 import Error

class DbSqlite():
 
    # Class variables
    _dbopen=False
    _dbconn=None
    _dbfile=""

    def __init__(self,db_file=None):
        #-------------------------------------------------------
        # Function: __init__
        # Desc: Constructor
        # :param self: Object instance
        # :param db_file: File name or default to None if no file 
        #        needs to be opened yet
        # :return: Connection or None on error 
        #-------------------------------------------------------
        try:
           _dbopen=False
           _dbconn=None
           _dbfile=db_file
           if db_file != None and db_file != "":
              self.create_connection(db_file)
           else:
              print("No database name passed in. Need to create later.")
        except Error as e:
            print(e)
        finally:
            return None #Can return None or omit any return

    def isopen(self):
        #-------------------------------------------------------
        # Function: isopen
        # Desc: Check if database is open 
        # :param self: Pointer to object instance. 
        # :return: True-Db is open, False=Db is not open
        #-------------------------------------------------------
        #return DB open status
        return self._dbopen

    def getconn(self):
        #-------------------------------------------------------
        # Function: getconn
        # Desc: Get database connection object 
        # :param self: Pointer to object instance. 
        # :return: Connection value
        #-------------------------------------------------------
        #return conn object
        return self._dbconn
    
    def create_connection(self,db_file):
        #-------------------------------------------------------
        # Function: create_connection
        # Desc: Create a database connection to a SQLite database 
        # :param self: Pointer to object instance. 
        # :param db_file: SQLite database file name/path
        # :return: True-Connection open, False-No connection open 
        #-------------------------------------------------------

        #Create connection variable
        conn = None 

        #Let's try and open the database. Will auto-create if not found.
        try:
            conn = sqlite3.connect(db_file)

            #Use the row_factory to give us both index-based and case-insensitive name-based access
            #case-insensitive name-based access to columns with almost no memory overhead.
            #See this link for more info if desired: https://docs.python.org/3/library/sqlite3.html 
            #Note: If we don't use row_factory, jinja templates won't render row data using names
            conn.row_factory=sqlite3.Row #TODO - What does this do ?

            #print(sqlite3.version) #pyselite version
            #print(sqlite3.sqlite_version) #SQLLite engine version
            # Set open flag = true
            if conn != None:
               #Save open connection info internally in the class 
               self._dbopen=True 
               self._dbconn = conn
            return self._dbopen;
        except Error as e:
            print(e)
            return False

    def close_connection(self):
        #-------------------------------------------------------
        # Function: close_connection
        # Desc: Close a database connection to a SQLite database 
        # :param self: Pointer to object instance. 
        # :return: True-Success, False-Error
        #-------------------------------------------------------

        # Let's attempt to close our database connection 
        try:
            self._dbconn.close()
            #Release object. Not sure if needed or automatic ?
            conn=None
            self._dbconn=None
            return True;
        except Error as e:
            print(e)
            return False

    def execute(self,sql):
        #----------------------------------------------------------
        # Function: execute
        # Desc: Execute an SQL action query that does not return results
        # :param self: Pointer to object instance. 
        # :param sql: SQL action query
        # :return: True-Success, False-Error
        #----------------------------------------------------------
        try:
            conn1 = self._dbconn
            conn1.execute("begin") # Start transaction
            conn1.execute(sql) #Execute the action query
            conn1.execute("commit") #Commit change
            return True
        except Error as e:
            print(e)  
            self._dbconn.rollback #roll back any changes
            return False

    def execute_query(self,sql):
        #----------------------------------------------------------
        # Function: execute_query
        # Desc: Execute an SQL query that does return results
        # :param self: Pointer to object instance. 
        # :param sql: SQL query expecting results
        # :return: Resulting cursor or None on error
        #----------------------------------------------------------
        try:
            cursor1 = self._dbconn.cursor()
            cursor1.execute(sql)
            return cursor1
        except Error as e:
            print(e)  
            return None

    def insert_qcustcdt(self,cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue,library=''):
        #----------------------------------------------------------
        # Function: insert_qcustcdt
        # Desc: Insert new record into Customer Master
        # :param self: Pointer to object instance. 
        # :param field names: Each individual field name needed
        # :param library: IBMi library. Not used. Default=BLANKS. 
        #                 Left in for parm compatability with IBMi class
        # :return: Result value from query
        #----------------------------------------------------------
        try:
           # Create the SQL statement 
           sql = """insert into qcustcdt (cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue) VALUES(%s,'%s','%s','%s','%s','%s',%s,%s,%s,%s,%s)""" % (cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue)
           # Insert the record
           # Note: self parm not needed for execute when internal class function called
           rtnexecute=self.execute(sql)
           # Return result value
           return rtnexecute
        except Exception as e:
            print(e)  
            return -2 # return -2 on error 

    def update_qcustcdt(self,cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue,library=''):
        #----------------------------------------------------------
        # Function: update_qcusctdt
        # Desc: Update existing record into Customer Master 
        # :param self: Pointer to object instance. 
        # :param field names: Each individual field name needed
        # :param library: IBMi library. Not used. Default=BLANKS. 
        #                 Left in for parm compatability with IBMi class
        # :return: Result value from query
        #----------------------------------------------------------
        try:
           # Create the SQL statement 
           sql = """update qcustcdt set cusnum=%s,lstnam='%s',init='%s',street='%s',city='%s',state='%s',zipcod=%s,cdtlmt=%s,chgcod=%s,baldue=%s,cdtdue=%s where cusnum = %s""" % (cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue,cusnum)
           # Update the record. 
           # Note: self parm not needed for execute when internal class function called
           rtnexecute=self.execute(sql)
           # Return result value
           return rtnexecute
        except Exception as e:
            print(e)  
            return -2 # return -2 on error 

    def delete_qcustcdt(self,cusnum,library=''):
        #----------------------------------------------------------
        # Function: delete_qcustcdt
        # Desc: Delete record from Customer Master 
        # :param self: Pointer to object instance. 
        # :param cusnum - Customer to delete
        # :param library: IBMi library. Not used. Default=BLANKS. 
        #                 Left in for parm compatability with IBMi class
        # :return: Result value from query
        #----------------------------------------------------------
        try:
           # Create the SQL statement 
           sql = """delete from qcustcdt where cusnum=%s""" % (cusnum)
           # Delete the record
           # Note: self parm not needed for execute when internal class function called
           rtnexecute=self.execute(sql)
           # Return result value
           return rtnexecute
        except Exception as e:
            print(e)  
            return -2 # return -2 on error 

    def getexists_qcusctcdt(self,cusnum,library='qiws'):
        #----------------------------------------------------------
        # Function: getexists_qcustcdt
        # Desc: See if Customer Master record exists
        # :param self: Pointer to object instance. 
        # :param cusnum - Customer to check for
        # :param library: IBMi library. Default=qiws
        # :return: Result value from query
        #----------------------------------------------------------
        try:
           cursor=self.execute_query("select count(*) from qcustcdt where cusnum=" + cusnum)
           reccount =  cursor.fetchone()[0]
           # Return record count value from query
           return reccount
        except Exception as e:
            print(e)  
            return -2 # return -2 on error 

    def query_qcustcdt(self,wherestmt,library='qiws'):
        #----------------------------------------------------------
        # Function: query_qcustcdt
        # Desc: Query Customer Master table records with select where statement
        # :param self: Pointer to object instance. 
        # :param wherestmt - query where statement if desired
        # :param library: IBMi library. Default=qiws
        # :return: Resulting cursor or None on error
        #----------------------------------------------------------
        try:
           # Set main SQL     
           sql = "select * from qcustcdt"

           # Add WHERE statement if criteria passed
           if wherestmt!="":
              sql = sql + " WHERE " + wherestmt

           # Execute the query to get data
           cursor=self.execute_query(sql)

           # Return results cursor
           return cursor
        except Exception as e:
            print(e)
            return None
     
    def getnewguid(self):
        #----------------------------------------------------------
        # Function: getnewguid
        # Desc: Generate new GUID using the uuid1 function
        # :param self: Pointer to object instance. 
        # :return: Resulting guid or None
        #----------------------------------------------------------
        try:
           # generate the guid (uuid1)
           return uuid.uuid1()
        except Error as e:
            print(e)  
            return None
