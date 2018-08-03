INSERT INTO tiger.loader_platform(os, declare_sect, pgbin, wget, unzip_command, psql, path_sep, loader, environ_set_command, county_process_command)
SELECT 'stretch', 'TMPDIR="${staging_fold}/temp/"
UNZIPTOOL=unzip
WGETTOOL=usr/bin/wget
export PGBIN=/usr/bin

PSQL=${PGBIN}/psql
SHP2PGSQL=${PGBIN}/shp2pgsql
cd  ${staging_fold}/', pgbin, wget, unzip_command, psql, path_sep, loader, environ_set_command, county_process_command
FROM tiger.loader_platform
WHERE os = 'sh';