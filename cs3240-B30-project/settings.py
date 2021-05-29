import socket

#/***************************************************************************************
#*  REFERENCES
#*  Author: smack
#*  Date: Jan 3rd, 2017
#*  URL: https://stackoverflow.com/questions/35536491/error-youre-accessing-the-development-server-over-https-but-it-only-supports
#*
#***************************************************************************************/

if socket.gethostname() == "Thai-Laptop": #Change to your local host name
    from .local_settings import *
else:
    from .production_settings import *