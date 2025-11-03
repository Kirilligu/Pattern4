import unittest
from main import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
    def test_get_report(self):
        response = self.client.get("/api/report_osv?start_date=2025-01-01&end_date=2025-01-03")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertIn("nomenclature", data[0])

    def test_get_references(self):
        response = self.client.get("/api/reference")
        self.assertEqual(response.status_code, 200)
        refs = response.get_json()
        self.assertIn("nomenclature", refs)
        self.assertIn("storages", refs)
        self.assertIn("unit_measure", refs)

if __name__ == "__main__":
    unittest.main()
