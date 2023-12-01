"""
Note: Remember to create a test container before running the tests the
first time. Please refer to the readme file of this project.
"""

import os

class TestConnection():
    def setup_method(self):
        # self.circle = shapes.Circle(10)
        os.system('docker start test_storage_app')

    def teardown_method(self):
        # reset database to original state, and stop the container!
        os.system('docker stop test_storage_app')

