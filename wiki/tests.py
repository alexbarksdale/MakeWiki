from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page
from django.utils.text import slugify


class WikiTests(TestCase):
    def test_edit_page(self):
        # Create a new user
        user = User.objects.create_user(
            username='test', password='makeschool123')
        # The edit form is only displayed if a user is logged in.
        # Refer to the page.html in /wiki/templates/
        self.client.login(username='test', password='makeschool123')

        # Create our page
        page = Page.objects.create(
            title='Iron Man', content='Super smart guy', author=user)
        page.save()  # save our page

        # Our post data we're updating
        post_data = {
            'title': 'Batman',
            'content': 'Scary man',
            'author': user.id
        }

        # Create a post request with our new data
        res = self.client.post(f'/{slugify(page.title)}/', post_data)

        # Check that the response code was sent properly
        self.assertEqual(res.status_code, 302)

        updated_data = Page.objects.get(title=post_data['title'])
        # Check that our post data went through and updated the page
        self.assertEqual(updated_data.title, 'Batman')

    def test_detail_page(self):
        # Instance of user to test the pages
        user = User.objects.create()

        # Create a test detail page
        page = Page.objects.create(title="Captain America",
                                   content="100% Natural man", author=user)
        page.save()  # save our page

        # Making a GET request to get our test detail page
        res = self.client.get(f'/{slugify(page.title)}/')

        # Very a 200 response
        self.assertEqual(res.status_code, 200)
        # Check if the page contains Captain America (our title)
        self.assertContains(res, 'Captain America')

    def test_create_page(self):
        # Instance of user to test the pages
        user = User.objects.create()

        # Post data to be sent via the form
        post_data = {
            'title': 'Avengers',
            'content': 'Super strong heroes',
            'author': user.id
        }

        # Request to create a post
        res = self.client.post('/create/', data=post_data)

        # Verify our response
        self.assertEqual(res.status_code, 302)

        # Get object to test
        page_object = Page.objects.get(title='Avengers')

        # Check that the page object was created. Checking if the page title matches Avengers.
        self.assertEqual(page_object.title, 'Avengers')
