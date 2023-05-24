from tkinter import filedialog, messagebox
from tkinter import ttk
import tkinter
from ttkthemes import ThemedStyle


class ViewAsym:
    def __init__(self, controller, root):
        self.controller = controller
        self.root = root
        
        self.root.configure(background='#f6f4f2') 

        self.root.title("Encryption Asymmetric")
        # Chemin vers le fichier d'icône
        #self.root.iconbitmap("@lock.xbm")
        
        # Récupérer les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculer les coordonnées x et y pour centrer la fenêtre
        x = (screen_width - 300) // 2
        y = (screen_height - 350) // 2
        # Définir la position de la fenêtre
        self.root.geometry(f'300x350+{x}+{y}')
        # Définition de la taille minimale de la fenêtre
        self.root.minsize(300, 350)
        self.root.resizable(0, 0)

        # Ajouter une liste déroulante pour choisir la taille de la clé
        self.key_sizes = [1024, 2048, 3072, 4096, 8192]

        # Creation des Frames
        self.frame = ttk.LabelFrame(self.root, text="RSA Encryption")
        # Configurer les Frames pour qu'il prennent toute la largeur
        self.frame.pack(fill='x', padx="20", pady="20")
        self.frame.grid_columnconfigure(0, weight=1)

        self.key_size_combobox = ttk.Combobox(
            self.frame, values=self.key_sizes, state="readonly")
        self.key_size_combobox.set("2048")  # Taille de clé par défaut
        self.key_size_combobox.grid(sticky="nesw", padx=10, pady=10)
        # Associer la fonction on_select à l'événement de sélection
        self.key_size_combobox.bind(
            "<<ComboboxSelected>>", self.on_key_size_select_change)

        # Ajouter un bouton pour générer la paire de clés
        self.key_button = ttk.Button(
            self.frame, text="Generate a key pair", command=self.controller.generate_key_pair)
        self.key_button.grid(sticky="nesw", padx=10, pady=10)

        # Ajouter un bouton pour chiffrer un fichier
        self.encrypt_button = ttk.Button(
            self.frame, text="Encrypt a file", command=self.controller.encrypt_file)
        self.encrypt_button.grid(sticky="nesw", padx=10, pady=10)

        # Ajouter un bouton pour déchiffrer un fichier
        self.decrypt_button = ttk.Button(
            self.frame, text="Decrypt a file", command=self.controller.decrypt_file)
        self.decrypt_button.grid(sticky="snew", padx=10, pady=10)

        # Creation du progress bar
        self.progress = ttk.Progressbar(
            self.frame, orient='horizontal', mode='determinate')
        self.progress.grid(sticky='wens', padx=10, pady=(10,0))
        
        # Creation d'un label pour affichier le fichier qu'il traite
        self.label_progress = ttk.Label(
            self.frame, text="Waiting ...", justify="right", anchor="e")
        self.label_progress.grid(
            sticky="w", padx=10, pady=(0,10))

    # Demander à l'utilisateur l'emplacement de sauvegarde du fichier
    def save_file(self, title, message, extension):

        path = filedialog.asksaveasfilename(
            parent=self.root,
            defaultextension=extension,
            filetypes=[(message, "*"+extension)],
            title=title
        )
        if not path:
            return

        return path

    # Charger les fichiers

    def open_file(self, title, extension):
        file_path = filedialog.askopenfilename(
            parent=self.root,
            title=title, filetypes=[("File " + extension, "*" + extension)])
        if not file_path:
            return
        return file_path

    # Quand le select des clés change
    def on_key_size_select_change(self, event):
        self.controller.model.key_size = self.key_size_combobox.get()

    # Stopper la progresse barre
    def start_task(self, message):
        self.progress.start()
        self.label_progress.config(text=message)
    
    # Stopper la progresse barre
    def stop_task(self):
        self.progress.stop()
        self.label_progress.config(text="Waiting ...")
        
    # Message box
    def message_box(self, title, message):
        # Création d'une fenêtre Toplevel pour la boîte de dialogue
        message_box = tkinter.Toplevel(self.root)
        message_box.title(title)
        message_box.configure(background="#f6f4f2")
        # Récupérer les dimensions de l'écran
        screen_width = message_box.winfo_screenwidth()
        screen_height = message_box.winfo_screenheight()
        # Calculer les coordonnées x et y pour centrer la fenêtre
        x = (screen_width - 250) // 2
        y = (screen_height - 100) // 2
        # Définir la position de la fenêtre
        message_box.geometry(f'250x100+{x}+{y}')
        # Définition de la taille minimale de la fenêtre
        message_box.minsize(250, 100)
        message_box.resizable(0, 0)
        
        # Contenu de la fenêtre de dialogue
        label = ttk.Label(message_box, text=message, font=('Arial', 15))
        label.pack(padx=20, pady=20)
        
        # Mise en focus de la fenêtre de dialogue
        message_box.focus_set()
        
    def start(self):
        style = ThemedStyle(self.root)
        style.set_theme("ubuntu")  # Thème initial
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Encrypto", 15))  # Remplacez "Arial" par la police souhaitée et 12 par la taille de police souhaitée
        self.root.mainloop()
