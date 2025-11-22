# game/views.py
import pickle
import base64
import logging
from django.shortcuts import render, redirect
from .Game import Game
from .Player import Player
from .Reputation import ReputationManager
from .World import World

logger = logging.getLogger(__name__)


def start_game(request):
    return render(request, 'game/start.html')

def new_game(request):
    if request.method == 'POST':
        player_name = request.POST.get('player_name', 'Hero')
        logger.info(f"Starting new game for player: {player_name}")
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
    messages = world.game.messages.copy()
    world.game.messages.clear()

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
        'messages': messages,
        'choices': scene['choices'],
        'scene_name': type(world.current_state).__name__,
        'character_name': player.name,
        'character_health': player.get_health(),
        'character_gold': player.gold_pouch,
        'character_health_pots': player.num_health_pots,
        'character_attack_pots': player.num_attack_pots,
        'character_attack_rating': player.max_attack_damage,
        'character_armour_rating': player.get_total_armour_level(),
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

    logger.info(f"Player {player.name} chose option {choice_index} in scene {scene_name}")
    scene = world.handle_choice(choice_index - 1)

    if scene and scene.get('game_over'):
        request.session.flush()
        return redirect('game_over')

    messages = world.game.messages.copy()
    world.game.messages.clear()

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
        'messages': messages,
        'choices': scene['choices'],
        'scene_name': type(world.current_state).__name__,
        'character_name': player.name,
        'character_health': player.get_health(),
        'character_mana': 0,  # Your Player class doesn't have mana
        'character_gold': player.gold_pouch,
        'character_health_pots': player.num_health_pots,
        'character_attack_pots': player.num_attack_pots,
        'character_attack_rating': player.max_attack_damage,
        'character_armour_rating': player.get_total_armour_level(),
        'inventory': player.inventory,
        'inventory_grid': grid,
    }
    return render(request, 'game/scene.html', context)

def inventory_view(request):
    if 'game_state' not in request.session:
        return redirect('start_game')

    game_state = request.session['game_state']
    world = pickle.loads(base64.b64decode(game_state['world']))
    player = world.player

    # Prepare inventory grid similar to game_scene
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
        'character_name': player.name,
        'character_health': player.get_health(),
        'character_gold': player.gold_pouch,
        'inventory_grid': grid,
    }
    return render(request, 'game/inventory.html', context)

def journal_view(request):
    if 'game_state' not in request.session:
        return redirect('start_game')

    game_state = request.session['game_state']
    world = pickle.loads(base64.b64decode(game_state['world']))
    player = world.player

    # Convert reputation points to display levels
    reputation_display = {}
    for faction, points in player.reputation.items():
        reputation_display[faction] = ReputationManager.get_level_from_points(points)

    context = {
        'character_name': player.name,
        'character_health': player.get_health(),
        'character_gold': player.gold_pouch,
        'character_attack_rating': player.max_attack_damage,
        'character_armour_rating': player.get_total_armour_level(),
        'reputation': reputation_display,
    }
    return render(request, 'game/journal.html', context)

def quests_view(request):
    if 'game_state' not in request.session:
        return redirect('start_game')

    game_state = request.session['game_state']
    world = pickle.loads(base64.b64decode(game_state['world']))
    player = world.player

    active_quests = [q for q in player.quests if not q.is_completed]
    completed_quests = [q for q in player.quests if q.is_completed]

    context = {
        'character_name': player.name,
        'character_health': player.get_health(),
        'character_gold': player.gold_pouch,
        'active_quests': active_quests,
        'completed_quests': completed_quests,
    }
    return render(request, 'game/quests.html', context)