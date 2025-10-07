"""
config.py - Configuration de l'application (version mise à jour)
"""

# === CONFIGURATION DES PROJECTEURS ===
PROJECTOR_CONFIG = {
    'default_count': 4,
    'default_color': '#ff0000',
    'default_intensity': 100,
    'max_intensity': 100,
    'min_intensity': 0
}

# === CONFIGURATION DE L'AFFICHAGE ===
DISPLAY_CONFIG = {
    'projector_width': 180,
    'projector_height': 80,
    'spacing': 20,
    'start_x': 20,
    'canvas_width': 820,
    'canvas_height': 120
}

# === CONFIGURATION DES EFFETS ===
EFFECTS_CONFIG = {
    'loop_interval': 100,
    'blink_speed': 10,
    'strobe_speed': 6,
    'fade_speed': 200,
    'chaser_speed': 5, 
    'default_fade_colors': ['#ff0000', "#0000ff"]
}

# === CONFIGURATION DE L'INTERFACE ===
UI_CONFIG = {
    'window_title': 'LightControl - Console DMX',
    'window_geometry': '900x750',
    'background_color': '#1a1a1a',
    'panel_color': '#2a2a2a',
    'control_color': '#333333',
    'quick_scenes_count': 6
}

# === STYLES DES BOUTONS ===
BUTTON_STYLES = {
    'default': {
        'bg': '#333333',
        'fg': 'white',
        'activebackground': '#555555',
        'activeforeground': 'white',
        'font': ('Arial', 9, 'bold'),
        'relief': 'raised',
        'bd': 2
    },
    'on_off': {
        'bg': '#006600',
        'fg': 'white',
        'activebackground': '#008800',
        'font': ('Arial', 9, 'bold')
    },
    'color': {
        'bg': '#660066',
        'fg': 'white',
        'activebackground': '#880088',
        'font': ('Arial', 9, 'bold')
    },
    'effect': {
        'bg': '#cc3300',
        'fg': 'white',
        'activebackground': '#ff4400',
        'font': ('Arial', 9, 'bold')
    },
    'stop': {
        'bg': '#990000',
        'fg': 'white',
        'activebackground': '#cc0000',
        'font': ('Arial', 9, 'bold')
    },
    'scene': {
        'bg': '#666600',
        'fg': 'white',
        'activebackground': '#888800',
        'font': ('Arial', 9, 'bold')
    },
    'selected': {
        'bg': '#ff6600'
    },
    'programmed': {
        'bg': '#006666'
    }
}

# === CONFIGURATION DES FICHIERS ===
FILES_CONFIG = {
    'scenes_file': 'light_scenes.json',
    'config_file': 'app_config.json',
    'export_extension': '.json'
}

# === MESSAGES DE L'INTERFACE ===
MESSAGES = {
    'save_scene_title': 'Sauvegarder',
    'save_scene_prompt': 'Nom de la scène:',
    'load_scene_title': 'Charger',
    'load_scene_prompt': 'Scènes disponibles: {scenes}\nNom de la scène:',
    'delete_scene_title': 'Supprimer une scène',
    'delete_scene_prompt': 'Scènes disponibles: {scenes}\nNom de la scène à supprimer:',
    'delete_scene_confirm': 'Êtes-vous sûr de vouloir supprimer la scène \'{name}\'?',
    'no_scenes': 'Aucune scène sauvegardée!',
    'scene_saved': 'Scène \'{name}\' sauvegardée!',
    'scene_loaded': 'Scène \'{name}\' chargée!',
    'scene_deleted': 'Scène \'{name}\' supprimée!',
    'scene_not_found': 'Scène \'{name}\' introuvable!',
    'scene_delete_error': 'Impossible de supprimer la scène \'{name}\'',
    'quick_scene_programmed': 'Scène rapide {number} programmée!',
    'quick_scene_loaded': 'Scène rapide {number} chargée!',
    'quick_scenes_cleared': '{count} scènes rapides effacées!',
    'no_quick_scenes': 'Aucune scène rapide à effacer.',
    'confirm_clear_quick': 'Êtes-vous sûr de vouloir effacer toutes les scènes rapides?',
    'fade_colors_title': 'Couleurs du fondu',
    'fade_color1_title': 'Première couleur du fondu',
    'fade_color2_title': 'Deuxième couleur du fondu',
    'fade_configured': 'Fondu configuré:\n{color1} → {color2}',
    'color_picker_title': 'Choisir une couleur',
    'invalid_scene_name': 'Le nom ne peut pas commencer par \'Quick_\'',
    'save_error': 'Erreur lors de la sauvegarde',
    'load_error': 'Erreur lors du chargement',
    'delete_error': 'Erreur lors de la suppression'
}

# === LABELS DE L'INTERFACE ===
LABELS = {
    'projection_screen': 'ÉCRAN PROJECTION',
    'dmx_console': 'CONSOLE DE MIXAGE DMX',
    'projector_selection': 'SÉLECTION PROJECTEUR',
    'individual_controls': 'CONTRÔLES INDIVIDUELS',
    'dmx_intensity': 'INTENSITÉ DMX',
    'special_effects': 'EFFETS SPÉCIAUX',
    'effects_config': 'CONFIG EFFETS',
    'active_effects': 'EFFETS ACTIFS:',
    'global_controls': 'CONTRÔLES GLOBAUX',
    'scene_memory': 'MÉMOIRE SCÈNES',
    'quick_recall': 'RAPPEL RAPIDE',
    'on_off': 'ON/OFF',
    'color': 'COULEUR',
    'blink': 'BLINK',
    'blink_all': 'BLINK ALL',
    'strobe': 'STROBE',
    'fade': 'FONDU',
    'chaser': 'CHASER',
    'fade_colors': 'Couleurs Fondu',
    'stop_effects': 'ARRÊT EFFETS',
    'all_on': 'TOUT\nALLUMER',
    'all_off': 'TOUT\nÉTEINDRE',
    'save_scene': 'SAUVER\nSCÈNE',
    'load_scene': 'CHARGER\nSCÈNE',
    'delete_scene': 'SUPPR\nSCÈNE',
    'clear_quick_scenes': 'EFFACER\nSCÈNES RAPIDES'
}