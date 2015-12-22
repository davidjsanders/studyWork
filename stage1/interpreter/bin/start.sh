#
# Check to see crucial environment variables are set. Set to defaults if needed
#
if [ "${ipaddr}x" == "x" ]; then ipaddr=127.0.0.1; fi
if [ "${hostname}x" == "x" ]; then hostname='localhost'; fi
#
# Add to hosts
#
echo "${ipaddr}     ${hostname}" >> /etc/hosts
#
# Run the Interpreter
#
if [ "${serverName}x" == "x" ]; then command_arg=""; else command_arg="server ${serverName}"; fi
/flask/bin/python3 interpreter.py "$command_arg"

