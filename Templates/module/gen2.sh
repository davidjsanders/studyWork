destination='NONE'
name='NONE'
version='v1_00'
lName=''
error=0
#
# Usage instructions
#
usage()
{
    echo "Usage: $0 -d /absolute/path -n new-name [-h]" 1>&2
    echo
    echo "  -d [path]    Specify the destination ABSOLUTE path"
    echo "  -n [string]  Specify the name of the service to be generated"
    echo "  -v [string]  Specify the version of the service, e.g. v3_00"
    echo "  -h           Show this help message."
    echo
    exit 1; 
}
#
# Get options
#
while getopts ":v:d:n:h" param; do
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
if [[ $name == "NONE" ]]; then
    echo
    echo "Error: name (-n) is required."
    echo
    usage
fi
#
# Check destinations has been defined and does not exist.
#
if [[ $destination == "NONE" ]]; then
    echo
    echo "Error: destination (-d) is required."
    echo
    usage
fi
if [[ -d $destination/$name ]]; then
    echo
    echo "Error: Bad destination - "$destination/$name 
    echo "       Already exists and cannot be written over."
    echo
    exit 1
fi
echo "Module Generator"
echo "================"
echo
echo "Define the services in the new module."
echo "--------------------------------------"
echo
echo "Enter the services to generate. Separate each with return, end with "
echo "EOF and do NOT include extensions, e.g. .py"
service_list=$(cat)
echo
echo
echo "Define the configuration services in the new module."
echo "----------------------------------------------------"
echo
echo "Enter the config services to generate. Separate each with return, end "
echo "with EOF and do NOT include extensions, e.g. .py"
config_list=$(cat)
echo
echo
echo "About to generate new module from template."
echo "==========================================="
echo
echo "Destination:     "$destination
echo "Name:            "$name
echo "Docker Name:     "$lName
echo "Service version: "$version
echo -n "Services:        "
for file_name in $service_list
do
    echo -n $file_name"; "
done
echo
echo -n "Config Services: "
for file_name in $config_list
do
    echo -n $file_name"; "
done
echo
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
echo "Starting"
echo "--------"
echo
echo -n "1. Copy template 'en masse' to ${destination} ..."
cp -r . $destination/$name
echo "done"
echo -n "2. Remove files used only in the template ..."
rm $destination/$name/generate.sh
rm $destination/$name/__DO_NOT_EDIT*
echo "done"
echo -n "3. Rename files and folders ..."
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
echo "4. Change source code. Replace Module to $name"
echo -n "  4.1 - 's/Module\./$name\./g' ..."
find $destination/$name/ -type f -exec sed -i 's/Module\./'$name'\./g' {} +
echo "done"
echo -n "  4.2 - 's/Module\//$name\//g' ..."
find $destination/$name/ -type f -exec sed -i 's/Module\//'$name'\//g' {} +
echo "done"
echo -n "  4.3 - 's/\/Module/\/$name/g' ..."
find $destination/$name/ -type f -exec sed -i 's/\/Module/\/'$name'/g' {} +
echo "done"
echo -n "  4.4 - 's/Module\_/$name\_/g' ..."
find $destination/$name/ -type f -exec sed -i 's/Module\_/'$name'\_/g' {} +
echo "done"
echo -n "  4.5 - 's/\_module/\_$lName/g' ..."
find $destination/$name/ -type f -exec sed -i 's/\_module/\_'$lName'/g' {} +
echo "done"
echo -n "  4.6 - 's/from Module/from $name/g' ..."
find $destination/$name/ -type f -exec sed -i 's/from Module/from '$name'/g' {} +
echo "done"
echo -n "  4.7 - 's/from 'Module'/from '$name'/g' ..."
find $destination/$name/ -type f -exec sed -i "s/\'Module\'/\'"$name"\'/g" {} +
echo "done"
echo -n "  4.8 - 's/'Module'/from '$name'/g' ..."
find $destination/$name/ -type f -exec sed -i "s/'Module'/'"$name"'/g" {} +
echo "done"
echo -n "  4.9 - 's/Module_$/"$name"_$/g' ..."
find $destination/$name/ -type f -exec sed -i 's/Module\_\$/'$name'\_\$/g' {} +
echo "done"
echo -n "  4.10 - 's/module_$/"$lName"_$/g' ..."
find $destination/$name/ -type f -exec sed -i 's/module\_\$/'$lName'\_\$/g' {} +
echo "done"
echo -n "  4.11 - 's/v1_00$/"$version"_$/g' ..."
find $destination/$name/ -type f -exec sed -i 's/v1_00/'$version'/g' {} +
echo "done"
echo
echo "5. Generate services."
echo
for file_name in $service_list
do
  lower_file_name=$(echo $file_name | tr [A-Z] [a-z])
  echo "  Generating $file_name ..."
  cp Module_Boundary/Sample_Boundary.py $destination/$name/$name"_Boundary"/$file_name"_Boundary.py"
  cp Module/Sample_Control.py $destination/$name/$name/$file_name"_Control.py"
  cp Module/v1_00_Sample_Control.py $destination/$name/$name/$version"_"$file_name"_Control.py"
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
#
  echo
done
echo
echo "6. Generate config services."
echo
for file_name in $config_list
do
  lower_file_name=$(echo $file_name | tr [A-Z] [a-z])
  echo "  Generating $file_name ..."
  cp Module_Config_Boundary/Config_Sample_Boundary.py \
    $destination/$name/$name"_Config_Boundary"/$file_name"_Boundary.py"
  cp Module_Config_Control/Config_Sample_Control.py \
    $destination/$name/$name"_Config_Control"/"Config_"$file_name"_Control.py"
  cp Module_Config_Control/v1_00_Config_Sample_Control.py \
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
#
  echo
done
echo
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
