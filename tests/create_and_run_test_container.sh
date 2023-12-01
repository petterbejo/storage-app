CONTAINER_NAME="test_storage_app"
SQL_SCRIPT="create_database_tables_and_test_content.sql"

docker run --name $CONTAINER_NAME -e POSTGRES_PASSWORD=somepassword -d postgres

docker cp $SQL_SCRIPT $CONTAINER_NAME:/docker-entrypoint-initdb.d/

docker restart $CONTAINER_NAME
