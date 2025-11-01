from enum import Enum


class ArmourTypes(Enum):
    BOOTS = 2
    HELM = 5
    TROUSERS = 7
    CHEST = 10

    def create_list(self):
        armour_list = []
        for material in ArmourTypes:
            armour_list.append(material)
        return armour_list
