import json

from rest_framework.test import APITestCase


class TestNotFoundAPIView(APITestCase):
    def test_raise_404_exception_with_invalid_get_request(self):
        response = self.client.get('/api/v1/not_exist_uri')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['detail'], '見つかりませんでした。')

    def test_raise_404_exception_with_invalid_post_request(self):
        response = self.client.post('/api/v1/not_exist_uri')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['detail'], '見つかりませんでした。')

    def test_raise_404_exception_with_invalid_put_request(self):
        response = self.client.put('/api/v1/not_exist_uri')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['detail'], '見つかりませんでした。')

    def test_raise_404_exception_with_invalid_delete_request(self):
        response = self.client.delete('/api/v1/not_exist_uri')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['detail'], '見つかりませんでした。')

    def test_return_template_when_the_path_is_outside_of_api(self):
        response = self.client.get('/aaa')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response['content-type'], 'text/html')

    