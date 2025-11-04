import unittest
import datetime
from Src.Logics.report import Report

class TestReport(unittest.TestCase):
    def setUp(self):
        self.data = {
            "storages": {
                "s1": type("Storage", (), {"id": "s1", "name": "Склад 1", "address": "Адрес 1"})()
            },
            "nomenclature": {
                "n1": {"id": "n1", "name": "wheat flour", "unit_measurement": "u1"},
                "n2": {"id": "n2", "name": "sugar", "unit_measurement": "u1"},
                "n3": {"id": "n3", "name": "salt", "unit_measurement": "u1"}
            },
            "unit_measure": {
                "u1": {"id": "u1", "name": "gramm", "coefficient": 1}
            },
            "transactions": {
                "t1": type("Transaction", (), {
                    "nomenclature": "n1",
                    "storage": "s1",
                    "quantity": 100,
                    "date": datetime.date(2025, 1, 1),
                    "unit": "u1"
                })(),
                "t2": type("Transaction", (), {
                    "nomenclature": "n2",
                    "storage": "s1",
                    "quantity": 50,
                    "date": datetime.date(2025, 1, 2),
                    "unit": "u1"
                })(),
            }
        }

    def test_report_includes_all_nomenclature(self):
        report = Report(self.data)
        start_date = datetime.date(2025, 1, 1)
        end_date = datetime.date(2025, 1, 3)

        result = report.generateReport("s1", start_date, end_date)
        names = [r["nomenclature"] for r in result]
        self.assertIn("wheat flour", names)
        self.assertIn("sugar", names)
        self.assertIn("salt", names)
        salt_row = next(r for r in result if r["nomenclature"] == "salt")
        self.assertEqual(salt_row["start_balance"], 0)
        self.assertEqual(salt_row["income"], 0)
        self.assertEqual(salt_row["outcome"], 0)
        self.assertEqual(salt_row["end_balance"], 0)

if __name__ == "__main__":
    unittest.main()