from django.test import TestCase

from api.decorators import empty_list, round_number


class TestDecorators(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_round_number(self):
        pass

    def test_empty_list(self):
        func = empty_list(lambda x: x)
        self.assertEquals(func([]), 0)

    def test_none_empty_list(self):
        func = empty_list(lambda x: x)
        self.assertEquals(func([1, 2, 3]), [1, 2, 3])

    def test_round_number_without_decimals(self):
        number = 123.123456789
        func = lambda x: x
        result = round_number()(func)(number)
        self.assertEquals(result, 123)

    def test_round_number_with_decimals(self):
        number = 123.123456789
        func = lambda x: x

        for decimals in range(10):
            self.assertEquals(round_number(decimals)(func)(number), round(number, decimals))
        