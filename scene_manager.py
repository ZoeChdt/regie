"""
scene_manager.py - Gestionnaire des scènes utilisant config.py
Version avec support de sauvegarde/restauration des effets
"""
import json
import os
from config import FILES_CONFIG

class SceneManager:
    def __init__(self, projectors, effects_manager=None):
        self.projectors = projectors
        self.effects_manager = effects_manager
        self.scenes = {}
        self.quick_scenes = {}
        self.scenes_file = FILES_CONFIG['scenes_file']
        self.load_scenes_from_file()
    
    def set_effects_manager(self, effects_manager):
        """Définit le gestionnaire d'effets (si créé après le SceneManager)"""
        self.effects_manager = effects_manager
    
    def save_scene(self, scene_name):
        """Sauvegarde l'état actuel des projecteurs ET des effets comme une scène"""
        try:
            scene_data = {
                'projectors': {},
                'effects': None
            }
            
            for i, projector in self.projectors.items():
                scene_data['projectors'][str(i)] = projector.get_state()
            
            if self.effects_manager:
                scene_data['effects'] = self.effects_manager.get_state()
            
            self.scenes[scene_name] = scene_data
            return self.save_scenes_to_file()
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la scène '{scene_name}': {e}")
            return False
    
    def load_scene(self, scene_name):
        """Charge une scène et l'applique aux projecteurs ET aux effets"""
        try:
            if scene_name not in self.scenes:
                print(f"Scène '{scene_name}' non trouvée")
                return False
            
            scene_data = self.scenes[scene_name]
            
            if 'projectors' in scene_data:
                projectors_data = scene_data['projectors']
                effects_data = scene_data.get('effects')
            else:
                projectors_data = scene_data
                effects_data = None
            
            for proj_id_str, state in projectors_data.items():
                proj_id = int(proj_id_str)
                if proj_id in self.projectors:
                    self.projectors[proj_id].set_state(state)
            
            if self.effects_manager and effects_data:
                self.effects_manager.set_state(effects_data)
            elif self.effects_manager:
                self.effects_manager.stop_all_effects()
            
            return True
        except Exception as e:
            print(f"Erreur lors du chargement de la scene '{scene_name}': {e}")
            return False
    
    def delete_scene(self, scene_name):
        """Supprime une scène"""
        try:
            if scene_name in self.scenes:
                del self.scenes[scene_name]
                return self.save_scenes_to_file()
            return False
        except Exception as e:
            print(f"Erreur lors de la suppression de la scene '{scene_name}': {e}")
            return False
    
    def get_scene_list(self):
        """Retourne la liste des noms de scènes (exclut les scènes rapides Quick_*)"""
        return [name for name in self.scenes.keys() if not name.startswith('Quick_')]
    
    def get_all_scenes_list(self):
        """Retourne la liste complète des noms de scènes"""
        return list(self.scenes.keys())
    
    def save_quick_scene(self, scene_index):
        """Sauvegarde une scène de rappel rapide (0-5)"""
        scene_name = f"Quick_{scene_index}"
        return self.save_scene(scene_name)
    
    def load_quick_scene(self, scene_index):
        """Charge une scène de rappel rapide"""
        scene_name = f"Quick_{scene_index}"
        return self.load_scene(scene_name)
    
    def has_quick_scene(self, scene_index):
        """Vérifie si une scène rapide existe"""
        scene_name = f"Quick_{scene_index}"
        return scene_name in self.scenes
    
    def delete_quick_scene(self, scene_index):
        """Supprime une scène de rappel rapide"""
        scene_name = f"Quick_{scene_index}"
        return self.delete_scene(scene_name)
    
    def save_scenes_to_file(self):
        """Sauvegarde toutes les scènes dans un fichier JSON"""
        try:
            os.makedirs(os.path.dirname(self.scenes_file) if os.path.dirname(self.scenes_file) else '.', exist_ok=True)
            
            with open(self.scenes_file, 'w', encoding='utf-8') as f:
                json.dump(self.scenes, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des scènes: {e}")
            return False
    
    def load_scenes_from_file(self):
        """Charge les scènes depuis le fichier JSON"""
        try:
            if os.path.exists(self.scenes_file):
                with open(self.scenes_file, 'r', encoding='utf-8') as f:
                    loaded_scenes = json.load(f)
                    self.scenes = {}
                    for scene_name, scene_data in loaded_scenes.items():
                        if isinstance(scene_data, dict):
                            self.scenes[scene_name] = scene_data
            else:
                self.scenes = {}
        except Exception as e:
            print(f"Erreur lors du chargement des scènes: {e}")
            self.scenes = {}
    
    def export_scenes(self, filename=None):
        """Exporte toutes les scènes vers un fichier"""
        if filename is None:
            filename = f"scenes_export{FILES_CONFIG['export_extension']}"       
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.scenes, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de l'export: {e}")
            return False
    
    def import_scenes(self, filename):
        """Importe des scènes depuis un fichier"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_scenes = json.load(f)
                valid_scenes = {}
                for scene_name, scene_data in imported_scenes.items():
                    if isinstance(scene_data, dict):
                        valid_scenes[scene_name] = scene_data
                
                self.scenes.update(valid_scenes)
                return self.save_scenes_to_file()
        except Exception as e:
            print(f"Erreur lors de l'import: {e}")
            return False
    
    def get_scene_info(self, scene_name):
        """Retourne les informations d'une scène"""
        if scene_name not in self.scenes:
            return None
        
        scene_data = self.scenes[scene_name]
        
        if 'projectors' in scene_data:
            projectors_data = scene_data['projectors']
            has_effects = scene_data.get('effects') is not None
        else:
            projectors_data = scene_data
            has_effects = False
        
        info = {
            'name': scene_name,
            'projectors_count': len(projectors_data),
            'projectors_on': sum(1 for state in projectors_data.values() if state.get('is_on', False)),
            'colors': list(set(state.get('color', '#000000') for state in projectors_data.values())),
            'has_effects': has_effects
        }
        return info