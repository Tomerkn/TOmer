# הגדרה נכונה של מחלקות ניירות ערך
class Security:
    def __init__(self, name="Unknown", amount=0):
        self.name = name
        self.amount = amount

class Stock(Security):
    def __init__(self,name="Unknown", amount=0):
        super().__init__(name,amount)

class Bond(Security):
    def __init__(self, name="Unknown"):
        super().__init__(name)

class RegularStock(Stock):
    def __init__(self, name="Regular Stock"):
        super().__init__(name)

class PreferredStock(Stock):
    def __init__(self, name="Preferred Stock"):
        super().__init__(name)

class CorporateBond(Bond):
    def __init__(self, name="Corporate Bond"):
        super().__init__(name)

class GovernmentalBond(Bond):
    def __init__(self, name="Governmental Bond"):
        super().__init__(name)
