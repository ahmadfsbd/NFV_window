#!/bin/bash
counter=0
line=''
<<<<<<< HEAD
check_power_status()
{   echo "================ Checking Power status of nOdes ========================"
    echo "================ Checking Power status of nOdes ========================">> node_clean.log
  output=$(ironic node-show "($1)")
  echo "$output"
  power_status=$(echo "$output" | awk -F "|" '/power status/ {print $1}')
  echo "$power_statust"
  echo "$power_status" >> node_clean.log
  counter=$(($counter+1))
  if [ $1='power on' ]
  then
    echo "Node $counter is ON"
  else
    echo "Node $counter is OFF"
  fi
  echo "============================================================================================================="
  echo "=============================================================================================================" >> node_clean.log
}

=======
>>>>>>> 3fd1fb1ae0525ebe7ded70c66b69700457aeb1ee
setting_Maintenance()
{   echo "================ Setting Node Maintenanace MOde to True ========================"
    echo "================ Setting Node Maintenanace MOde to True ========================">> node_clean.log
  output=$(ironic node-set-maintenance "($1)" true)
  echo "$output"
  echo "$output" >> node_clean.log
  echo "============================================================================================================="
  echo "=============================================================================================================" >> node_clean.log
}

deleting_node()
{   echo "================ Deleting Nodes ========================"
    echo "================ Deleting Nodes ========================">> node_clean.log
  output=$(ironic node-delete "($1)")
  echo "$output"
  echo "$output" >> node_clean.log
  echo "============================================================================================================="
  echo "=============================================================================================================" >> node_clean.log
}

echo "================================ Node Clean Log File =====================" > node_clean.log
output=$(ironic node-list)
node_uuids=$(echo "$output" | awk -F "|" '/-/ { print $1}')
<<<<<<< HEAD
power_status=$(echo "$output" | awk -F "|" '/-/ { print $1}')
echo "$node_uuids" > node_uuid_list.txt
echo "$power_status" > node_power_status.txt
#=============maintenanace and deletion==========
filename="node_uuid_list.txt"
while read -r line; do
#  setting_Maintenance $line
#  deleting_node $line
   echo "Node uuid is $line"
done < "$filename"

#=============== power check ========================
filename="node_power_status.txt"
while read -r line; do
    check_power_status $line
done < "$filename"
#cd
#rm -rf instackenv.json
=======
echo "$node_uuids" > node_uuid_list.txt

filename="node_uuid_list.txt"
while read -r line; do
  setting_Maintenance $line
  deleting_node $line
done < "$filename"

cd
rm -rf instackenv.json
>>>>>>> 3fd1fb1ae0525ebe7ded70c66b69700457aeb1ee
