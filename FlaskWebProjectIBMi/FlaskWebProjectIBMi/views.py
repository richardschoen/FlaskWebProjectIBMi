#--------------------------------------------------------------------------
# Module: views.py
# Desc: Routes and views for the flask application.
#--------------------------------------------------------------------------
import json
import collections
import sys
from sys import platform
import os
import time
import traceback
from datetime import datetime
from flask import render_template
from dbibmi import DbIbmi
from dbsqlite import DbSqlite
from FlaskWebProjectIBMi import * 

#--------------------------------------------------------------------------
#Define app level work variables - if any
#--------------------------------------------------------------------------
#Load system config settings into variables
appname=app.config["APP_NAME"]
appcopyright=app.config["APP_COPYRIGHT"] 
connstring = app.config["APP_CONNSTRING"] #IBMi ODBC connection string
library1=app.config["APP_LIBRARY1"] #IBMi Data Library 
appdbfile=app.config["APPDB_FILE"] #sqlite file name
appdbtype=app.config["APP_DBTYPE"] #Database type IBMI/SQLITE

#--------------------------------------------------------------------------
#Define our web app routes
#--------------------------------------------------------------------------

# NOTE - DO NOT connect to database at this level. After initialization
# only the specific routes are called. Connect to DB each time a route is 
# is executed

#--------------------------------------------------------------------------
# TODO - Decide how to best use before_request and after_request if at all
# Run this code before any route code. Ex: Open database connection 
# https://pythonise.com/series/learning-flask/python-before-after-request
#--------------------------------------------------------------------------
#@app.before_request
#def before_request_func():
#
    # Connect to database 
#    db=DbIbmi(app.config["APPDB_FILE"])

#--------------------------------------------------------------------------
# Run this code after any route code. Ex: CLose database connection 
#--------------------------------------------------------------------------
#@app.after_request
#def after_request_func():
#
#    # Close database connection
#    db.close_connection()

#--------------------------------------------------------------------------
# Home route/index page
#--------------------------------------------------------------------------
@app.route('/')
@app.route('/home',methods=["GET", "POST"])
def home():

    """Renders the home page."""
    return render_template(
           'index.html',
            title='Home Page',
            year=datetime.now().year,
            appname = appname,
            appcopyright = appcopyright,

    )

#--------------------------------------------------------------------------
# Render the Contact page/view
#--------------------------------------------------------------------------
@app.route('/contact')
def contact():

    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message1='Your contact page.',
        appname = appname,
        appcopyright = appcopyright,
    )

#--------------------------------------------------------------------------
# Render the about page/view
#--------------------------------------------------------------------------
@app.route('/about')
def about():
    
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message1='Your application description page.',
        appname = appname,
        appcopyright = appcopyright,
    )

#--------------------------------------------------------------------------
# Render the dashboard view
#--------------------------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    
    return render_template(
        'dashboard.html',
        title='Dashboard',
        year=datetime.now().year,
        message1='Dashboard page.',
        appcopyright = appcopyright,
        appname = appname,
    )

#--------------------------------------------------------------------------
# Render the charts view
#--------------------------------------------------------------------------
@app.route('/charts')
def charts():
    
    return render_template(
        'charts.html',
        title='Charts',
        year=datetime.now().year,
        message1='Charts page.',
        appcopyright = appcopyright,
        appname = appname,
    )

#--------------------------------------------------------------------------
# Render the login page
#--------------------------------------------------------------------------
@app.route('/login')
def login():
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
        message1='Your application login page.',
        appname = appname,
        appcopyright = appcopyright,
    )

#--------------------------------------------------------------------------
#Renders customer detail page
#--------------------------------------------------------------------------
@app.route('/qcustcdtdetail',methods=["GET", "POST"])
def qcustcdtdetail():

    # Connect to database 
    if appdbtype=="IBMI":
      db=DbIbmi(connstring)
    else:
      db=DbSqlite(appdbfile)

    results=None

    #If the form was posted, do query
    if request.method == 'GET':
        #Get the org number and last name filters from form
        icusnum = request.args.get('icusnum')

        #If no org number parm. New Record, show empty form
        if icusnum == None:
            flash('New Customer')

            # successful query display results
            return render_template('qcustcdtdetail.html',
                         title='Customer Master Detail',
                         year=datetime.now().year,
                         message1='Enter information for a new Org',
                         appname = appname,
                         appcopyright = appcopyright,
                         results=results)

        #Org number entered
        elif icusnum != '':
           cursor=db.query_qcustcdt("cusnum=" + icusnum,library1)
           results=cursor.fetchall()
        #If no results, redirect to customer list page       
        if not results:
            flash('No results found!')
            session.modified = True
            return redirect('/qcustcdtlist')
        else:
            # successful query display results
            return render_template('qcustcdtdetail.html',
                         title='Customer Master Detail',
                         year=datetime.now().year,
                         message1='This page contains customer detail information.',
                         appname = appname,
                         appcopyright = appcopyright,
                         results=results)
    elif request.method == 'POST':
        # display customer list results. No data
            return render_template('qcustcdtdetail.html',
                 title='Customer Master Detail',
                 year=datetime.now().year,
                 message1='Customer Master Detail page. No results',
                 appname = appname,
                 appcopyright = appcopyright,
                 results=results)

    # Close connection
    db.close_connection 

#--------------------------------------------------------------------------
#Updates org master data after post
#--------------------------------------------------------------------------
@app.route('/qcustcdtupdate',methods=["POST"])
def qcustcdtupdate():

    # Connect to database 
    if appdbtype=="IBMI":
      db=DbIbmi(connstring)
    else:
      db=DbSqlite(appdbfile)

    results=None

    #If the form was posted, do insert or update to database
    if request.method == 'POST':

        #Get the data entry fields from the form
        action=request.form['action']
        cusnum=request.form['cusnum']
        lstnam=request.form['lstnam']
        init=request.form['init']
        street=request.form['street']
        city=request.form['city']
        state=request.form['state']
        zipcod=request.form['zipcod']
        cdtlmt=request.form['cdtlmt']
        chgcod=request.form['chgcod']
        baldue=request.form['baldue']
        cdtdue=request.form['cdtdue']

        #Query to see if org exists
        if cusnum != '':
           reccount =  db.getexists_qcusctcdt(cusnum)

        #If no record, let's go ahead and insert   
        if action=='Insert' and reccount < 1:
           rtninsert=db.insert_qcustcdt(cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue,library1)
           if rtninsert:
              flash('Customer %s inserted' % cusnum)
              return redirect(url_for('qcustcdtlist')) 
           else:
              flash('Customer %s NOT inserted' % cusnum)
              return redirect(url_for('qcustcdtlist')) 
        elif action=='Insert' and reccount >= 1:
           flash('Customer number %s exists in %s records. Cannot be inserted.' % (cusnum,reccount))
           return redirect(url_for('qcustcdtlist')) 
        #Let user know if we found more than 1 matching record. Can't update or delete
        elif reccount > 1: 
           flash('Customer number %s exists in %s records. Cannot be updated.' % (cusnum,reccount))
           return redirect(url_for('qcustcdtlist')) 
        #If record found, update or delete
        elif reccount == 1:
           #Update selected, so update the record
           if action == "Update":
              rtnupd=db.update_qcustcdt(cusnum,lstnam,init,street,city,state,zipcod,cdtlmt,chgcod,baldue,cdtdue,library1)
              #flash('Org %s updated' % orguuid)
              if rtnupd:
                 flash('Customer %s updated' % cusnum)
                 return redirect(url_for('qcustcdtlist')) 
              else:
                 flash('Customer %s NOT updated' % cusnum)
                 return redirect(url_for('qcustcdtlist')) 
           #Update selected, so update the record 
           elif action == "Delete":
              #Delete the record now
              rtndel=db.delete_qcustcdt(cusnum,library1)
              if rtndel:
                 flash('Customer %s deleted' % cusnum)
                 return redirect(url_for('qcustcdtlist')) 
              else:
                 flash('Customer %s NOT deleted' % cusnum)
                 return redirect(url_for('qcustcdtlist')) 

    # Close connection
    db.close_connection 

#--------------------------------------------------------------------------
# Renders the Customer list page
#--------------------------------------------------------------------------
@app.route('/qcustcdtlist',methods=["GET", "POST"])
def qcustcdtlist():

    # Connect to database 
    if appdbtype=="IBMI":
      db=DbIbmi(connstring)
    else:
      db=DbSqlite(appdbfile)

    results=None #init query results

    #If the form was posted, do query
    if request.method == 'POST':
        #Get the customer number and last name filters from form
        icusnum = request.form['icusnum']
        ilstnam = request.form['ilstnam']
        #Get a db cursor - not needed with sqlite class
        #cursor = conn.cursor()
        #Customer number entered
        if icusnum != '':
           # Query project table
           cursor=db.query_qcustcdt("cusnum=" + icusnum)
           results=cursor.fetchall()
        #Custome last name entered
        elif ilstnam != '':
           cursor=db.query_qcustcdt("lstnam like '" + ilstnam + "'")
           results=cursor.fetchall()
        #Query filter parameters blank, show all (IE: No customer or name passed in)
        else:
           cursor=db.query_qcustcdt("")
           results=cursor.fetchall()
        #If no results, redirect to customer list page       
        if not results:
            flash('No results found!')
            session.modified=True
            ## No flash message if doing redirect ?
            return redirect(url_for('qcustcdtlist')) 
        else:
            # successful query display results
            return render_template('qcustcdtlist.html',
                         title='Customer Master',
                         year=datetime.now().year,
                         message1='',
                         appname = appname,
                         appcopyright = appcopyright,
                         results=results)
    elif request.method == 'GET':

            # display customer list results.
            return render_template('qcustcdtlist.html',
                         title='Customer Master',
                         year=datetime.now().year,
                         message1='',
                         appname = appname,
                         appcopyright = appcopyright,
                         results=results)
    # Close connection
    db.close_connection 
#--------------------------------------------------------------------------
# Renders the Customer list page as JSON
# https://anthonydebarros.com/2012/03/11/generate-json-from-sql-using-python/
#--------------------------------------------------------------------------
@app.route('/api/qcustcdtlist',methods=["GET", "POST"])
def qcustcdtlistjson():

    # Connect to database 
    if appdbtype=="IBMI":
      db=DbIbmi(connstring)
    else:
      db=DbSqlite(appdbfile)

    results=None #init query results

    #Query filter parameters blank, show all (IE: No customer or name passed in)
    cursor=db.query_qcustcdt("")
    results=cursor.fetchall()

    # Convert query to row arrays
    # Numeric fields need to be converted to strings
    rowarray_list = []
    for row in results:
        t = (str(row.CUSNUM), row.LSTNAM, row.INIT, row.STREET, 
              row.CITY, row.STATE,str(row.ZIPCOD),str(row.CDTLMT),
              str(row.CHGCOD),str(row.BALDUE),str(row.CDTDUE))
        rowarray_list.append(t)
 
    #Use jsonify to convert array list to JSON list and return 
    return jsonify(rowarray_list) 
    
    #Dump JSON row array
    #j = json.dumps(rowarray_list)
    #return j 

    # Close connection
    db.close_connection 
#--------------------------------------------------------------------------
# Renders the Data Tables customer list
#--------------------------------------------------------------------------
@app.route('/tables',methods=["GET", "POST"])
def tables():

    # Connect to database 
    if appdbtype=="IBMI":
      db=DbIbmi(connstring)
    else:
      db=DbSqlite(appdbfile)

    results=None #init query results

    #If the form was posted, do query
    if request.method == 'POST':
        #Get the customer number and last name filters from form
        icusnum = request.form['icusnum']
        ilstnam = request.form['ilstnam']
        #Get a db cursor - not needed with sqlite class
        #cursor = conn.cursor()
        #Customer number entered
        if icusnum != '':
           # Query project table
           cursor=db.query_qcustcdt("cusnum=" + icusnum)
           results=cursor.fetchall()
        #Custome last name entered
        elif ilstnam != '':
           cursor=db.query_qcustcdt("lstnam like '" + ilstnam + "'")
           results=cursor.fetchall()
        #Query filter parameters blank, show all (IE: No customer or name passed in)
        else:
           cursor=db.query_qcustcdt("")
           results=cursor.fetchall()
        #If no results, redirect to customer list page       
        if not results:
            flash('No results found!')
            return redirect('/tables')
        else:
            # successful query display results
            return render_template('tables.html',
                         title='Customer Master DataTables Example',
                         year=datetime.now().year,
                         message1='',
                         appname = appname,
                         appcopyright = appcopyright,
                         results=results)
    elif request.method == 'GET':
  
            #query all records for data table
            cursor=db.query_qcustcdt("")
            results=cursor.fetchall()
            
            # display customer list results.
            return render_template('tables.html',
                         title='Customer Master DataTables Example',
                         year=datetime.now().year,
                         message1='',
                         appname = appname,
                         appcopyright = appcopyright,
                         results=results)
    # Close connection
    db.close_connection 

#--------------------------------------------------------------------------
# Our custom 404 error handler route
#--------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    # Return page 
    return render_template(
        '404.html',
        title='',
        year=datetime.now().year,
        message1=e,
        appname = appname,
        appcopyright = appcopyright,
    )  

#--------------------------------------------------------------------------
# Our custom 401 error handler route
#--------------------------------------------------------------------------
@app.errorhandler(401)
def page_not_found(e):
    # Return page 
    return render_template(
        '401.html',
        title='',
        year=datetime.now().year,
        message1=e,
        appname = appname,
        appcopyright = appcopyright,
    )  
#--------------------------------------------------------------------------
# Our custom 500 error handler route
#--------------------------------------------------------------------------
@app.errorhandler(500)
def page_not_found(e):
    # Return page 
    return render_template(
        '500.html',
        title='',
        year=datetime.now().year,
        message1=e,
        appname = appname,
        appcopyright = appcopyright,
    )  

