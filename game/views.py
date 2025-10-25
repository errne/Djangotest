# game/views.py

from django.shortcuts import render

def game_scene(request):
    # This dictionary will hold all the data to be sent to the template
    context = {
        'scene_text': "You find yourself in a dimly lit cavern. A faint glow emanates from a passage to the north. A cold draft suggests another path to the west.",
        'choices': [
            {'text': "Go North", 'url': "/north"},
            {'text': "Go West", 'url': "/west"},
            {'text': "Examine the cavern", 'url': "/examine"},
        ],
        'character_name': "Hero McHeroFace",
        'character_health': 85,
        'character_mana': 45,
        'character_gold': 120,
        'inventory': [
            "Rusty Sword",
            "Leather Armor",
            "Healing Potion (x2)",
            "Torch",
            "Mysterious Orb",
        ]
    }
    return render(request, 'game/scene.html', context)

# You can add more view functions here for different scenes/actions
def north_path(request):
    context = {
        'scene_text': "You venture north into the glowing passage. The air grows warmer, and the walls begin to shimmer with arcane energy. You hear a low rumble...",
        'choices': [
            {'text': "Continue deeper", 'url': "/deeper"},
            {'text': "Turn back", 'url': "/"},
        ],
        'character_name': "Hero McHeroFace",
        'character_health': 80, # Health might change after an action
        'character_mana': 40,
        'character_gold': 120,
        'inventory': [
            "Rusty Sword",
            "Leather Armor",
            "Healing Potion (x2)",
            "Torch",
            "Mysterious Orb",
        ]
    }
    return render(request, 'game/scene.html', context)