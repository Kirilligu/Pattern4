import connexion
from flask import request, jsonify
from Src.start_service import start_service
from Src.reposity import reposity
from Src.Logics.factory_entities import factory_entities

app = connexion.FlaskApp(__name__)

# Инициализация сервисов
data_service = start_service()
data_service.start()
response_factory = factory_entities()


@app.route("/api/accessibility", methods=['GET'])
def check_accessibility():
    """
    Проверить доступность REST API
    """
    return "Good job"


@app.route("/api/data/<entity_type>", methods=['GET'])
def get_entity_data(entity_type):
    # Получение формата
    response_format = request.args.get('format', 'csv').lower()
    entity_to_key_mapping = {
        "nomenclature": reposity.nomenclature_key(),
        "range": reposity.range_key(),
        "receipt": reposity.receipt_key(),
        "group": reposity.group_key()
    }
    if entity_type not in entity_to_key_mapping:
        return jsonify({"error": "Неизвестный тип сущности"}), 404
    entity_data = data_service.data[entity_to_key_mapping[entity_type]]

    try:
        format_handler = response_factory.create(response_format)
        formatted_response = format_handler.build(response_format, entity_data)
        return formatted_response, 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)