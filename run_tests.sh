#!/bin/sh
# #####################################################################################
# Generar base de test con datos de prueba y opcionalmente instalarle módulos a testear
#
# Este script requiere en la carpeta backup_dir una subcarpeta bkp_test en la que debe
# haber un backup llamado test.zip que contiene un backup de una base vacia con datos
# de prueba credenciales admin / admin y sin modificar pais y lenguaje de los valores
# por defecto.
# #####################################################################################

IMAGE="jobiols/odoo-ent:17.0e.debug"
DB="pg-sama:db"
BASE=$(readlink -f "../../..")

# restaurar la base de test vacia
cp $BASE/sama/backup_dir/bkp_test/test.zip $BASE/sama/backup_dir/
oe --restore -d sama_test --no-deactivate -f test.zip
rm $BASE/sama/backup_dir/test.zip

sudo docker run --rm -it \
    --link wdb \
    --link $DB \
    -v $BASE/sama/config:/opt/odoo/etc/ \
    -v $BASE/sama/data_dir:/opt/odoo/data \
    -v $BASE/sama/sources:/opt/odoo/custom-addons \
    -v $BASE/sama/backup_dir:/var/odoo/backups/ \
    -e ODOO_CONF=/dev/null \
    -e WDB_SOCKET_SERVER=wdb $IMAGE --stop-after-init -d sama_test \
    -i modulo-a-testear # --test-enable.
