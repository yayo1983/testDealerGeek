from django.test import TestCase


class ViewsTestCase(TestCase):
    def test_check_urls(self):
        """The index page loads properly"""
        response = self.client.get('127.0.0.1:8000')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/package/create')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/tracking')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/package/update')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/package/report')
        # Is 302 because check if authenticated user
        self.assertEqual(response.status_code, 302)