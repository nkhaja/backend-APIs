import firstFlask as server
import unittest
from flask import jsonify, json

class FlaskServerTest(unittest.TestCase):

    def setUp(self):
        #Run app in testing mode to retrive exception and stacktraces
        server.app.testing = True
        self.app = server.app.test_client()


    def test_hello(self):
        response = self.app.get('/hello')
        assert response.status_code == 200, "status_code was not okay"
        print response
        assert response.data == "Hello World!"

    def test_hello_to_person(self):
        response = self.app.get('hello/Julia')
        assert response.data == "Hello, Julia!"

    def test_posts(self):
        dic = {"name":"Carmen", "species": "dog", "age": "80"}
        post = self.app.post('/pets', data=dic)
        #response = self.app.get('/pets')
        assert post.status_code == 200, "status_code was not okay"
        #assert response.data["name"] == "Carmen"









if __name__ == '__main__':
    unittest.main()
