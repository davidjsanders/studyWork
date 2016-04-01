#
# Declare parameter variables
#
destination='NONE'
name='NONE'
template='NONE'
config_file='NONE'
#
# Declare arrays
#
declare -a service_list
declare -a config_list
#
# Declare general variables
#
error=0
step_counter=0
error_text=''
version='v1_00'
lName=''
services=''
config_services=''
#
# Define functions
#
#
# show_parameters - show the parameters passed to the script
#
show_parameters()
{
    echo
    echo
    echo "Module Generator"
    echo "================"
    echo
    echo "Destination:     "$destination
    echo "Name:            "$name
    echo "Docker Name:     "$lName
    echo "Service version: "$version
    echo
}
#
# show_services - show the services detected from the config file
#
show_services()
{
    echo
    echo "Services in the new module."
    echo "---------------------------"
    for service_name in ${service_list[@]};
    do
        echo $service_name
    done
}
#
# show_config_services - show the config services detected from the config file
#
show_config_services()
{
    echo
    echo "Config services in the new module."
    echo "----------------------------------"
    for config_name in ${config_list[@]};
    do
        echo $config_name
    done
}
#
# read_config_file - Read the configuration file to detect services & config services
#
read_config_file()
{
    let service_counter=0
    let config_counter=0
    while read input_line
    do
        if [ "${input_line:0:1}" != "#" ]; then
            commands=($input_line)
            command=$(echo ${commands[0]} | tr [A-Z] [a-z])
            if [ "$command" == "route" ]; then
                service_list[$service_counter]=${commands[1]}
                let service_counter+=1
            elif [ "$command" == "config" ]; then
                config_list[$config_counter]=${commands[1]}
                let config_counter+=1
            fi
        fi
    done < $config_file
}
#
# usage - display usage instructions
#
usage()
{
    echo "Usage: mscit_gen -d path -t path -v v9_99 -c file.conf -n name [-h]" 1>&2
    echo
    echo "Required"
    echo "  -d [path]    the destination path"
    echo "  -t [path]    the path to the template"
    echo "  -n [string]  the name of the service to be generated"
    echo "  -c [path]    the configuration file"
    echo
    echo "Optional"
    echo "  -v [string]  the version of the service, e.g. v3_00"
    echo "  -h           show this help message."
    echo
    exit 1; 
}
#
# error_handler - handle specific errors
#
error_handler()
{
    echo
    echo "***"
    echo "*** Error: "$error_text
    echo "***"
    echo
    usage
}
#
# parse_parameters - parse the parameters passed to the script
#
parse_parameters()
{
    #
    # Get options
    #
    while getopts ":v:d:n:t:c:h" param; do
        case "$param" in
            n) name=$OPTARG
               check_case=$(echo ${name} | grep [A-Z])
               if [[ -z $check_case ]]; then
                   echo "Error: Name must begin with a capital letter."
                   error=1
                   break
               fi
               lName=$(echo $name | tr [A-Z] [a-z])
               ;;
            d) destination=$OPTARG
               ;;
            v) version=$OPTARG
               ;;
            t) template=$OPTARG
               ;;
            c) config_file=$OPTARG
               ;;
            h) usage
               ;;
            *) not_allowed="invalid option: -"$OPTARG
               let error_occurred=1
               break
               ;;
        esac
    done
    #
    # Check for errors
    #
    if [[ "$error" -ne "0" ]]; then
        usage
    fi
    #
    # Check name has been defined
    #
    if [ $name == "NONE" -o $destination == "NONE" -o $template == "NONE" -o $config_file == "NONE" ]; then
        error_text="Error: name (-n), destination (-d), template path (-t), and config file (-c) are required."
        error_handler
    fi
    if ! [[ -f $template/__README_FIRST__DO_NOT_EDIT__COPY_ONLY__ ]]; then
        error_text="Template file - "$template". File does not exist."
        error_handler
    fi
    if ! [[ -f $config_file ]]; then
        error_text="Configuration file - "$config_file". File does not exist."
        error_handler
    fi
    if ! [[ -d $destination ]]; then
        error_text="Bad destination - "$destination". Destination does not exist."
        error_handler
    fi
    if [[ -d $destination/$name ]]; then
        error_text="Error: Bad destination - "$destination/$name". Already exists and cannot be written over."
        error_handler
    fi
}
#
# confirm_generate - confirm the user really wants to generate the service
#
confirm_generate()
{
    echo
    read -p "Generate module? Y to continue, anything else to quit. Y/N? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Generating new module"
    else
        echo
        echo "Aborted."
        exit 1
    fi
    echo
}
#
# start_banner - show the first screen prompts
#
start_banner()
{
    echo "Starting"
    echo "--------"
    echo
}
#
# copy_template - Copy the template to the new service
#
copy_template()
{
    echo -n " "$step_counter". Copy template 'en masse' to ${destination} ..."
    cp -r $template/ $destination/$name
    echo "done"
}
#
# rm_files - Remove files only used by the generator but copied in step 1
#
rm_files()
{
    echo -n " "$step_counter". Remove files used only in the template ..."
    rm $destination/$name/mscit_gen*.sh
    rm $destination/$name/__README_FIRST__DO_NOT_EDIT*
    rm -r $destination/$name/*.old
    rm -r $destination/$name/*~
    echo "done"
}
#
# rename_files - Change the file names to the new module name
#
rename_files()
{
    echo -n " "$step_counter". Rename files and folders ..."
    mv $destination/$name/Module $destination/$name/$name
    mv $destination/$name/Module_Boundary $destination/$name/$name"_Boundary"
    mv $destination/$name/Module_Config_Boundary \
          $destination/$name/$name"_Config_Boundary"
    mv $destination/$name/Module_Config_Control \
          $destination/$name/$name"_Config_Control"
    mv $destination/$name/$name/Module_Database.py \
          $destination/$name/$name/$name"_Database.py"
    mv $destination/$name/$name/v1_00_Module_Database.py \
          $destination/$name/$name/"v1_00_"$name"_Database.py"
    echo "done"
}
#
# change_source - modify the original source code
#
change_source()
{
    echo " "$step_counter". Change source code. Replace Module to $name"
    echo -n "   "$step_counter".1 - 's/Module\./$name\./g' ..."
    find $destination/$name/ -type f -exec sed -i 's/Module\./'$name'\./g' {} +
    echo "done"
    echo -n "   "$step_counter".2 - 's/Module\//$name\//g' ..."
    find $destination/$name/ -type f -exec sed -i 's/Module\//'$name'\//g' {} +
    echo "done"
    echo -n "   "$step_counter".3 - 's/\/Module/\/$name/g' ..."
    find $destination/$name/ -type f -exec sed -i 's/\/Module/\/'$name'/g' {} +
    echo "done"
    echo -n "   "$step_counter".4 - 's/Module\_/$name\_/g' ..."
    find $destination/$name/ -type f -exec sed -i 's/Module\_/'$name'\_/g' {} +
    echo "done"
    echo -n "   "$step_counter".5 - 's/\_module/\_$lName/g' ..."
    find $destination/$name/ -type f -exec sed -i 's/\_module/\_'$lName'/g' {} +
    echo "done"
    echo -n "   "$step_counter".6 - 's/from Module/from $name/g' ..."
    find $destination/$name/ -type f -exec sed -i 's/from Module/from '$name'/g' {} +
    echo "done"
    echo -n "   "$step_counter".7 - 's/from 'Module'/from '$name'/g' ..."
    find $destination/$name/ -type f -exec sed -i "s/\'Module\'/\'"$name"\'/g" {} +
    echo "done"
    echo -n "   "$step_counter".8 - 's/'Module'/from '$name'/g' ..."
    find $destination/$name/ -type f -exec sed -i "s/'Module'/'"$name"'/g" {} +
    echo "done"
    echo -n "   "$step_counter".9 - 's/Module_$/"$name"_$/g' ..."
    find $destination/$name/ -type f -exec sed -i 's/Module\_\$/'$name'\_\$/g' {} +
    echo "done"
    echo -n "   "$step_counter".10 - 's/module_$/"$lName"_$/g' ..."
    find $destination/$name/ -type f -exec sed -i 's/module\_\$/'$lName'\_\$/g' {} +
    echo "done"
    echo -n "   "$step_counter".11 - 's/v1_00$/"$version"_$/g' ..."
    find $destination/$name/ -type f -exec sed -i 's/v1_00/'$version'/g' {} +
    echo "done"
    if [ "$version" != "v1_00" ]; then
        echo -n "   "$step_counter".12 - Modify base version numbers ..."
        mv $destination/$name/$name/v1_00_Control.py $destination/$name/$name/$version"_Control.py"
        mv $destination/$name/$name/v1_00_Sample_Control.py $destination/$name/$name/$version"_Sample_Control.py"
        mv $destination/$name/$name/v1_00_Test_Database.py $destination/$name/$name/$version"_Test_Database.py"
        mv $destination/$name/$name"_Config_Control/v1_00_Config_Logger_Control.py" \
          $destination/$name/$name"_Config_Control/"$version"_Config_Logger_Control.py"
        mv $destination/$name/$name"_Config_Control/v1_00_Config_Sample_Control.py" \
          $destination/$name/$name"_Config_Control/"$version"_Config_Sample_Control.py"
        echo "done"
    fi
}
#
# generate_services - generate the services identified in the config file
#
generate_services()
{
    echo " "$step_counter". Generate services."
    for file_name in ${service_list[@]}
    do
      lower_file_name=$(echo $file_name | tr [A-Z] [a-z])
      echo "  Generating $file_name ..."
      cp $template/Module_Boundary/Sample_Boundary.py $destination/$name/$name"_Boundary"/$file_name"_Boundary.py"
      cp $template/Module/Sample_Control.py $destination/$name/$name/$file_name"_Control.py"
      cp $template/Module/v1_00_Sample_Control.py $destination/$name/$name/$version"_"$file_name"_Control.py"
    #
    # Modify service boundary
    #
      echo -n "    Modifying "$file_name"_Boundary.py ..."
      find $destination/$name/$name"_Boundary"/$file_name"_Boundary.py" \
         -type f -exec sed -i 's/Sample_Boundary/'$file_name'_Boundary/g' {} +
      find $destination/$name/$name"_Boundary"/$file_name"_Boundary.py" \
         -type f -exec sed -i 's/sample_control_object/'$lower_file_name'_control_object/g' {} +
      find $destination/$name/$name"_Boundary"/$file_name"_Boundary.py" \
         -type f -exec sed -i 's/Sample_Control/'$file_name'_Control/g' {} +
      find $destination/$name/$name"_Boundary"/$file_name"_Boundary.py" \
         -type f -exec sed -i 's/Module\./'$name'\./g' {} +
      echo "done"
    #
      echo >> $destination/$name/$name"_Boundary/main.py"
      echo "### Generated path for service: "$file_name \
         >> $destination/$name/$name"_Boundary/main.py"
      echo "from "$name"_Boundary."$file_name"_Boundary import "$file_name"_Boundary" \
         >> $destination/$name/$name"_Boundary/main.py"
      echo "api.add_resource("$file_name"_Boundary, '/{0}/"$lower_file_name"'.format(version))" \
         >> $destination/$name/$name"_Boundary/main.py"
    #
      echo >> $destination/$name/Dockerfile
      echo "### Generated Boundary for service: "$file_name >> $destination/$name/Dockerfile
      echo "COPY "$name"_Boundary"/$file_name"_Boundary.py /"$name"/"$name"_Boundary/" \
         >> $destination/$name/Dockerfile
    #
    # Modify service control
    #
      echo -n "    Modifying "$file_name"_Control.py ..."
      find $destination/$name/$name/$file_name"_Control.py" \
         -type f -exec sed -i 's/Module/'$name'/g' {} +
      find $destination/$name/$name/$file_name"_Control.py" \
         -type f -exec sed -i 's/v1_00/'$version'/g' {} +
      find $destination/$name/$name/$file_name"_Control.py" \
         -type f -exec sed -i 's/Sample_Control/'$file_name'_Control/g' {} +
      find $destination/$name/$name/$file_name"_Control.py" \
         -type f -exec sed -i 's/sample_control_object/'$lower_file_name'_control_object/g' {} +
      echo >> $destination/$name/Dockerfile
      echo "### Generated Control for service: "$file_name >> $destination/$name/Dockerfile
      echo "COPY "$name/$file_name"_Control.py /"$name"/"$name"/" \
         >> $destination/$name/Dockerfile
      echo "done"
    #
    # Modify service control version
    #
      echo -n "    Modifying "$version"_"$file_name"_Control.py ..."
      find $destination/$name/$name/$version"_"$file_name"_Control.py" \
         -type f -exec sed -i "s/'Module'/'"$file_name"'/g" {} +
      find $destination/$name/$name/$version"_"$file_name"_Control.py" \
         -type f -exec sed -i 's/Module/'$name'/g' {} +
      find $destination/$name/$name/$version"_"$file_name"_Control.py" \
         -type f -exec sed -i 's/v1_00/'$version'/g' {} +
      find $destination/$name/$name/$version"_"$file_name"_Control.py" \
         -type f -exec sed -i 's/Sample_Control/'$file_name'_Control/g' {} +
      echo >> $destination/$name/Dockerfile
      echo "### Generated Control for service: "$version"_"$file_name >> $destination/$name/Dockerfile
      echo "COPY "$name/$version"_"$file_name"_Control.py /"$name"/"$name"/" \
         >> $destination/$name/Dockerfile
      echo "done"
    done
}
#
# generate_config - generate the config routes specified in the config file
#
generate_config()
{
    echo " "$step_counter". Generate config services."
    for file_name in ${config_list[@]}
    do
      lower_file_name=$(echo $file_name | tr [A-Z] [a-z])
      echo "  Generating $file_name ..."
      cp $template/Module_Config_Boundary/Config_Sample_Boundary.py \
        $destination/$name/$name"_Config_Boundary"/$file_name"_Boundary.py"
      cp $template/Module_Config_Control/Config_Sample_Control.py \
        $destination/$name/$name"_Config_Control"/"Config_"$file_name"_Control.py"
      cp $template/Module_Config_Control/v1_00_Config_Sample_Control.py \
        $destination/$name/$name"_Config_Control"/$version"_Config_"$file_name"_Control.py"
    #
    # Modify service boundary
    #
      echo -n "    Modifying "$file_name"_Boundary.py ..."
      find $destination/$name/$name"_Config_Boundary"/$file_name"_Boundary.py" \
         -type f -exec sed -i 's/Sample_Boundary/'$file_name'_Boundary/g' {} +
      find $destination/$name/$name"_Config_Boundary"/$file_name"_Boundary.py" \
         -type f -exec sed -i 's/sample_control_object/'$lower_file_name'_control_object/g' {} +
      find $destination/$name/$name"_Config_Boundary"/$file_name"_Boundary.py" \
         -type f -exec sed -i 's/Sample_Control/'$file_name'_Control/g' {} +
      find $destination/$name/$name"_Config_Boundary"/$file_name"_Boundary.py" \
         -type f -exec sed -i 's/Module/'$name'/g' {} +
      echo "done"
    #
      echo >> $destination/$name/$name"_Config_Boundary/main.py"
      echo "### Generated path for service: "$file_name \
         >> $destination/$name/$name"_Config_Boundary/main.py"
      echo "from "$name"_Config_Boundary."$file_name"_Boundary import Config_"$file_name"_Boundary" \
         >> $destination/$name/$name"_Config_Boundary/main.py"
      echo "api.add_resource(Config_"$file_name"_Boundary, '/{0}/config/"$lower_file_name"'.format(version))" \
         >> $destination/$name/$name"_Config_Boundary/main.py"
    #
      echo >> $destination/$name/Dockerfile
      echo "### Generated Config Boundary for service: "$file_name >> $destination/$name/Dockerfile
      echo "COPY "$name"_Config_Boundary"/$file_name"_Boundary.py /"$name"/"$name"_Config_Boundary/" \
         >> $destination/$name/Dockerfile
    #
    # Modify service control
    #
      echo -n "    Modifying "$file_name"_Control.py ..."
      find $destination/$name/$name"_Config_Control"/"Config_"$file_name"_Control.py" \
         -type f -exec sed -i 's/Module/'$name'/g' {} +
      find $destination/$name/$name"_Config_Control"/"Config_"$file_name"_Control.py" \
         -type f -exec sed -i 's/v1_00/'$version'/g' {} +
      find $destination/$name/$name"_Config_Control"/"Config_"$file_name"_Control.py" \
         -type f -exec sed -i 's/Sample_Control/'$file_name'_Control/g' {} +
      find $destination/$name/$name"_Config_Control"/"Config_"$file_name"_Control.py" \
         -type f -exec sed -i 's/sample_control_object/'$lower_file_name'_control_object/g' {} +
    #
      echo >> $destination/$name/Dockerfile
      echo "### Generated Config Control for service: "$file_name >> $destination/$name/Dockerfile
      echo "COPY "$name"_Config_Control"/"Config_"$file_name"_Control.py /"$name"/"$name"_Config_Control/" \
         >> $destination/$name/Dockerfile
      echo "done"
    #
    # Modify service control version
    #
      echo -n "    Modifying "$version"_"$file_name"_Control.py ..."
      find $destination/$name/$name"_Config_Control"/$version"_Config_"$file_name"_Control.py" \
         -type f -exec sed -i "s/'Module'/'"$file_name"'/g" {} +
      find $destination/$name/$name"_Config_Control"/$version"_Config_"$file_name"_Control.py" \
         -type f -exec sed -i 's/Module/'$name'/g' {} +
      find $destination/$name/$name"_Config_Control"/$version"_Config_"$file_name"_Control.py" \
         -type f -exec sed -i 's/v1_00/'$version'/g' {} +
      find $destination/$name/$name"_Config_Control"/$version"_Config_"$file_name"_Control.py" \
         -type f -exec sed -i 's/Sample_Control/'$file_name'_Control/g' {} +
    #
      echo >> $destination/$name/Dockerfile
      echo "### Generated Config Control for service: "$version"_"$file_name >> $destination/$name/Dockerfile
      echo "COPY "$name"_Config_Control"/$version"_Config_"$file_name"_Control.py /"$name"/"$name"_Config_Control/" \
         >> $destination/$name/Dockerfile
      echo "done"
    done
}
#
# end_banner - show the final screen prompts
#
end_banner()
{
    echo 
    echo "Complete. Service has been generated"
    echo "  Build the service with:      ./build.sh"
    echo "  Run the service with:        ./debug.sh"
    echo "  Push the service to the hub: ./push.sh"
    echo
    echo "After completion, change directory to the new service"
    echo "  cd $destination/$name"
    echo
    echo "Done."
}
#
# Program Start
#
parse_parameters $@
read_config_file
show_parameters
show_services
show_config_services
confirm_generate
#
# Build process
#
start_banner
#
let step_counter+=1
copy_template
#
let step_counter+=1
rm_files
#
let step_counter+=1
rename_files
#
let step_counter+=1
change_source
#
let step_counter+=1
generate_services
#
let step_counter+=1
generate_config
#
let step_counter+=1
end_banner
#
# Program End
#

