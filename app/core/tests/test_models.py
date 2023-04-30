"""
TEST for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

#when we use other model we have to use that directly
from core import models

def create_user(email='user@example.com', password='testpass123'):
    """create and return a new user"""
    return get_user_model().objects.create_user(email,password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_with_email(self):
        """Test creating a user with email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails=[
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email,expected)


    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')


    def test_create_superuser(self):
        """Test creating Super User"""
        user = get_user_model().objects.create_superuser(
            'test1@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_recipe(self):
        """Test creating a recipe is successful"""
        # creating user so it assign to the the recipe
        user = get_user_model().objects.create_user(
            'test@example.com'
            'testpass123'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='sample recipe name',
            time_minutes=5,
            # better use integer
            price=Decimal('5.50'),
            description='sample recipe description',
        )
        # here string representation I use a logic in model that convers the model to title
        self.assertEqual(str(recipe), recipe.title)


    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)