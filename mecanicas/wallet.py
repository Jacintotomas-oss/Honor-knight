
class wallet:
    def __init__(self, creditos_iniciales = 1000):
        self.creditos = creditos_iniciales
        self.deudas = [] #lista de {"acreedor": "tavernero", "monto": 100}
        self.items = []  # lista de {"nombre": "espada", "cantidad": 1}

    def ganar(self, cantidad, motivo=""):
        self.creditos += cantidad
        print(f"Ganaste {cantidad} créditos. {motivo} Saldo actual: {self.creditos} créditos.")
    
    def gastar(self, cantidad):
        if self.creditos >= cantidad:
            self.creditos -= cantidad
            return True
        return False # si no hay fondos
    
    def tomar_deuda(self, acredor, monto):
        self.creditos += monto
        self.deudas.append({"acreedor": acredor, "monto": monto})

    def pagar_deuda(self, acreedor):
        for deuda in self.deudas:
            if deuda["acreedor"] == acreedor:
                if self.gastar(deuda["monto"]):
                    self.deudas.remove(deuda)
                    return True
        return False # no se encontró la deuda o no hay fondos
    
    def agregar_item(self, nombre, cantidad=1):
        for item in self.items:
            if item["nombre"] == nombre:
                item["cantidad"] += cantidad
                return
        self.items.append({"nombre": nombre, "cantidad": cantidad})

    def total_deudas(self):
        return sum(d["monto"] for d in self.deudas)
