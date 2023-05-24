import tkinter
from tkinter import BOTH, filedialog, ttk, StringVar, BooleanVar, messagebox
from ttkthemes import ThemedStyle
from tkinter import font


class View:
    def __init__(self, controller, root):
        self.controller = controller
        self.root = root

        # Creation de la fenetre
        self.root.title('SecureAsym')
        self.root.configure(background='#f6f4f2') 
        
        # Chemin vers le fichier d'icône
        #self.root.iconbitmap("@lock.xbm")
        
        self.root.resizable(0, 0)
        # Récupérer les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculer les coordonnées x et y pour centrer la fenêtre
        x = (screen_width - 500) // 2
        y = (screen_height - 680) // 2
        # Définir la position de la fenêtre
        self.root.geometry(f'500x680+{x}+{y}')
        # Définition de la taille minimale de la fenêtre
        self.root.minsize(500, 680)
        
        police_speciale = font.Font(family="Encrypto", size=12, file="Encrypto.ttf")


        # Definir la variable pour choisir est ce qu'on crypt ou decrypt
        self.encrypt_or_decrypt = StringVar()
        self.encrypt_or_decrypt.set("Encrypt")

        # Definir la variable pour choisir si on crypt un fichier ou un dossier
        self.file_or_folder = StringVar()
        self.file_or_folder.set("File")

        # Definir la variable pour choisir le type d'encryption
        self.type_of_encryption = StringVar()
        self.type_of_encryption.set("AES")

        # Definir la variable pour choise la taille de la clé
        # Key Size disponibles
        self.key_sizes = ["128", "192", "256"]
        # Modes disponibles
        self.encrypt_mode = ["CBC", "ECB", "CFB", "OFB", "CTR"]

        # Definir la variable pour choisir si on genere une clé ou on utilise une existante
        self.choose_key_generate = StringVar()
        self.choose_key_generate.set("Generate")

        # Checkbox supprimer les fichier à la fin
        self.var_delete_files = BooleanVar()
        # Définition de la valeur initiale de la variable
        self.var_delete_files.set(False)
        
        # Variable de la modale pour ne pas ouvrir une autre
        self.modal_open = False

        # Creation des Frames
        self.frame_titre = ttk.Frame(self.root)
        self.frame_crypt_or_decrypt = ttk.Frame(self.root)
        self.frame_choose_file_encryption = ttk.Frame(self.root)
        self.frame_browse_file = ttk.Frame(self.root)
        self.frame_key = ttk.Frame(self.root)
        self.frame_crypt_button = ttk.Frame(self.root)
        self.frame_progress_bar = ttk.Frame(self.root)
        self.frame_button_asym = ttk.Frame(self.root)
        self.frame_button_help = ttk.Frame(self.root)

        # Configurer les Frames pour qu'il prennent toute la largeur
        self.frame_titre.pack(fill='x')
        self.frame_crypt_or_decrypt.pack(fill=BOTH)
        self.frame_choose_file_encryption.pack(fill=BOTH)
        self.frame_browse_file.pack(fill=BOTH)
        self.frame_key.pack(fill=BOTH)
        self.frame_crypt_button.pack(fill=BOTH)
        self.frame_progress_bar.pack(fill=BOTH)
        self.frame_button_asym.pack(fill='x')
        self.frame_button_help.pack(fill=BOTH)
        self.frame_crypt_or_decrypt.grid_columnconfigure(0, weight=1)
        self.frame_choose_file_encryption.grid_columnconfigure(0, weight=1)
        self.frame_choose_file_encryption.grid_columnconfigure(1, weight=1)
        self.frame_browse_file.grid_columnconfigure(0, weight=1)
        self.frame_key.grid_columnconfigure(0, weight=1)
        self.frame_crypt_button.grid_columnconfigure(0, weight=1)
        self.frame_progress_bar.grid_columnconfigure(0, weight=1)
        self.frame_button_asym.grid_columnconfigure(0, weight=1)
   
        
        # Creation du titre
        self.label_titre = ttk.Label(
            self.frame_titre, text="SecureAsym", font=(police_speciale)).pack()

        # Creation pour choisir crypter ou décrypter
        # Creation du LabelFrame choisir crypter ou décrypter
        self.label_frame_crypt_or_decrypt = ttk.LabelFrame(
            self.frame_crypt_or_decrypt, text="Choose what you want to do")
        self.label_frame_crypt_or_decrypt.grid(
            row=0, column=0, sticky='nwes', padx=10, pady=10)
        # Configurer les Frames pour qu'il prennent toute la largeur
        self.label_frame_crypt_or_decrypt.grid_columnconfigure(0, weight=1)
        self.label_frame_crypt_or_decrypt.grid_columnconfigure(1, weight=1)
        self.label_frame_crypt_or_decrypt.grid_columnconfigure(2, weight=1)

        self.radio1_crypt_or_decrypt = ttk.Radiobutton(self.label_frame_crypt_or_decrypt, text="Encrypt",
                                                           variable=self.encrypt_or_decrypt, value="Encrypt", command=self.on_radio_button_crypt_decrypt_change).grid(row=0, column=0, sticky="nesw", padx=10)
        self.radio2_crypt_or_decrypt = ttk.Radiobutton(self.label_frame_crypt_or_decrypt, text="Decrypt",
                                                           variable=self.encrypt_or_decrypt, value="Decrypt", command=self.on_radio_button_crypt_decrypt_change).grid(row=0, column=1, sticky="nesw", padx=10)
        self.radio3_crypt_or_decrypt = ttk.Radiobutton(self.label_frame_crypt_or_decrypt, text="Generate a key",
                                                           variable=self.encrypt_or_decrypt, value="Generate a key", command=self.on_radio_button_crypt_decrypt_change).grid(row=0, column=2, sticky="nesw", padx=10)

        # Creation choisir dossier ou fichier
        # Creation du LabelFrame File/Folder
        self.label_frame_file_folder = ttk.LabelFrame(
            self.frame_choose_file_encryption, text="Choose a type to encrypt")
        self.label_frame_file_folder.grid(
            row=0, column=0, sticky='snew', padx=10, pady=(0, 10))
        # Definir la variable pour choisir
        self.radio1_file_folder = ttk.Radiobutton(self.label_frame_file_folder, text="Encrypt a File",
                                                      variable=self.file_or_folder, value="File", command=lambda:
                                                      self.on_radio_button_file_folder_change())
        self.radio1_file_folder.grid(
            row=0, column=0, sticky='w', padx=10, pady=(0, 0))
        self.radio2_file_folder = ttk.Radiobutton(self.label_frame_file_folder, text="Encrypt a Folder",
                                                      variable=self.file_or_folder, value="Folder", command=lambda:
                                                      self.on_radio_button_file_folder_change())
        self.radio2_file_folder.grid(
            row=1, column=0, sticky='w', padx=10, pady=(0, 0))

        # Creation choisir type d'encryption
        # Creation du LabelFrame Choose Encrypt Symmetric
        self.label_frame_choose_encrypt = ttk.LabelFrame(
            self.frame_choose_file_encryption, text="Symmetric encryption")
        self.label_frame_choose_encrypt.grid(
            row=0, column=1, sticky='snew', padx=(0, 10), pady=(0, 10))
        self.radio1_encrypt = ttk.Radiobutton(self.label_frame_choose_encrypt, text="AES",
                                                  variable=self.type_of_encryption, value="AES", command=lambda: self.on_type_encryption_change()).grid(row=0, column=0, sticky='w', padx=10, pady=(0, 0))
        self.radio2_encrypt = ttk.Radiobutton(self.label_frame_choose_encrypt, text="ChaCha20",
                                                  variable=self.type_of_encryption, value="ChaCha20", command=lambda: self.on_type_encryption_change()).grid(row=1, column=0, sticky='w', padx=10, pady=(0, 0))

        # Création de la liste déroulante
        # Creation du LabelFrame Choose Key Size
        self.label_frame_choose_key_mode = ttk.LabelFrame(
            self.frame_choose_file_encryption, text="Choose Key Size - Encryption Mode")
        self.label_frame_choose_key_mode.grid(
            row=2, column=0, columnspan=3, sticky='nesw', padx=(10, 10))
        # Configurer les Frames pour qu'il prenent toute la largeur
        self.label_frame_choose_key_mode.grid_columnconfigure(0, weight=1)
        self.label_frame_choose_key_mode.grid_columnconfigure(1, weight=1)

        # Créer le select liste des key size
        self.label_frame_choose_key_size = ttk.LabelFrame(
            self.label_frame_choose_key_mode, text="Choose Key Size")
        self.label_frame_choose_key_size.grid(
            row=0, column=0, sticky='nesw', padx=10, pady=(0, 10))
        self.label_frame_choose_key_size.grid_columnconfigure(0, weight=1)

        self.key_size_combobox = ttk.Combobox(
            self.label_frame_choose_key_size, values=self.key_sizes, state="readonly")
        # Sélectionner la première option par défaut
        self.key_size_combobox.current(0)
        self.key_size_combobox.grid(
            row=0, column=0, sticky='snew', padx=10, pady=(0, 10))
        # Associer la fonction on_select à l'événement de sélection
        self.key_size_combobox.bind(
            "<<ComboboxSelected>>", self.on_key_size_select_change)

        # Créer le select pour les mode
        self.label_frame_choose_mode = ttk.LabelFrame(
            self.label_frame_choose_key_mode, text="Choose Mode")
        self.label_frame_choose_mode.grid(
            row=0, column=1, sticky='nesw', padx=10, pady=(0, 10))
        self.label_frame_choose_mode.grid_columnconfigure(0, weight=1)

        self.mode_combobox = ttk.Combobox(
            self.label_frame_choose_mode, values=self.encrypt_mode, state="readonly")
        # Sélectionner la première option par défaut
        self.mode_combobox.current(0)
        self.mode_combobox.grid(
            row=0, column=0, sticky='snew', padx=10, pady=(0, 10))
        # Associer la fonction on_select à l'événement de sélection
        self.mode_combobox.bind(
            "<<ComboboxSelected>>", self.on_mode_select_change)

        # Créer le bouton "Parcourir"
        # Creation du LabelFrame Parcourir
        self.label_frame_browse = ttk.LabelFrame(
            self.frame_browse_file, text="Browse a file/folder")
        self.label_frame_browse.grid(
            row=0, column=0, sticky='nwes', padx=10, pady=(10, 0))
        # Configurer les Frames pour qu'il prenent toute la largeur
        self.label_frame_browse.grid_columnconfigure(0, weight=1)
        # Creation du bouton
        self.browse_button = ttk.Button(
            self.label_frame_browse, text="Browse", command=lambda: self.browse_file_folder())
        self.browse_button.grid(
            row=0, column=0, sticky='wens', padx=10)
        # Créer le champ de saisie pour afficher le chemin d'accès sélectionné
        self.path_entry = ttk.Label(
            self.label_frame_browse, text="No file or folder selected.")
        self.path_entry.grid(
            row=1, column=0, sticky='wens', padx=10)
        self.checkbox_delete_files = ttk.Checkbutton(
            self.label_frame_browse, text="Delete original file(s) after task ?", variable=self.var_delete_files, command=self.on_checkbox_change)
        self.checkbox_delete_files.grid(
            row=2, column=0, sticky='snew', padx=10)

        # Creation Key
        # Creation du LabelFrame Key
        self.label_frame_key = ttk.LabelFrame(
            self.frame_key, text="Choose an option")
        self.label_frame_key.grid(
            row=0, column=0, sticky='nwes', padx=10, pady=10)
        # Configurer les Frames pour qu'il prenent toute la largeur
        self.label_frame_key.grid_columnconfigure(0, weight=1)
        self.label_frame_key.grid_columnconfigure(1, weight=1)

        self.radio1_choose_key = ttk.Radiobutton(self.label_frame_key, text="Generate a key", variable=self.choose_key_generate,
                                                     command=self.update_key_button, value="Generate")
        self.radio1_choose_key.grid(row=0, column=0, sticky="nesw", padx=10)
        self.radio2_choose_key = ttk.Radiobutton(self.label_frame_key, text="Use an existing key", variable=self.choose_key_generate,
                                                     command=self.update_key_button, value="Use an existing")
        self.radio2_choose_key.grid(row=0, column=1, sticky="nesw", padx=10)

        # Creation du bouton parcourir une clé
        self.browse_button_key = ttk.Button(
            self.label_frame_key, text="Browse", state="disabled", command=lambda: self.browse_key_file())
        self.browse_button_key.grid(
            row=1, column=0, columnspan=2, sticky='wens', padx=10)
        # Créer le label pour afficher le chemin d'accès sélectionné
        self.label_path_key = ttk.Label(
            self.label_frame_key, text="No key file selected.", state="disabled")
        self.label_path_key.grid(
            row=2, column=0, columnspan=2, sticky='wens', padx=10)

        # Creation du bouton Crypter
        self.encrypt_decrypt_button = ttk.Button(
            self.frame_crypt_button, text=self.encrypt_or_decrypt.get(), style="Custom.TButton", command=lambda: self.encrypt_decrypt())
        self.encrypt_decrypt_button.grid(
            row=0, column=0, sticky='wens', padx=10)
       
        # Creation du progress bar
        self.progress = ttk.Progressbar(
            self.frame_progress_bar, orient='horizontal', mode='determinate')
        self.progress.grid(row=0, column=0, sticky='wens',
                           padx=10, pady=(10, 0))
        # Creation d'un label pour affichier le fichier qu'il traite
        self.label_progress = ttk.Label(
            self.frame_progress_bar, text="Waiting ...", justify="right", anchor="e")
        self.label_progress.grid(
            row=1, column=0, sticky="w", padx=10, pady=(0, 10))
        
        #Bouton Asymétrique
        self.button_modal = ttk.Button(self.frame_button_asym, text="Asymmetric Encryption", style="Custom.TButton", command=lambda: self.show_modal())
        self.button_modal.pack()
        
        # Créer le bouton avec l'image
        self.button_help = ttk.Button(self.frame_button_help, text="v1.0", command=lambda: self.show_help())
        self.button_help.pack(padx=10, anchor="ne")

     # Quand la radio bouton de encrypt decrypt change on met à jour la bouton vert "Encrypt Decrypt"
    def on_radio_button_crypt_decrypt_change(self):
        # On met à jour le texte dans le bouton
        self.encrypt_decrypt_button.config(
            text=self.encrypt_or_decrypt.get())

        # Réinitialiser les path des liens
        self.reset_path_entry()

        # On envoie la nouvelle valeur de la variable au model
        self.controller.update_variable(
            "encrypt_or_decrypt", self.encrypt_or_decrypt.get())

        # Réinitialisation des boutons
        self.radio1_choose_key.config(state='normal')
        self.radio2_choose_key.config(state='normal')
        self.radio1_file_folder.config(state="normal")
        self.radio2_file_folder.config(state="normal")
        self.browse_button.config(state="normal")
        self.path_entry.config(state="normal")
        self.checkbox_delete_files.config(state="normal")
        self.on_type_encryption_change()

        # Si on clique sur décrypter, on désactive le radio bouton pour générer une clé et on laisse juste parcourir
        if self.encrypt_or_decrypt.get() == "Decrypt":
            self.choose_key_generate.set("Use an existing")
            self.radio1_choose_key.config(state='disabled')
            self.update_key_button()
        # Si on est sur Encrypt on rentre
        elif self.encrypt_or_decrypt.get() == "Encrypt":
            self.radio1_choose_key.config(state='normal')

        elif self.encrypt_or_decrypt.get() == "Generate a key":
            self.choose_key_generate.set("Generate")
            self.radio2_choose_key.config(state='disabled')
            self.update_key_button()
            # Désactiver File Folder Radio Button
            self.radio1_file_folder.config(state="disabled")
            self.radio2_file_folder.config(state="disabled")
            self.mode_combobox.config(state="disabled")
            self.browse_button.config(state="disabled")
            self.path_entry.config(state="disabled")
            self.checkbox_delete_files.config(state="disabled")

    # Quand le radio bouton file folder change

    def on_radio_button_file_folder_change(self):
        self.controller.update_variable(
            "file_or_folder", self.file_or_folder.get())
        self.reset_path_entry()

    # Méthode pour choisir un fichier ou un dossier
    def browse_file_folder(self):
        # On choisi soit un fichier ou dossier sa depend le bouton radio
        path_file_folder = "No file or folder selected."
        if self.file_or_folder.get() == "File":
            path = filedialog.askopenfilename(title="Select a file", filetypes=[(
                "File .enc", "*.enc")] if self.encrypt_or_decrypt.get() == "Decrypt" else [("All Files", "*.*")])
            if path != "":
                path_file_folder = path
        else:
            path = filedialog.askdirectory(title="Select a folder")
            if path != "":
                path_file_folder = path

        # Afficher le chemin d'accès sélectionné dans le label pour le lien du fichier / dossier
        self.path_entry.config(text=path_file_folder)
        self.controller.update_variable("path_file_folder", path_file_folder)

    # Renitialiser la chemin vers le fichier dossier
    def reset_path_entry(self):
        path_file_folder = "No file or folder selected."
        self.path_entry.config(text=path_file_folder)
        self.controller.update_variable("path_file_folder", path_file_folder)

    # Quand le type de cryptage change on change la liste des tailles des clés et on update le model
    def on_type_encryption_change(self):

        if self.type_of_encryption.get() in ["AES"]:
            self.key_sizes = [128, 192, 256]
            self.mode_combobox.config(state='readonly')

        elif self.type_of_encryption.get() in ["ChaCha20"]:
            self.key_sizes = [256]
            self.mode_combobox.config(state='disabled')

        # Mettre à jour les valeurs de la Combobox
        self.key_size_combobox['values'] = self.key_sizes
        self.key_size_combobox.current(0)
        # Envoyé les données au model
        self.controller.update_variable(
            "type_of_encryption", self.type_of_encryption.get())
        self.controller.update_variable(
            "key_size", self.key_size_combobox.get())

    # Quand la checkbox qui demande si on supprime les fichier à la fin change on met à jour le model
    def on_checkbox_change(self):
        if self.var_delete_files.get() == True:
            self.message_box_warning(
                'Attention', 'The original file(s) will be deleted !')
        self.controller.update_variable(
            "var_delete_files", self.var_delete_files.get())

    # Fonction appelée lors de la sélection d'une option de changement de taille de clé
    def on_key_size_select_change(self, event):
        self.controller.update_variable(
            "key_size", self.key_size_combobox.get())

    # Fonction appelée lors de la sélection d'un mode de cryptage
    def on_mode_select_change(self, event):
        self.controller.update_variable(
            "mode", self.mode_combobox.get())

    # Desactiver le boutton parcourir pour choisir une clé quand le radio bouton est sur Generate
    def update_key_button(self):
        if self.choose_key_generate.get() == "Generate":
            self.browse_button_key.config(state="disabled")
            self.label_path_key.config(state='disabled')
            self.key_size_combobox.config(state='readonly')
        else:
            self.browse_button_key.config(state="normal")
            self.label_path_key.config(state='normal')
            self.key_size_combobox.config(state='disabled')
        # Mettre à jour la variable dans le model
        self.controller.update_variable(
            "choose_key_generate", self.choose_key_generate.get())

     # Methode pour choisir un fichier clé
    def browse_key_file(self):
        # Si on selectionne rien on retourne cette chaine de caractere
        path_key_file = "No key file selected."
        # On choisi soit un fichier clé
        path = filedialog.askopenfilename(
            title="Select a key file", filetypes=[("File .key", "*.key")])
        if path != "":
            path_key_file = path

        # Effacer le contenu précédent
        self.label_path_key.config(text=path_key_file)
        # self.label_path_key.delete(0, ttk.END)
        # self.label_path_key.insert(0, path_key_file)  # Inserer le nouveau contenu
        # Déplacer la vue horizontale vers la fin du texte
        # self.label_path_key.xview_moveto(1)
        self.controller.update_variable("path_key_file", path_key_file)

    # Message box pour demander ou engistrer la clé
    def save_key_file_box(self):

        key_file_path = filedialog.asksaveasfilename(
            title="Select the folder to save the key",
            defaultextension='.key',
            filetypes=[("Key file", "*.key")]
        )

        return key_file_path

    # Message box
    def message_box(self, title, message):
        messagebox.showinfo(
            title, message)

    # Message box avertissement
    def message_box_warning(self, title, message):
        messagebox.showwarning(title, message)

    # Lancer le processus
    def encrypt_decrypt(self):
        self.encrypt_decrypt_button.config(
            text="Stop")
        self.encrypt_decrypt_button.configure(
            command=self.controller.stop_process)
        self.encrypt_decrypt_button.update()
        self.controller.encrypt_decrypt()

    # Renitialiser le bouton crypter decrypter
    def reset_button(self):
        self.encrypt_decrypt_button.config(
            text=self.encrypt_or_decrypt.get())
        self.encrypt_decrypt_button.configure(command=self.encrypt_decrypt)
        self.encrypt_decrypt_button.update()

    # Mettre à jour la barre de progression
    def update_task(self, value, message):
        
        #if len(message) >= 20:
            #message = "..." + message[-(20-3):]
        self.label_progress.config(text=message)
        self.label_progress.update()
        self.progress['value'] = value
        self.progress.update()

    # Stopper la barre de progression
    def stop_task(self):
        self.progress.stop()  # Arrêter la barre de progression
        self.label_progress.config(text='Waiting ...')
        self.label_progress.update()
        self.reset_button()
    
    # Afficher la modale    
    def show_modal(self):
        if self.modal_open:
            return
        self.modal_open = True
        self.controller.show_modal()
        
     #Afficher modale help
    def show_help(self):
        self.help_window = tkinter.Toplevel(self.root)
        self.help_window.protocol("WM_DELETE_WINDOW", self.close_help)
        self.help_window.title("Encryption Asymmetric")
        # Chemin vers le fichier d'icône
        #self.root.iconbitmap("@lock.xbm")
        
        # Récupérer les dimensions de l'écran
        screen_width = self.help_window.winfo_screenwidth()
        screen_height = self.help_window.winfo_screenheight()
        # Calculer les coordonnées x et y pour centrer la fenêtre
        x = (screen_width - 450) // 2
        y = (screen_height - 450) // 2
        # Définir la position de la fenêtre
        self.help_window.geometry(f'450x450+{x}+{y}')
        # Définition de la taille minimale de la fenêtre
        self.help_window.minsize(450, 450)
        
        self.help_window.grab_set()  # Désactive la fenêtre principale
        self.help_window.focus_force()  # Mettre la fenêtre modale en focus
        
        # Ajouter la barre de défilement
        scrollbar = ttk.Scrollbar(self.help_window)
        scrollbar.pack(side="right", fill="y")

        # Ajouter le texte long avec le widget Text
        help_text = """AsymSecure v1.0 - File Encryption Program Description

        AsymSecure v1.0 is a powerful software designed to ensure the security and confidentiality of your sensitive files. This program utilizes both symmetric and asymmetric encryption algorithms, combining the best of both worlds to offer robust protection.

        Key Features:

        Hybrid Encryption: AsymSecure v1.0 adopts a hybrid encryption approach, utilizing both symmetric and asymmetric algorithms. Files are encrypted using a randomly generated symmetric key with AES or ChaCha20 algorithms, ensuring high confidentiality. Then, the symmetric key is encrypted with an RSA public key to enhance security.

        RSA Key Generation: The program automatically generates an RSA key pair (private key and public key) for each recipient of the encrypted files. The private key is used for subsequent file decryption, while the public key is used to encrypt the symmetric keys.

        File Encryption: With AsymSecure v1.0, you can easily select sensitive files to encrypt. The program generates a random symmetric key for each file and encrypts its content using AES or ChaCha20 algorithms. This ensures that the encrypted files are unreadable without the corresponding symmetric key.

        Symmetric Key Encryption: After encrypting the files, AsymSecure v1.0 encrypts the symmetric key used for each file using the recipient's RSA public key. This process enhances overall security, as only recipients with the corresponding private key can decrypt the symmetric keys and access the original files.

        Secure Transmission: Once the files are successfully encrypted and the symmetric keys are encrypted with the recipients' public keys, AsymSecure v1.0 enables you to securely send the encrypted files. It is recommended to use secure transmission methods to protect sensitive data during transfer.

        The security of this program relies on the strength of the encryption algorithms used (AES, ChaCha20, RSA) and the proper protection of private and public keys. It is essential to implement additional security measures to safeguard keys and encrypted data, including secure storage mechanisms and appropriate transmission protocols.

        Use this program to secure your sensitive files and ensure the confidentiality of your confidential data during transfer or storage."""
        
        text_widget = tkinter.Text(self.help_window, wrap="word", yscrollcommand=scrollbar.set)
        text_widget.insert("1.0", help_text)
        text_widget.pack(fill="both", expand=True)

        scrollbar.config(command=text_widget.yview)
        
        self.help_window.mainloop()
    # Fermer la modale
    def close_help(self):
        self.help_window.destroy()
    
    #Commencer l'application
    def start(self):
        style = ThemedStyle(self.root)
        style.set_theme("ubuntu")  # Thème initial
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Encrypto", 15))  # Remplacez "Arial" par la police souhaitée et 12 par la taille de police souhaitée
        self.root.mainloop()
        
    
        