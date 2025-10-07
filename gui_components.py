"""
gui_components.py - Composants de l'interface utilisateur utilisant config.py
Version avec support de suppression de scènes
"""
import tkinter as tk
from tkinter import colorchooser, messagebox, simpledialog
from config import DISPLAY_CONFIG, BUTTON_STYLES, LABELS, MESSAGES, UI_CONFIG

class ProjectorDisplay:
    """Affichage des projecteurs sur le canvas"""
    
    def __init__(self, canvas, projectors):
        self.canvas = canvas
        self.projectors = projectors
        self.create_projector_rectangles()
    
    def create_projector_rectangles(self):
        """Crée les rectangles visuels des projecteurs avec config"""
        config = DISPLAY_CONFIG
        
        for i, projector in self.projectors.items():
            x1 = config['start_x'] + i * (config['projector_width'] + config['spacing'])
            x2 = x1 + config['projector_width']
            y1 = 20
            y2 = y1 + config['projector_height']
            
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="#666", width=3)
            projector.rect = rect
            
            text_x = x1 + config['projector_width'] // 2
            text_y = y1 - 10
            self.canvas.create_text(text_x, text_y, text=f"PROJ {i+1}", 
                                  fill="yellow", font=("Arial", 12, 'bold'))
    
    def update_projector(self, projector_id):
        """Met à jour l'affichage d'un projecteur"""
        projector = self.projectors[projector_id]
        color = projector.get_dimmed_color()
        self.canvas.itemconfig(projector.rect, fill=color)
    
    def update_all_projectors(self):
        """Met à jour l'affichage de tous les projecteurs"""
        for i in self.projectors.keys():
            self.update_projector(i)

class ControlPanel:
    """Panneau de contrôle des projecteurs"""
    def __init__(self, parent, projectors, on_projector_select, on_intensity_change):
        self.parent = parent
        self.projectors = projectors
        self.selected_projector = 0
        self.on_projector_select = on_projector_select
        self.on_intensity_change = on_intensity_change
        
        self.projector_buttons = []
        self.intensity_scale = None
        self.info_label = None
        
        self.create_controls()
    
    def create_controls(self):
        """Crée les contrôles de sélection et d'intensité"""
        default_style = BUTTON_STYLES['default']
        on_off_style = BUTTON_STYLES['on_off']
        color_style = BUTTON_STYLES['color']
        selected_style = BUTTON_STYLES['selected']
        
        tk.Label(self.parent, text=LABELS['projector_selection'], 
                bg=UI_CONFIG['control_color'], fg="white", font=('Arial', 10, 'bold')).pack(pady=5)
        
        selection_frame = tk.Frame(self.parent, bg=UI_CONFIG['control_color'])
        selection_frame.pack(pady=5)
        
        for i in range(len(self.projectors)):
            btn = tk.Button(selection_frame, text=f"P{i+1}", width=6, height=2,
                           command=lambda x=i: self.select_projector(x), **default_style)
            btn.grid(row=0, column=i, padx=2)
            self.projector_buttons.append(btn)
        
        self.projector_buttons[0].config(bg=selected_style['bg'])
        
        tk.Label(self.parent, text=LABELS['individual_controls'], 
                bg=UI_CONFIG['control_color'], fg="white", font=('Arial', 10, 'bold')).pack(pady=(20, 5))
        
        individual_frame = tk.Frame(self.parent, bg=UI_CONFIG['control_color'])
        individual_frame.pack(pady=5)
        
        self.btn_on = tk.Button(individual_frame, text=LABELS['on_off'], width=12, height=2,
                               command=self.toggle_light, **on_off_style)
        self.btn_on.pack(pady=2)

        self.btn_color = tk.Button(individual_frame, text=LABELS['color'], width=12, height=2,
                                  command=self.pick_color, **color_style)
        self.btn_color.pack(pady=2)
        
        tk.Label(self.parent, text=LABELS['dmx_intensity'], 
                bg=UI_CONFIG['control_color'], fg="white", font=('Arial', 10, 'bold')).pack(pady=(20, 5))
        
        self.intensity_scale = tk.Scale(self.parent, from_=0, to=100, orient=tk.HORIZONTAL, 
                                       length=150, command=self.on_intensity_changed,
                                       bg='#444444', fg='white', highlightbackground=UI_CONFIG['control_color'],
                                       troughcolor='#666666', font=('Arial', 8))
        self.intensity_scale.set(100)
        self.intensity_scale.pack(pady=5)
        self.info_label = tk.Label(self.parent, text="", bg=UI_CONFIG['control_color'], fg="white", 
                                  font=('Arial', 8), wraplength=180)
        self.info_label.pack(pady=10)
        
        self.update_info_display()
    
    def select_projector(self, projector_id):
        """Sélectionne un projecteur"""
        for btn in self.projector_buttons:
            btn.config(bg=BUTTON_STYLES['default']['bg'])
        
        self.projector_buttons[projector_id].config(bg=BUTTON_STYLES['selected']['bg'])
        self.selected_projector = projector_id
        
        self.intensity_scale.set(self.projectors[projector_id].intensity)
        
        self.update_info_display()
        self.on_projector_select(projector_id)
    
    def toggle_light(self):
        """Active/désactive le projecteur sélectionné"""
        self.projectors[self.selected_projector].toggle()
        self.update_info_display()
    
    def pick_color(self):
        """Ouvre le sélecteur de couleur"""
        color_code = colorchooser.askcolor(title=MESSAGES['color_picker_title'])[1]
        if color_code:
            self.projectors[self.selected_projector].set_color(color_code)
            self.update_info_display()
    
    def on_intensity_changed(self, value):
        """Callback pour le changement d'intensité"""
        intensity = int(value)
        self.projectors[self.selected_projector].set_intensity(intensity)
        self.update_info_display()
        self.on_intensity_change(self.selected_projector, intensity)
    
    def update_info_display(self):
        """Met à jour l'affichage des informations du projecteur"""
        projector = self.projectors[self.selected_projector]
        status = "ON" if projector.is_on else "OFF"
        info_text = (f"PROJ {self.selected_projector + 1}\n{status}\n"
                    f"Couleur: {projector.base_color}\n"
                    f"Intensité: {projector.intensity}%")
        self.info_label.config(text=info_text)

class EffectsPanel:
    """Panneau des effets spéciaux avec exclusion mutuelle"""   
    def __init__(self, parent, effects_manager, get_selected_projector_callback):
        self.parent = parent
        self.effects_manager = effects_manager
        self.get_selected_projector = get_selected_projector_callback
        self.status_labels = {}
        
        self.create_effects_controls()
    
    def create_effects_controls(self):
        """Crée les contrôles d'effets"""
        default_style = BUTTON_STYLES['default']
        effect_style = BUTTON_STYLES['effect']
        stop_style = BUTTON_STYLES['stop']
        
        tk.Label(self.parent, text=LABELS['special_effects'], 
                bg=UI_CONFIG['control_color'], fg="white", font=('Arial', 10, 'bold')).pack(pady=5)
     
        rhythm_frame = tk.Frame(self.parent, bg=UI_CONFIG['control_color'])
        rhythm_frame.pack(pady=5)
        
        tk.Label(rhythm_frame, text="EFFETS DE RYTHME (exclusifs)", 
                bg=UI_CONFIG['control_color'], fg="yellow", font=('Arial', 8, 'bold')).pack()
        
        rhythm_buttons_frame = tk.Frame(rhythm_frame, bg=UI_CONFIG['control_color'])
        rhythm_buttons_frame.pack(pady=2)
        
        self.btn_blink = tk.Button(rhythm_buttons_frame, text=LABELS['blink'], width=8, height=2,
                                  command=self.toggle_blink, **effect_style)
        self.btn_blink.grid(row=0, column=0, padx=1, pady=2)
        
        self.btn_blink_all = tk.Button(rhythm_buttons_frame, text=LABELS['blink_all'], width=8, height=2,
                                      command=self.toggle_blink_all, **effect_style)
        self.btn_blink_all.grid(row=0, column=1, padx=1, pady=2)
        
        self.btn_strobe = tk.Button(rhythm_buttons_frame, text=LABELS['strobe'], width=8, height=2,
                                   command=self.toggle_strobe, **effect_style)
        self.btn_strobe.grid(row=1, column=0, padx=1, pady=2)
        
        self.btn_chaser = tk.Button(rhythm_buttons_frame, text=LABELS['chaser'], width=8, height=2,
                                   command=self.toggle_chaser, **effect_style)
        self.btn_chaser.grid(row=1, column=1, padx=1, pady=2)
        
        fade_frame = tk.Frame(self.parent, bg=UI_CONFIG['control_color'])
        fade_frame.pack(pady=5)
        
        tk.Label(fade_frame, text="EFFET DE COULEUR (compatible)", 
                bg=UI_CONFIG['control_color'], fg="lightgreen", font=('Arial', 8, 'bold')).pack()
        
        self.btn_fade = tk.Button(fade_frame, text=LABELS['fade'], width=21, height=2,
                                 command=self.toggle_fade, **effect_style)
        self.btn_fade.pack(pady=2)
 
        config_frame = tk.Frame(self.parent, bg=UI_CONFIG['control_color'])
        config_frame.pack(pady=10)
        
        tk.Label(config_frame, text=LABELS['effects_config'], 
                bg=UI_CONFIG['control_color'], fg="white", font=('Arial', 10, 'bold')).pack()
        
        self.btn_fade_colors = tk.Button(config_frame, text=LABELS['fade_colors'], width=15,
                                        command=self.set_fade_colors, **default_style)
        self.btn_fade_colors.pack(pady=2)
        
        self.btn_stop_effects = tk.Button(config_frame, text=LABELS['stop_effects'], width=15, height=2,
                                         command=self.stop_all_effects, **stop_style)
        self.btn_stop_effects.pack(pady=5)
        
        self.create_status_indicators(config_frame)
    
    def create_status_indicators(self, parent):
        """Crée les indicateurs d'état des effets"""
        status_frame = tk.Frame(parent, bg=UI_CONFIG['control_color'])
        status_frame.pack(pady=5)
        
        tk.Label(status_frame, text=LABELS['active_effects'], 
                bg=UI_CONFIG['control_color'], fg="white", font=('Arial', 8, 'bold')).pack()
        
        self.status_labels = {
            'rhythm': tk.Label(status_frame, text="RYTHME: OFF", 
                              bg=UI_CONFIG['control_color'], fg="gray", font=('Arial', 7)),
            'fade': tk.Label(status_frame, text="FONDU: OFF", 
                            bg=UI_CONFIG['control_color'], fg="gray", font=('Arial', 7))
        }
        
        for label in self.status_labels.values():
            label.pack()
    
    def _update_rhythm_buttons(self, active_effect=None):
        """Met à jour l'apparence des boutons de rythme"""
        normal_bg = BUTTON_STYLES['effect']['bg']
        active_bg = '#ff4400'
        
        self.btn_blink.config(bg=normal_bg)
        self.btn_blink_all.config(bg=normal_bg)
        self.btn_strobe.config(bg=normal_bg)
        self.btn_chaser.config(bg=normal_bg)
        
        if active_effect == 'blink':
            self.btn_blink.config(bg=active_bg)
        elif active_effect == 'blink_all':
            self.btn_blink_all.config(bg=active_bg)
        elif active_effect == 'strobe':
            self.btn_strobe.config(bg=active_bg)
        elif active_effect == 'chaser':
            self.btn_chaser.config(bg=active_bg)
    
    def toggle_blink(self):
        """Active/désactive le clignotement du projecteur sélectionné"""
        selected_id = self.get_selected_projector()
        if selected_id is not None:
            is_active = self.effects_manager.toggle_blink(selected_id)
            if is_active:
                self._update_rhythm_buttons('blink')
            else:
                self._update_rhythm_buttons()
    
    def toggle_blink_all(self):
        """Active/désactive le clignotement collectif"""
        is_active = self.effects_manager.toggle_blink_all()
        if is_active:
            self._update_rhythm_buttons('blink_all')
        else:
            self._update_rhythm_buttons()
    
    def toggle_strobe(self):
        """Active/désactive l'effet strobe"""
        is_active = self.effects_manager.toggle_strobe()
        if is_active:
            self._update_rhythm_buttons('strobe')
        else:
            self._update_rhythm_buttons()
    
    def toggle_chaser(self):
        """Active/désactive l'effet chaser"""
        is_active = self.effects_manager.toggle_chaser()
        if is_active:
            self._update_rhythm_buttons('chaser')
        else:
            self._update_rhythm_buttons()
    
    def toggle_fade(self):
        """Active/désactive l'effet de fondu"""
        is_active = self.effects_manager.toggle_fade()
        if is_active:
            self.btn_fade.config(bg='#ff4400')
        else:
            self.btn_fade.config(bg=BUTTON_STYLES['effect']['bg'])
    
    def stop_all_effects(self):
        """Arrête tous les effets"""
        self.effects_manager.stop_all_effects()
        self._update_rhythm_buttons()
        self.btn_fade.config(bg=BUTTON_STYLES['effect']['bg'])
    
    def set_fade_colors(self):
        """Configure les couleurs du fondu"""
        color1 = colorchooser.askcolor(title=MESSAGES['fade_color1_title'])[1]
        if color1:
            color2 = colorchooser.askcolor(title=MESSAGES['fade_color2_title'])[1]
            if color2:
                self.effects_manager.set_fade_colors(color1, color2)
                messagebox.showinfo(MESSAGES['fade_colors_title'], 
                                  MESSAGES['fade_configured'].format(color1=color1, color2=color2))
    
    def update_status_indicators(self):
        """Met à jour les indicateurs d'état des effets"""
        status = self.effects_manager.get_effects_status()
        
        rhythm_active = None
        if status['strobe']:
            rhythm_active = "STROBE"
        elif status['chaser']:
            rhythm_active = "CHASER"
        elif status['blink_all']:
            rhythm_active = "BLINK ALL"
        elif any(status['individual_blinks'].values()):
            active_blinks = [str(i+1) for i, active in status['individual_blinks'].items() if active]
            rhythm_active = f"BLINK P{',P'.join(active_blinks)}"
        
        if rhythm_active:
            self.status_labels['rhythm'].config(text=f"RYTHME: {rhythm_active}", fg="lime")
        else:
            self.status_labels['rhythm'].config(text="RYTHME: OFF", fg="gray")
        
        if status['fade']:
            self.status_labels['fade'].config(text="FONDU: ON", fg="lime")
        else:
            self.status_labels['fade'].config(text="FONDU: OFF", fg="gray")

class GlobalControlPanel:
    """Panneau des contrôles globaux et scènes avec suppression"""
    
    def __init__(self, parent, projectors, scene_manager):
        self.parent = parent
        self.projectors = projectors
        self.scene_manager = scene_manager
        self.scene_buttons = []
        
        self.create_global_controls()
    
    def create_global_controls(self):

        """Crée les contrôles globaux"""
        default_style = BUTTON_STYLES['default']
        on_off_style = BUTTON_STYLES['on_off']
        stop_style = BUTTON_STYLES['stop']
        scene_style = BUTTON_STYLES['scene']
        programmed_style = BUTTON_STYLES['programmed']
        
        tk.Label(self.parent, text=LABELS['global_controls'], 
                bg=UI_CONFIG['control_color'], fg="white", font=('Arial', 10, 'bold')).pack(pady=5)
        
        global_frame = tk.Frame(self.parent, bg=UI_CONFIG['control_color'])
        global_frame.pack(pady=5)
        
        self.btn_all_on = tk.Button(global_frame, text=LABELS['all_on'], width=8, height=3,
                                   command=self.all_lights_on, **on_off_style)
        self.btn_all_on.grid(row=0, column=0, padx=2, pady=2)
        
        self.btn_all_off = tk.Button(global_frame, text=LABELS['all_off'], width=8, height=3,
                                    command=self.all_lights_off, **stop_style)
        self.btn_all_off.grid(row=0, column=1, padx=2, pady=2)
        
        tk.Label(self.parent, text=LABELS['scene_memory'], 
                bg=UI_CONFIG['control_color'], fg="white", font=('Arial', 10, 'bold')).pack(pady=(15, 8))
        
        scenes_frame = tk.Frame(self.parent, bg=UI_CONFIG['control_color'])
        scenes_frame.pack(pady=8)
        
        scenes_row1 = tk.Frame(scenes_frame, bg=UI_CONFIG['control_color'])
        scenes_row1.pack(pady=3)
        
        self.btn_save_scene = tk.Button(scenes_row1, text=LABELS['save_scene'], width=8, height=2,
                                       command=self.save_scene, **scene_style)
        self.btn_save_scene.grid(row=0, column=0, padx=2, pady=2)
        
        self.btn_load_scene = tk.Button(scenes_row1, text=LABELS['load_scene'], width=8, height=2,
                                       command=self.load_scene, **scene_style)
        self.btn_load_scene.grid(row=0, column=1, padx=2, pady=2)
        
        scenes_row2 = tk.Frame(scenes_frame, bg=UI_CONFIG['control_color'])
        scenes_row2.pack(pady=3)
        
        self.btn_delete_scene = tk.Button(scenes_row2, text="SUPPR\nSCÈNE", width=17, height=2,
                                         command=self.delete_scene, **stop_style)
        self.btn_delete_scene.pack()
        
        tk.Label(self.parent, text=LABELS['quick_recall'], 
                bg=UI_CONFIG['control_color'], fg="white", font=('Arial', 10, 'bold')).pack(pady=(18, 8))
        
        quick_scenes_frame = tk.Frame(self.parent, bg=UI_CONFIG['control_color'])
        quick_scenes_frame.pack(pady=8)
        
      
        for i in range(UI_CONFIG['quick_scenes_count']):
            btn = tk.Button(quick_scenes_frame, text=f"S{i+1}", width=4, height=2,
                           command=lambda x=i: self.recall_quick_scene(x), **default_style)
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.scene_buttons.append(btn)

        clear_quick_frame = tk.Frame(self.parent, bg=UI_CONFIG['control_color'])
        clear_quick_frame.pack(pady=(12, 8))
        
        self.btn_clear_quick = tk.Button(clear_quick_frame, text="EFFACER\nSCÈNES RAPIDES", 
                                        width=17, height=2, **stop_style,
                                        command=self.clear_quick_scenes)
        self.btn_clear_quick.pack()
        self.update_quick_scene_buttons()
    
    def all_lights_on(self):
        """Allume tous les projecteurs"""
        for projector in self.projectors.values():
            projector.turn_on()
    
    def all_lights_off(self):
        """Éteint tous les projecteurs"""
        for projector in self.projectors.values():
            projector.turn_off()
    
    def save_scene(self):
        """Sauvegarde une nouvelle scène"""
        scene_name = simpledialog.askstring(MESSAGES['save_scene_title'], 
                                           MESSAGES['save_scene_prompt'])
        if scene_name and scene_name.strip():
            if scene_name.startswith('Quick_'):
                messagebox.showerror("Erreur", "Le nom ne peut pas commencer par 'Quick_'")
                return
                
            if self.scene_manager.save_scene(scene_name.strip()):
                messagebox.showinfo(MESSAGES['save_scene_title'], 
                                  MESSAGES['scene_saved'].format(name=scene_name.strip()))
            else:
                messagebox.showerror("Erreur", "Erreur lors de la sauvegarde")
    
    def load_scene(self):
        """Charge une scène existante"""
        scene_list = self.scene_manager.get_scene_list()
        if not scene_list:
            messagebox.showwarning(MESSAGES['load_scene_title'], MESSAGES['no_scenes'])
            return
        
        scene_name = simpledialog.askstring(MESSAGES['load_scene_title'], 
            MESSAGES['load_scene_prompt'].format(scenes=', '.join(scene_list)))
        
        if scene_name and scene_name.strip():
            if self.scene_manager.load_scene(scene_name.strip()):
                messagebox.showinfo(MESSAGES['load_scene_title'], 
                                  MESSAGES['scene_loaded'].format(name=scene_name.strip()))
            else:
                messagebox.showerror("Erreur", 
                                   MESSAGES['scene_not_found'].format(name=scene_name.strip()))
    
    def delete_scene(self):
        """Supprime une scène existante"""
        scene_list = self.scene_manager.get_scene_list()
        if not scene_list:
            messagebox.showwarning("Supprimer une scène", MESSAGES['no_scenes'])
            return
        
        scene_name = simpledialog.askstring("Supprimer une scène", 
            f"Scènes disponibles: {', '.join(scene_list)}\nNom de la scène à supprimer:")
        
        if scene_name and scene_name.strip():
            if messagebox.askyesno("Confirmation", 
                                 f"Êtes-vous sûr de vouloir supprimer la scène '{scene_name.strip()}'?"):
                if self.scene_manager.delete_scene(scene_name.strip()):
                    messagebox.showinfo("Suppression", f"Scène '{scene_name.strip()}' supprimée!")
                else:
                    messagebox.showerror("Erreur", 
                                       f"Impossible de supprimer la scène '{scene_name.strip()}'")
    
    def recall_quick_scene(self, scene_index):
        """Gère les scènes de rappel rapide"""
        if self.scene_manager.has_quick_scene(scene_index):
            if self.scene_manager.load_quick_scene(scene_index):
                messagebox.showinfo("Rappel rapide", f"Scène rapide {scene_index+1} chargée!")
            else:
                messagebox.showerror("Erreur", f"Erreur lors du chargement de la scène rapide {scene_index+1}")
        else:
            if self.scene_manager.save_quick_scene(scene_index):
                self.scene_buttons[scene_index].config(bg=BUTTON_STYLES['programmed']['bg'])
                messagebox.showinfo("Programmation", 
                                  MESSAGES['quick_scene_programmed'].format(number=scene_index+1))
            else:
                messagebox.showerror("Erreur", f"Erreur lors de la programmation de la scène rapide {scene_index+1}")
    
    def clear_quick_scenes(self):
        """Efface toutes les scènes rapides"""
        if messagebox.askyesno("Confirmation", 
                             "Êtes-vous sûr de vouloir effacer toutes les scènes rapides?"):
            cleared_count = 0
            for i in range(UI_CONFIG['quick_scenes_count']):
                if self.scene_manager.has_quick_scene(i):
                    if self.scene_manager.delete_quick_scene(i):
                        cleared_count += 1
            
            if cleared_count > 0:
                self.update_quick_scene_buttons()
                messagebox.showinfo("Effacement", f"{cleared_count} scènes rapides effacées!")
            else:
                messagebox.showinfo("Effacement", "Aucune scène rapide à effacer.")
    
    def update_quick_scene_buttons(self):
        """Met à jour l'apparence des boutons de scènes rapides"""
        for i, btn in enumerate(self.scene_buttons):
            if self.scene_manager.has_quick_scene(i):
                btn.config(bg=BUTTON_STYLES['programmed']['bg'])
            else:
                btn.config(bg=BUTTON_STYLES['default']['bg'])