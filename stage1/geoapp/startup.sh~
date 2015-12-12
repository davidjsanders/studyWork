#
# $portToUse is an environment variable required to set the nginx configuration
# (see below). We check the variable has been set - if it hasn't, then the
# default of 5000 is used.
#
if [ "${portToUse}x" == "x" ]; then portToUse='5000'; fi
if [ "${serverName}x" == "x" ]; then serverName='localhost'; fi
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
echo "server {" > bluetooth_uwsgi.conf
echo "    listen      ${portToUse};" >> bluetooth_uwsgi.conf
echo "    server_name ${serverName};" >> bluetooth_uwsgi.conf
echo "    charset     utf-8;" >> bluetooth_uwsgi.conf
echo "    client_max_body_size 75M;" >> bluetooth_uwsgi.conf
echo "" >> bluetooth_uwsgi.conf
echo "    location / { try_files \$uri @yourapplication; }" >> bluetooth_uwsgi.conf
echo "    location @yourapplication {" >> bluetooth_uwsgi.conf
echo "        include uwsgi_params;" >> bluetooth_uwsgi.conf
echo "        uwsgi_pass 127.0.0.1:3031;" >> bluetooth_uwsgi.conf
echo "    }" >> bluetooth_uwsgi.conf
echo "}" >> bluetooth_uwsgi.conf
#
# Start nginx
#
rm -r -f /etc/nginx/sites-enabled/default
ln -s /bluetooth/bluetooth_uwsgi.conf /etc/nginx/conf.d/bluetooth_uwsgi.conf
service nginx start
#
# Start UWSGI and pass the notes_final.ini file.
#
/flask/bin/uwsgi bluetooth_uwsgi.ini
