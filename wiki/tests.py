from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page


class ListViewTests(TestCase):
    def test_detail_page(self):
        # Instance of user to test the pages
        user = User.objects.create()

        # Create a test detail page
        Page.objects.create(title="Test", content="test content", author=user)

        # Making a GET request to the home page
        res = self.client.get('/')

        # Very a 200 response
        self.assertEqual(res.status_code, 200)
        result = res.context['pages']

        # Check if we got out test page
        self.assertQuerysetEqual(
            result,
            ['<Page: Test>']
        )
