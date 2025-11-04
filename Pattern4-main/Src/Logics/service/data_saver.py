import json

class data_saver:
    def __init__(self, repo, filepath="data/data.json"):
        self.repo = repo
        self.filepath = filepath

    def save_to_file(self):
        data = {}
        for key, items in self.repo.items():
            data[key] = []
            for obj in items:
                # Простейший сериализатор для теста
                item_dict = {k: str(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
                data[key].append(item_dict)

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return {"status": "ok", "file": self.filepath}