
from model import Model
from view import View
from CryptDecrypt.ControllerAsym import ControllerAsym
import tkinter


class Controller():
    def __init__(self, root):
        # Définir la fenêtre
        self.root = root

        # Creation des instances
        self.model = Model(self)
        self.view = View(self, self.root)
        self.view.start()

        # Variable de la modale
        self.modal_window = None

    # Mettre à jour les variables du model
    def update_variable(self, var, value):
        setattr(self.model, var, value)
        #print(f"Variable {var} mise à jour : {getattr(self.model, var)}")

    # Demander ou enregistrer la clé
    def save_key_file(self):
        path = self.view.save_key_file_box()
        return path

    # Afficher message box
    def show_message(self, title, message):
        self.view.message_box(title, message)

    # Bouton pour lancer le cryptage décryptage
    def encrypt_decrypt(self):
        self.model.encrypt_decrypt()

    # Stopper le processus
    def stop_process(self):
        self.model.encrypt_decrypt_file.stop_process()
        self.model.encrypt_decrypt_folder.stop_process()

    # Réinitialiser le bouton Encrypt Decrypt
    def reset_button(self):
        self.view.reset_button()

    # Commencer la barre de progression
    def start_task(self, max_progress):
        self.view.start_task(max_progress)

    # Mettre à jour la barre de progression
    def update_task(self, value, message):
        self.view.update_task(value, message)

    # Stopper la barre de progression
    def stop_task(self):
        self.view.stop_task()

    # Afficher Modal
    def show_modal(self):
        self.modal_window = tkinter.Toplevel(self.root)
        self.modal_window.protocol("WM_DELETE_WINDOW", self.close_modal)

        self.modal_window.grab_set()  # Désactive la fenêtre principale
        self.modal_window.focus_force()  # Mettre la fenêtre modale en focus
        # Instanciation du contrôleur et de ViewAsym dans la fenêtre modale
        controller = ControllerAsym(self.modal_window)
        controller.view.start()

    # Fermer la modale
    def close_modal(self):
        self.modal_window.destroy()
        
        # Réactiver la fenêtre principale après la fermeture de la fenêtre modale
        self.root.grab_release()
        self.view.modal_open = False
        
   