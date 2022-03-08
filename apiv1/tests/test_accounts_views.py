from rest_framework.test import APITestCase


class TestInitWordbookPageAPIView(APITestCase):
    TARGET_URL = '/api/v1/guest_login/'

    def test_return_201(self):
        response = self.client.post(self.TARGET_URL)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("auth_token" in response.data)
        self.assertTrue("user" in response.data)
