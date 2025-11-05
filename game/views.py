# game/views.py
import pickle
import base64
from django.shortcuts import render, redirect
from .Game import Game
from .Player import Player
from .World import World

def start_game(request):
    return render(request, 'game/start.html')

def new_game(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name', 'Hero')
        game = Game()
        player = game.create_player(player_name)
        world = World(player, game)
        request.session['game_state'] = {
            'world': base64.b64encode(pickle.dumps(world)).decode('utf-8')
        }
        return redirect('game_scene')
    return redirect('start_game')

def game_scene(request, scene_name=None):
    if 'game_state' not in request.session:
        return redirect('start_game')

    game_state = request.session['game_state']
    world = pickle.loads(base64.b64decode(game_state['world']))
    player = world.player
    if not hasattr(player, 'gold_pouch'):
        player.gold_pouch = 0

    scene = world.get_current_scene()

    inventory = player.inventory
    grid = []
    for i in range(4):
        row = []
        for j in range(6):
            index = i * 6 + j
            if index < len(inventory):
                row.append(inventory[index])
            else:
                row.append(None)
        grid.append(row)

    context = {
        'scene_text': scene['text'],
        'choices': scene['choices'],
        'scene_name': world.current_location or 'start',
        'character_name': player.name,
        'character_health': player.get_health(),
        'character_mana': 0,  # Your Player class doesn't have mana
        'character_gold': player.gold_pouch,
        'inventory_grid': grid,
    }
    return render(request, 'game/scene.html', context)

def game_over(request):
    return render(request, 'game/game_over.html')

def make_choice(request, scene_name, choice_index):
    if 'game_state' not in request.session:
        return redirect('game_scene')

    game_state = request.session['game_state']
    world = pickle.loads(base64.b64decode(game_state['world']))
    player = world.player
    if not hasattr(player, 'gold_pouch'):
        player.gold_pouch = 0

    scene = world.handle_choice(choice_index - 1)

    if scene and scene.get('game_over'):
        request.session.flush()
        return redirect('game_over')

    # Save the updated world object back to the session
    request.session['game_state'] = {
        'world': base64.b64encode(pickle.dumps(world)).decode('utf-8')
    }

    inventory = player.inventory
    grid = []
    for i in range(4):
        row = []
        for j in range(6):
            index = i * 6 + j
            if index < len(inventory):
                row.append(inventory[index])
            else:
                row.append(None)
        grid.append(row)

    context = {
        'scene_text': scene['text'],
        'choices': scene['choices'],
        'scene_name': world.current_location or 'start',
        'character_name': player.name,
        'character_health': player.get_health(),
        'character_mana': 0,  # Your Player class doesn't have mana
        'character_gold': player.gold_pouch,
        'inventory': player.inventory,
        'inventory_grid': grid,
    }
    return render(request, 'game/scene.html', context)