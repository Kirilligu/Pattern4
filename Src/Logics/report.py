class Report:
    def __init__(self, data):
        self.data = data

    def generateReport(self, storage_id, start_date, end_date):
        result = []
        for nomen_id, nomen in self.data["nomenclature"].items():
            start_balance = 0
            income = 0
            outcome = 0
            for t_id, t in self.data["transactions"].items():
                if t.storage == storage_id and t.nomenclature == nomen_id:
                    q = t.quantity
                    if t.date < start_date:
                        start_balance += q
                    elif start_date <= t.date <= end_date:
                        if q > 0:
                            income += q
                        else:
                            outcome += abs(q)

            result.append({
                "nomenclature": nomen["name"],
                "unit": self.data["unit_measure"][nomen["unit_measurement"]]["name"],
                "start_balance": start_balance,
                "income": income,
                "outcome": outcome,
                "end_balance": start_balance + income - outcome
            })

        return result
