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
    @classmethod
    def setUpTestData(cls):
        UserModel.objects.create(
            username="test",
            email="test@test.com",
            password="test",
            first_name="Aaaa",
            last_name="Bbbb",
        )

    def test_full_name(self):
        """Test if full name is first and last name"""
        user = UserModel.objects.get(id=1)
        self.assertEqual(user.full_name(), f"{user.first_name} {user.last_name}")


class TestTimeModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserModel.objects.create(
            username="test", email="test@test.com", password="test"
        )
        TimeModel.objects.create(
            user=UserModel.objects.get(id=1),
            time=1234,
            dnf=False,
            penalty=False,
            comment="Some comment",
        )

    def test_object_name(self):
        time = TimeModel.objects.get(id=1)
        self.assertEquals(str(time), str(time.time))

    def test_user_label(self):
        time = TimeModel.objects.get(id=1)
        field_label = time._meta.get_field("user").verbose_name
        self.assertEquals(field_label, "user")

    def test_time_label(self):
        time = TimeModel.objects.get(id=1)
        field_label = time._meta.get_field("time").verbose_name
        self.assertEquals(field_label, "time")

    def test_dnf_label(self):
        time = TimeModel.objects.get(id=1)
        field_label = time._meta.get_field("dnf").verbose_name
        self.assertEquals(field_label, "dnf")

    def test_penalty_label(self):
        time = TimeModel.objects.get(id=1)
        field_label = time._meta.get_field("penalty").verbose_name
        self.assertEquals(field_label, "penalty")

    def test_comment_label(self):
        time = TimeModel.objects.get(id=1)
        field_label = time._meta.get_field("comment").verbose_name
        self.assertEquals(field_label, "comment")

    def test_created_label(self):
        time = TimeModel.objects.get(id=1)
        field_label = time._meta.get_field("created").verbose_name
        self.assertEquals(field_label, "created")

    def test_comment_default_argments(self):
        time = TimeModel.objects.get(id=1)
        is_null = time._meta.get_field("comment").null
        is_blank = time._meta.get_field("comment").blank
        self.assertTrue(is_null)
        self.assertTrue(is_blank)

    def test_created_default_arguments(self):
        time = TimeModel.objects.get(id=1)
        is_auto_now_add = time._meta.get_field("created").auto_now_add
        self.assertTrue(is_auto_now_add)

    def test_default_dnf_value(self):
        time = TimeModel.objects.get(id=1)
        self.assertEquals(time.dnf, False)

    def test_default_penalty_value(self):
        time = TimeModel.objects.get(id=1)
        self.assertEquals(time.penalty, False)
