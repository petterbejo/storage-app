CONTAINER_NAME="test_storage_app"
SQL_SCRIPT="create_database_tables_and_test_content.sql"
TESTING_PASSWORD='somepassword'

docker run --name $CONTAINER_NAME --publish 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=$TESTING_PASSWORD -d postgres

docker cp $SQL_SCRIPT $CONTAINER_NAME:/docker-entrypoint-initdb.d/

docker restart $CONTAINER_NAME
