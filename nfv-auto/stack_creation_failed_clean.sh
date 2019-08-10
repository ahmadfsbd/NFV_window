#!/bin/bash
counter=0
line=''
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
echo "$node_uuids" > node_uuid_list.txt

filename="node_uuid_list.txt"
while read -r line; do
  setting_Maintenance $line
  deleting_node $line
done < "$filename"

cd
rm -rf instackenv.json