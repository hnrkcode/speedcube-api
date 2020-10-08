from django.test import TestCase

from api.models import CheckEmail, CheckUsername, TimeModel, UserModel


class TestCheckEmailModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        CheckEmail.objects.create(email="test@mail.com")

    def test_username_label(self):
        email = CheckEmail.objects.get(id=1)
        field_label = email._meta.get_field("email").verbose_name
        self.assertEquals(field_label, "email")

    def test_created_label(self):
        email = CheckEmail.objects.get(id=1)
        field_label = email._meta.get_field("created").verbose_name
        self.assertEquals(field_label, "created")

    def test_object_name(self):
        email = CheckEmail.objects.get(id=1)
        self.assertEquals(str(email), email.email)

    def test_username_max_length(self):
        email = CheckEmail.objects.get(id=1)
        field_label = email._meta.get_field("email").max_length
        self.assertEquals(field_label, 255)

    def test_created_default_arguments(self):
        email = CheckEmail.objects.get(id=1)
        is_auto_now_add = email._meta.get_field("created").auto_now_add
        self.assertTrue(is_auto_now_add)


class TestCheckUsernameModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        CheckUsername.objects.create(username="testvalue")

    def test_username_label(self):
        username = CheckUsername.objects.get(id=1)
        field_label = username._meta.get_field("username").verbose_name
        self.assertEquals(field_label, "username")

    def test_created_label(self):
        username = CheckUsername.objects.get(id=1)
        field_label = username._meta.get_field("created").verbose_name
        self.assertEquals(field_label, "created")

    def test_object_name(self):
        username = CheckUsername.objects.get(id=1)
        self.assertEquals(str(username), username.username)

    def test_username_max_length(self):
        username = CheckUsername.objects.get(id=1)
        field_label = username._meta.get_field("username").max_length
        self.assertEquals(field_label, 255)

    def test_created_default_arguments(self):
        username = CheckUsername.objects.get(id=1)
        is_auto_now_add = username._meta.get_field("created").auto_now_add
        self.assertTrue(is_auto_now_add)


class TestUserModel(TestCase):
    def setUp(self):
        user = UserModel.objects.create_user(
            username="TestUsername", password="TestPassword"
        )
        user.first_name = "First"
        user.last_name = "Last"
        user.save()

    def test_object_name(self):
        """Test __str__ method"""

        user = UserModel.objects.get(username="TestUsername")
        received = str(user)
        expected = "TestUsername"

        self.assertEqual(received, expected)

    def test_get_full_name(self):
        """Test if full name is first and last name"""

        user = UserModel.objects.get(username="TestUsername")
        received = user.get_full_name()
        expected = "First Last"

        self.assertEqual(received, expected)


class TestTimeModel(TestCase):
    def setUp(self):
        user = UserModel.objects.create_user(
            username="TestUsername", password="TestPassword"
        )
        user.save()
        time = TimeModel.objects.create(
            user=UserModel.objects.get(username="TestUsername"),
            time=1234,
            dnf=False,
            penalty=False,
            comment="Some comment",
        )
        time.save()

    def test_object_name(self):
        time = TimeModel.objects.get(time=1234)
        received = str(time)
        expected = str(time.time)

        self.assertEquals(received, expected)

    def test_user_label(self):
        time = TimeModel.objects.get(time=1234)
        field_label = time._meta.get_field("user")
        received = field_label.verbose_name
        expected = "user"

        self.assertEquals(received, expected)

    def test_time_label(self):
        time = TimeModel.objects.get(time=1234)
        field_label = time._meta.get_field("time")
        received = field_label.verbose_name
        expected = "time"

        self.assertEquals(received, expected)

    def test_dnf_label(self):
        time = TimeModel.objects.get(time=1234)
        field_label = time._meta.get_field("dnf")
        received = field_label.verbose_name
        expected = "dnf"

        self.assertEquals(received, expected)

    def test_penalty_label(self):
        time = TimeModel.objects.get(time=1234)
        field_label = time._meta.get_field("penalty")
        received = field_label.verbose_name
        expected = "penalty"

        self.assertEquals(received, expected)

    def test_comment_label(self):
        time = TimeModel.objects.get(time=1234)
        field_label = time._meta.get_field("comment")
        received = field_label.verbose_name
        expected = "comment"

        self.assertEquals(received, expected)

    def test_created_label(self):
        time = TimeModel.objects.get(time=1234)
        field_label = time._meta.get_field("created")
        received = field_label.verbose_name
        expected = "created"

        self.assertEquals(received, expected)

    def test_comment_default_argments(self):
        time = TimeModel.objects.get(time=1234)
        is_null = time._meta.get_field("comment").null
        is_blank = time._meta.get_field("comment").blank

        self.assertTrue(is_null)
        self.assertTrue(is_blank)

    def test_created_default_arguments(self):
        time = TimeModel.objects.get(time=1234)
        is_auto_now_add = time._meta.get_field("created").auto_now_add
        self.assertTrue(is_auto_now_add)

    def test_default_dnf_value(self):
        time = TimeModel.objects.get(time=1234)
        self.assertFalse(time.dnf)

    def test_default_penalty_value(self):
        time = TimeModel.objects.get(time=1234)
        self.assertFalse(time.penalty)
