# FlaskWebProjectIBMi
Sample Python Flask App for use on IBM i, Windows or Linux. Uses IBM i Access ODBC Driver or SQLite Database.

# Webinar youtube link from Magic session

https://www.youtube.com/watch?v=k8IrBGebfvo&t=122s

# Setting up for development and use from Windows with Visual Studio
Install Visual Studio 2019

Clone project to local directory from Windows command line (or your favorite method)

```
cd /

git clone https://github.com/richardschoen/FlaskWebProjectIBMi.git

```

Open ***FlaskWebProjectIBMi.sln*** project solution in Visual Studio. 

Run the project and it should execute by default with the included SQLite database table.

# Setting up for development and use natively on IBM i 
Make sure IBM i ACS Open Source Package Management loaded

Install Python and Unix ODBC Yum packages via ACS or via yum commands
```
yum install unixODBC

yum install unixODBC'devel

yum install python3
```

Make sure IBM i Access ODBC Driver for PASE is loaded. Instructions on new Yum installer for ODBC driver:
https://www.seidengroup.com/2022/07/11/using-yum-to-install-or-update-the-ibm-i-odbc-driver/


From IBM i bash shell or QSH, run following commands to clone the web project:

```
cd /

git clone https://github.com/richardschoen/FlaskWebProjectIBMi.git
```

Run project with Python test server
```
cd /gitrepos/FlaskWebProjectIBMi/FlaskWebProjectIBMi

python3 runserver.py
```

If any Python packages are missing, use pip3 to install them.
```
pip3 install pyodbc

pip3 install flask

pip3 install pysqlite3
```

