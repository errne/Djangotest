# game/views.py
import pickle
import base64
from django.shortcuts import render, redirect
from .Game import Game
from .Player import Player
from .World import World

def game_scene(request, scene_name=None):
    if 'game_state' not in request.session:
        game = Game()
        player = game.create_player("Hero")
        world = World(player, game)
    else:
        game_state = request.session['game_state']
        player = pickle.loads(base64.b64decode(game_state['player']))
        world = pickle.loads(base64.b64decode(game_state['world']))

    scene = world.get_current_scene()
    
    # Save the updated state
    request.session['game_state'] = {
        'player': base64.b64encode(pickle.dumps(player)).decode('utf-8'),
        'world': base64.b64encode(pickle.dumps(world)).decode('utf-8')
    }

    context = {
        'scene_text': scene['text'],
        'choices': scene['choices'],
        'scene_name': world.current_location or 'start',
        'character_name': player.name,
        'character_health': player.get_health(),
        'character_mana': 0,  # Your Player class doesn't have mana
        'character_gold': player.gold_pouch,
        'inventory': [item.to_string() for item in player.inventory] if hasattr(player, 'inventory') else []
    }
    return render(request, 'game/scene.html', context)

def make_choice(request, scene_name, choice_index):
    if 'game_state' not in request.session:
        return redirect('game_scene')

    game_state = request.session['game_state']
    player = pickle.loads(base64.b64decode(game_state['player']))
    world = pickle.loads(base64.b64decode(game_state['world']))

    scene = world.handle_choice(choice_index - 1)

    # If handle_choice returns a new scene, we update the context with it
    if scene:
        request.session['game_state'] = {
            'player': base64.b64encode(pickle.dumps(player)).decode('utf-8'),
            'world': base64.b64encode(pickle.dumps(world)).decode('utf-8')
        }

    return redirect('game_scene')