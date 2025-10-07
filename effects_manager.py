"""
effects_manager.py - Gestionnaire des effets lumineux avec synchronisation des clignotements
Version avec support de sauvegarde/restauration d'état
"""
from config import EFFECTS_CONFIG

class EffectsManager:
    def __init__(self, projectors):
        self.projectors = projectors
        self.num_projectors = len(projectors)

        self.active_effects = {
            'strobe': {'active': False, 'step': 0},
            'fade': {'active': False, 'step': 0},
            'chaser': {'active': False, 'step': 0},
            'blink_all': {'active': False, 'step': 0},
            'individual_blinks': {}
        }
        
        self.fade_colors = EFFECTS_CONFIG['default_fade_colors']
        self.blink_speed = EFFECTS_CONFIG['blink_speed']
        self.strobe_speed = EFFECTS_CONFIG['strobe_speed']
        self.fade_speed = EFFECTS_CONFIG['fade_speed']
        self.chaser_speed = EFFECTS_CONFIG['chaser_speed']
        
        for i in range(self.num_projectors):
            self.active_effects['individual_blinks'][i] = {'active': False, 'step': 0}

    def get_state(self):
        """Retourne l'état complet des effets pour sauvegarde"""
        return {
            'strobe_active': self.active_effects['strobe']['active'],
            'fade_active': self.active_effects['fade']['active'],
            'chaser_active': self.active_effects['chaser']['active'],
            'blink_all_active': self.active_effects['blink_all']['active'],
            'individual_blinks_active': {
                str(i): self.active_effects['individual_blinks'][i]['active'] 
                for i in range(self.num_projectors)
            },
            'fade_colors': self.fade_colors.copy()
        }
    
    def set_state(self, state):
        """Restaure l'état complet des effets depuis une sauvegarde"""
        self.stop_all_effects()
        
        if 'fade_colors' in state:
            self.fade_colors = state['fade_colors'].copy()
        
        if 'individual_blinks_active' in state:
            for proj_id_str, is_active in state['individual_blinks_active'].items():
                proj_id = int(proj_id_str)
                if proj_id < self.num_projectors and is_active:
                    self.active_effects['individual_blinks'][proj_id]['active'] = True
                    self.active_effects['individual_blinks'][proj_id]['step'] = 0

        if state.get('blink_all_active', False):
            self.active_effects['blink_all']['active'] = True
            self.active_effects['blink_all']['step'] = 0

        if state.get('strobe_active', False):
            self.active_effects['strobe']['active'] = True
            self.active_effects['strobe']['step'] = 0

        if state.get('chaser_active', False):
            self.active_effects['chaser']['active'] = True
            self.active_effects['chaser']['step'] = 0
        
        if state.get('fade_active', False):
            self.active_effects['fade']['active'] = True
            self.active_effects['fade']['step'] = 0

    def process_all_effects(self):
        """Traite tous les effets actifs et met à jour les couleurs des projecteurs"""
        for projector_id, projector in self.projectors.items():
            final_color = self._calculate_final_color(projector_id, projector)
            projector.color = final_color

    def _calculate_final_color(self, projector_id, projector):
        """Calcule la couleur finale d'un projecteur en combinant tous les effets actifs"""
        if not projector.is_on:
            return '#000000'
        
        base_color = projector.base_color
        
        if self.active_effects['fade']['active']:
            base_color = self._get_fade_color()

        if self.active_effects['chaser']['active']:
            if not self._is_chaser_active_for_projector(projector_id):
                return '#000000'
            return base_color
        elif self.active_effects['strobe']['active']:
            if not self._is_strobe_active():
                return '#000000'
            return base_color
        else:
            has_blink_effects = (self.active_effects['blink_all']['active'] or 
                                self.active_effects['individual_blinks'][projector_id]['active'])
            
            if has_blink_effects:
                should_blink = self._is_blink_synchronized()
                if not should_blink:
                    return '#000000'
            return base_color

    def _get_fade_color(self):
        """Calcule la couleur actuelle pour l'effet fade avec cycle complet"""
        fade_data = self.active_effects['fade']
        fade_data['step'] = (fade_data['step'] + 1) % self.fade_speed
        half_speed = self.fade_speed // 2
        
        if fade_data['step'] <= half_speed:
            progress = fade_data['step'] / half_speed
        else:
            progress = (self.fade_speed - fade_data['step']) / half_speed

        return self._interpolate_colors(self.fade_colors[0], self.fade_colors[1], progress)

    def _interpolate_colors(self, color1, color2, progress):
        """Interpole entre deux couleurs hexadécimales"""
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)

        r = int(r1 + (r2 - r1) * progress)
        g = int(g1 + (g2 - g1) * progress)
        b = int(b1 + (b2 - b1) * progress)
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def _hex_to_rgb(self, hex_color):
        """Convertit une couleur hex en tuple RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _is_strobe_active(self):
        """Détermine si le strobe doit allumer les projecteurs"""
        strobe_data = self.active_effects['strobe']
        strobe_data['step'] = (strobe_data['step'] + 1) % self.strobe_speed
        return strobe_data['step'] < (self.strobe_speed // 3)

    def _is_chaser_active_for_projector(self, projector_id):
        """Détermine si un projecteur spécifique doit être allumé pour l'effet chaser"""
        chaser_data = self.active_effects['chaser']
        chaser_data['step'] = (chaser_data['step'] + 1) % (self.chaser_speed * self.num_projectors)
        
        active_projector = (chaser_data['step'] // self.chaser_speed) % self.num_projectors
        return projector_id == active_projector

    def _is_blink_synchronized(self):
        """Détermine l'état synchronisé pour tous les clignotements"""
        has_active_blink = (self.active_effects['blink_all']['active'] or 
                        any(self.active_effects['individual_blinks'][i]['active'] 
                            for i in range(self.num_projectors)))
        
        if not has_active_blink:
            return False  
        
        blink_all_data = self.active_effects['blink_all']
        blink_all_data['step'] = (blink_all_data['step'] + 1) % self.blink_speed
        
        is_on = blink_all_data['step'] < (self.blink_speed // 2)

        for i in range(self.num_projectors):
            if self.active_effects['individual_blinks'][i]['active']:
                self.active_effects['individual_blinks'][i]['step'] = blink_all_data['step']
        
        return is_on

    def _stop_rhythm_effects_except_blinks(self):
        """Arrête tous les effets de rythme sauf les clignotements"""
        self.active_effects['strobe']['active'] = False
        self.active_effects['strobe']['step'] = 0
        self.active_effects['chaser']['active'] = False
        self.active_effects['chaser']['step'] = 0

    def _stop_rhythm_effects(self):
        """Arrête tous les effets de rythme"""
        self.active_effects['strobe']['active'] = False
        self.active_effects['strobe']['step'] = 0
        self.active_effects['chaser']['active'] = False
        self.active_effects['chaser']['step'] = 0
        self.active_effects['blink_all']['active'] = False
        self.active_effects['blink_all']['step'] = 0
        
        for i in range(self.num_projectors):
            self.active_effects['individual_blinks'][i]['active'] = False
            self.active_effects['individual_blinks'][i]['step'] = 0

    def toggle_blink(self, projector_id):
        """Active/désactive le clignotement d'un projecteur spécifique"""
        if projector_id >= self.num_projectors:
            return False
        
        blink_data = self.active_effects['individual_blinks'][projector_id]
        
        if blink_data['active']:
            blink_data['active'] = False
            blink_data['step'] = 0
        else:
            self._stop_rhythm_effects_except_blinks()
            blink_data['active'] = True
            blink_data['step'] = 0
        
        return blink_data['active']

    def toggle_blink_all(self):
        """Active/désactive le clignotement collectif de tous les projecteurs"""
        blink_all_data = self.active_effects['blink_all']
        
        if blink_all_data['active']:
            blink_all_data['active'] = False
            blink_all_data['step'] = 0
        else:
            self._stop_rhythm_effects_except_blinks()
            blink_all_data['active'] = True
            blink_all_data['step'] = 0
        
        return blink_all_data['active']

    def toggle_strobe(self):
        """Active/désactive l'effet strobe"""
        strobe_data = self.active_effects['strobe']
        
        if strobe_data['active']:
            strobe_data['active'] = False
            strobe_data['step'] = 0
        else:
            self._stop_rhythm_effects()
            strobe_data['active'] = True
            strobe_data['step'] = 0
        
        return strobe_data['active']

    def toggle_chaser(self):
        """Active/désactive l'effet chaser"""
        chaser_data = self.active_effects['chaser']
        
        if chaser_data['active']:
            chaser_data['active'] = False
            chaser_data['step'] = 0
        else:
            self._stop_rhythm_effects()
            chaser_data['active'] = True
            chaser_data['step'] = 0
        
        return chaser_data['active']

    def toggle_fade(self):
        """Active/désactive l'effet de fondu"""
        fade_data = self.active_effects['fade']
        
        if fade_data['active']:
            fade_data['active'] = False
            fade_data['step'] = 0
            for projector in self.projectors.values():
                projector.color = projector.base_color
        else:
            fade_data['active'] = True
            fade_data['step'] = 0
        
        return fade_data['active']

    def set_fade_colors(self, color1, color2):
        """Définit les couleurs pour l'effet fade"""
        self.fade_colors = [color1, color2]

    def stop_all_effects(self):
        """Arrête tous les effets"""
        self.active_effects['strobe']['active'] = False
        self.active_effects['strobe']['step'] = 0
        self.active_effects['fade']['active'] = False
        self.active_effects['fade']['step'] = 0
        self.active_effects['chaser']['active'] = False
        self.active_effects['chaser']['step'] = 0
        self.active_effects['blink_all']['active'] = False 
        self.active_effects['blink_all']['step'] = 0
        
        for i in range(self.num_projectors):
            self.active_effects['individual_blinks'][i]['active'] = False
            self.active_effects['individual_blinks'][i]['step'] = 0
        
        for projector in self.projectors.values():
            projector.color = projector.base_color

    def get_effects_status(self):
        """Retourne l'état de tous les effets"""
        return {
            'strobe': self.active_effects['strobe']['active'],
            'fade': self.active_effects['fade']['active'],
            'chaser': self.active_effects['chaser']['active'],
            'blink_all': self.active_effects['blink_all']['active'],
            'individual_blinks': {
                i: data['active'] 
                for i, data in self.active_effects['individual_blinks'].items()
            }
        }