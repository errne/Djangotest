from enum import Enum


class ArmourMaterials(Enum):
    CLOTH = 1
    LEATHER = 4
    STEEL = 7
    MITHRIL = 9

    def create_list(self):
        armour_material_list = []
        for material in ArmourMaterials:
            armour_material_list.append(material)
        return armour_material_list
