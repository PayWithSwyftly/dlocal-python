import unittest
from dlocal.client import DLocalExchangeRate


class TestDLocalClientLive(unittest.TestCase):
    def setUp(self):
        self.client = DLocalExchangeRate()

    def tearDown(self):
        self.client.close()

    def test_get_exchange_rate_live(self):
        response = self.client.get_exchange_rate("PHP")
        self.assertIn("rate", response)


if __name__ == "__main__":
    unittest.main()
