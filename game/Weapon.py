class Weapon:

    def __init__(self, material_type, weapon_type, image=None):
        self.material_type = material_type
        self.weapon_type = weapon_type
        self.max_damage = self.calculate_max_damage()
        self.price = self.generate_price()
        self.image = image

    def calculate_max_damage(self):
        return self.material_type.value * self.weapon_type.value

    def to_string(self):
        return self.material_type.name.capitalize() + " " + self.weapon_type.name.lower()

    def generate_price(self):
        price = self.max_damage * 2
        return price
