import datetime

class TransactionModel:
    def __init__(self, date, nomenclature_id, storage_id, quantity, unit_id):
        self.date = date
        self.nomenclature = nomenclature_id
        self.storage = storage_id
        self.quantity = quantity
        self.unit = unit_id
