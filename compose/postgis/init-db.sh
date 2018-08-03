#!bin/sh

set -e

psql -c "CREATE DATABASE geodjango"

psql -f tiger_loader_platform.sql

#restart postgresql
service postgresql restart

psql -c "SELECT loader_generate_nation_script('stretch') AS aaaaa" -t -x -A -F "" -q -o 02a_load_nation_tiger.sh
#Replace the text
sed -i 's/aaaaa//g' 02a_load_nation_tiger.sh
chmod a+x 02a_load_nation_tiger.sh
su postgres 02a_load_nation_tiger.sh

psql -c "SELECT loader_generate_script(ARRAY[$geostates], 'stretch') AS aaaaa" -t -x -A -F "" -q -o 02b_load_state_tiger.sh

sed -i 's/aaaaa//g' 02b_load_state_tiger.sh
chmod a+x 02b_load_state_tiger.sh
su postgres 02b_load_state_tiger.sh

psql -c "SELECT install_missing_indexes()"
