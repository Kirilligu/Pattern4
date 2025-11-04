from flask import Flask, request, jsonify
from Src.start_service import StartService
from Src.Logics.report import Report
from Src.data_manager import DataManager
import datetime
import json
import os

app = Flask(__name__)
settings_file = "settings.json"
if os.path.exists(settings_file):
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
else:
    settings = {"first_start": True}
service = StartService()
if settings.get("first_start", True):
    service.start()  # формируем стартовые данные
    settings["first_start"] = False  # выключаем первый старт
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)
else:
    service.start()

report_service = Report(service.data)
data_manager = DataManager()
@app.route("/api/report_osv", methods=["GET"])
def get_report():
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    storage_id = request.args.get("storage_id") or list(service.data["storages"].keys())[0]
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    result = report_service.generateReport(storage_id, start_date, end_date)
    return jsonify(result)

#сохранения данных в файл
@app.route("/api/save", methods=["POST"])
def save_data():
    success = data_manager.save_data_to_file(service.data)
    return jsonify({"success": success})

#получения справочников
@app.route("/api/reference", methods=["GET"])
def get_references():
    references = {
        "nomenclature": list(service.data["nomenclature"].values()),
        "storages": [vars(s) for s in service.data["storages"].values()],
        "unit_measure": list(service.data["unit_measure"].values())
    }
    return jsonify(references)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)