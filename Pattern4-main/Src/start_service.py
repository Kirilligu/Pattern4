import json
import datetime
from Src.Models.transaction_model import TransactionModel
from Src.Models.storage_model import StorageModel

class StartService:
    def __init__(self, data_file="data/data.json"):
        self.data_file = data_file
        self.data = {
            "storages": {},
            "transactions": {},
            "nomenclature": {},
            "unit_measure": {}
        }

    def start(self):
        with open(self.data_file, "r", encoding="utf-8") as f:
            raw = json.load(f)

        for s in raw.get("storage", []):
            self.data["storages"][s["id"]] = StorageModel(s["id"], s["name"], s["address"])

        for t in raw.get("transaction", []):
            date = datetime.date(2025, 1, 1)  # для примера фиксируем дату
            self.data["transactions"][t["id"]] = TransactionModel(
                date, t["nomenclature"], t["storage"], t["quantity"], t["unit"]
            )
        for n in raw.get("nomenclature", []):
            self.data["nomenclature"][n["id"]] = n
        for u in raw.get("unit_measure", []):
            self.data["unit_measure"][u["id"]] = u