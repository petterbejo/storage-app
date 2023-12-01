"""
Note: Remember to create a test container before running the tests the
first time. Please refer to the readme file of this project.
"""
import os
from time import sleep

import pytest
from psycopg2 import Error

from app.data_handler import DataHandler

class TestConnection():
    def setup_method(self):
        os.system('docker start test_storage_app')
        os.environ['POSTGRES_PASSWORD_FILE'] = 'tests/db_password.txt'
        os.environ['POSTGRES_DB'] = 'postgres'
        os.environ['DB_PORT'] = '5432'
        os.environ['POSTGRES_USER'] = 'postgres'
        os.environ['DB_HOST'] ='localhost'
        sleep(0.5) # Container needs a moment to accept queries
        self.data_handler = DataHandler()

    def teardown_method(self):
        # reset database to original state, and stop the container!
        os.system('docker stop test_storage_app')

    def test_basic_connection(self):
        os.system('docker ps')
        try:
            conn = self.data_handler._get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categories;')

            result = cursor.fetchone()
            cursor.close()
            conn.close()
            assert result is not None
        except Error as e:
            pytest.fail(f"Error: {e}")


