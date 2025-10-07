import tkinter as tk
from projector import Projector
from effects_manager import EffectsManager
from scene_manager import SceneManager
from gui_components import ProjectorDisplay, ControlPanel, EffectsPanel, GlobalControlPanel
from config import *

class LightControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title(UI_CONFIG['window_title'])
        self.root.geometry(UI_CONFIG['window_geometry'])
        self.root.configure(bg=UI_CONFIG['background_color'])

        self.num_projectors = PROJECTOR_CONFIG['default_count']
        
        self.init_projectors()
        self.init_managers()
        self.init_gui()
        
        self.run_effects_loop()
    
    def init_projectors(self):
        """Initialise les projecteurs avec la configuration"""
        self.projectors = {}
        for i in range(self.num_projectors):
            self.projectors[i] = Projector(i)
            self.projectors[i].set_color(PROJECTOR_CONFIG['default_color'])
            self.projectors[i].set_intensity(PROJECTOR_CONFIG['default_intensity'])
    
    def init_managers(self):
        """Initialise les gestionnaires"""
        self.effects_manager = EffectsManager(self.projectors)
        self.scene_manager = SceneManager(self.projectors, self.effects_manager)
    
    def init_gui(self):
        """Initialise l'interface graphique"""
        main_frame = tk.Frame(self.root, bg=UI_CONFIG['background_color'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === ZONE D'AFFICHAGE DES PROJECTEURS ===
        self.create_display_area(main_frame)
        
        # === CONSOLE DE CONTRÔLE ===
        self.create_control_console(main_frame)
    
    def create_display_area(self, parent):
        """Crée la zone d'affichage des projecteurs"""
        display_frame = tk.Frame(parent, bg=UI_CONFIG['panel_color'], relief='sunken', bd=3)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(display_frame, text=LABELS['projection_screen'], 
                bg=UI_CONFIG['panel_color'], fg="white", font=('Arial', 10, 'bold')).pack(pady=5)
        
        canvas_config = DISPLAY_CONFIG
        self.canvas = tk.Canvas(display_frame, 
                               width=min(canvas_config['canvas_width'], 1180),
                               height=canvas_config['canvas_height'], 
                               bg="black")
        self.canvas.pack(pady=10)
        
        self.projector_display = ProjectorDisplay(self.canvas, self.projectors)
    
    def create_control_console(self, parent):
        """Crée la console de contrôle avec répartition ajustée"""
        console_frame = tk.Frame(parent, bg=UI_CONFIG['panel_color'], relief='sunken', bd=3)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(console_frame, text=LABELS['dmx_console'], 
                bg=UI_CONFIG['panel_color'], fg="white", font=('Arial', 14, 'bold')).pack(pady=5)
        
        left_panel = tk.Frame(console_frame, bg=UI_CONFIG['control_color'], 
                             relief='raised', bd=2, width=280)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left_panel.pack_propagate(False)
        
        self.control_panel = ControlPanel(
            left_panel, 
            self.projectors, 
            self.on_projector_select,
            self.on_intensity_change
        )
        
        center_panel = tk.Frame(console_frame, bg=UI_CONFIG['control_color'], 
                               relief='raised', bd=2, width=270)
        center_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        center_panel.pack_propagate(False)
        
        self.effects_panel = EffectsPanel(
            center_panel, 
            self.effects_manager,
            self.get_selected_projector
        )
        
        right_panel = tk.Frame(console_frame, bg=UI_CONFIG['control_color'], 
                              relief='raised', bd=2)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.global_panel = GlobalControlPanel(right_panel, self.projectors, self.scene_manager)
    
    def run_effects_loop(self):
        """Boucle principale pour les effets"""
        self.effects_manager.process_all_effects()
        self.projector_display.update_all_projectors()
        self.effects_panel.update_status_indicators()
        self.control_panel.update_info_display()
        self.root.after(EFFECTS_CONFIG['loop_interval'], self.run_effects_loop)
    
    def get_selected_projector(self):
        """Retourne l'ID du projecteur actuellement sélectionné"""
        return self.control_panel.selected_projector
    
    def on_projector_select(self, projector_id):
        """Callback lors de la sélection d'un projecteur"""
        pass
    
    def on_intensity_change(self, projector_id, intensity):
        """Callback lors du changement d'intensité"""
        pass