from enum import Enum


class MaterialTypes(Enum):
    WOOD = 3
    IRON = 6
    STEEL = 8
    MITHRIL = 10

    def create_list(self):
        material_list =[]
        for material in MaterialTypes:
            material_list.append(material)
        return material_list
