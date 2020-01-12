# Developing Django Web applications

The latest [Django](https://www.djangoproject.com/) version for python-based web framework development with the adminLTE web dashboard is pre-installed.

A complete Django instruction guide is planned (the current version of Yocto works with Django properly).

## Short notes of the usage of Django with *rsYocto*

**Please follow the [official Django getting started tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/)**.

Use *Visual Studio Code Insider* as remote Django development IDE.

**Note:** Consider that Django 3.01 requires Python 3.0 -> Use allways "*python3* ..."

### Access Django application with a web browser
* By default is the Django web server only reachable internally by the embedded linux
* To access Django applications within your network do following steps:
  1. Open the Django project settings (*settings.py*) and allow every with following lines:
    ````python
    ALLOWED_HOSTS = [
     '*'
   ]
   ````
  2. Use the next command to start the web server (here on Port 8181)
  ````bash
   python3 manage.py runserver 0:8181
  ````
  * **Note:** The default port 8080 is used by the apache web server
  
  
### Access the FPGA fabric within a Django web application
* Import `subprocess.calls`to your Django project
  ````python
  from subprocess import call
  ````
* Write the FPGA fabric with following python line:
  ````python
  success = call('FPGA-writeBridge -lw 20 -b 7 1 -b', shell=True)
  ````
