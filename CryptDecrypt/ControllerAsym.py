from .ViewAsym import ViewAsym
from .ModelAsym import ModelAsym
from threading import Thread


class ControllerAsym:
    def __init__(self, root):

        # Définir la fenêtre
        self.root = root

        # Creation des instances
        self.model = ModelAsym(self)
        self.view = ViewAsym(self, self.root)

    def generate_key_pair(self):
        generate_thread = Thread(target=self.model.generate_key_pair())
        generate_thread.start()

    def encrypt_file(self):
        encrypt_thread = Thread(target=self.model.encrypt_file())
        encrypt_thread.start()
        

    def decrypt_file(self):
        decrypt_thread = Thread(target=self.model.decrypt_file())
        decrypt_thread.start()
    
    def start_task(self, message):
        self.view.start_task(message)
        
    def stop_task(self):
        self.view.stop_task()
        
