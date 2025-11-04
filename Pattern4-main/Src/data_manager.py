import json

class DataManager:
    def save_data_to_file(self, data, filename="data/data.json"):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({
                    "nomenclature": list(data["nomenclature"].values()),
                    "storage": [vars(s) for s in data["storages"].values()],
                    "transaction": [vars(t) for t in data["transactions"].values()],
                    "unit_measure": list(data["unit_measure"].values())
                }, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print("Ошибка при сохранении:", e)
            return False