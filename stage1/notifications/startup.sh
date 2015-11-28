#
# $portToUse is an environment variable required to set the nginx configuration
# (see below). We check the variable has been set - if it hasn't, then the
# default of 5000 is used.
#
if [ "${portToUse}x" == "x" ]; then portToUse='5000'; fi
#
# Debug statements - access through 'docker logs <containername>'
# For this app, that is: docker logs notesfinal<portToUse>
#
echo ""
echo "** Starting Port ${portToUse} **"
echo ""
#
# Create the nginx configuration file dynamically, so that the correct
# port number is assigned. This ensures that the port is mapped and that
# the correct URL's are returned. In addition to this step, another step
# is used in notes/resources/Config.py - there, the port number is used
# to generate full URLs as Flask was dropping the port numbers. A final
# part of this sequence is runserver.py; this is the Python program that
# is called by the UWSGI call below. It stores the environment variable
# portToUse in Config.py
#
echo "server {" > notes_final.conf
echo "    listen      ${portToUse};" >> notes_final.conf
echo "    server_name localhost;" >> notes_final.conf
echo "    charset     utf-8;" >> notes_final.conf
echo "    client_max_body_size 75M;" >> notes_final.conf
echo "" >> notes_final.conf
echo "    location / { try_files \$uri @yourapplication; }" >> notes_final.conf
echo "    location @yourapplication {" >> notes_final.conf
echo "        include uwsgi_params;" >> notes_final.conf
echo "        uwsgi_pass 127.0.0.1:3031;" >> notes_final.conf
echo "    }" >> notes_final.conf
echo "}" >> notes_final.conf
#
# Start nginx
#
service nginx start
#
# Start UWSGI and pass the notes_final.ini file.
#
/flask/bin/uwsgi notifications_uwsgi.ini
