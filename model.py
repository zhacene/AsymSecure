from CryptDecrypt.CryptDecryptFile import EncryptDecryptFile
from CryptDecrypt.CryptDecryptFolder import EncryptDecryptFolder
from threading import Thread
from tkinter import messagebox


class Model:
    def __init__(self, controller):
       # Instance Controlleur
        self.controller = controller

        # Definir la variable pour choisir est ce qu'on crypt ou decrypt
        self.encrypt_or_decrypt = "Encrypt"

        # Definir la variable pour choisir si on crypt un fichier ou un dossier
        self.file_or_folder = "File"
        self.path_file_folder = "No file or folder selected."

        # Definir la variable pour choisir le type d'encryption
        self.type_of_encryption = "AES"

        # Definir la variable pour choisir la taille de la clé
        self.key_size = 128

        # Definir la variable pour choisir la taille de l'IV'
        self.iv_size = 128

        # Definir la variable pour choisir le mode de cryptage
        self.mode = "CBC"

        # Definir la variable pour choisir si on génère une clé ou on utilise une existante
        self.choose_key_generate = "Generate"
        # Definir la variable pour choisir un fichier clé
        self.path_key_file = "No key file selected."

        # Checkbox supprimer les fichier à la fin
        self.var_delete_files = False

        # Instance du crypteur
        self.encrypt_decrypt_file = EncryptDecryptFile(self.controller)
        self.encrypt_decrypt_folder = EncryptDecryptFolder(self.controller)

    # La fonction qui va lancer le cryptage

    def encrypt_decrypt(self):
        try:

            # Si l'utilisateur a choisi de crypter alors on rentre
            if self.encrypt_or_decrypt == "Encrypt":

                # On vérifie si on génère une clé ou on utilise une existante
                if self.choose_key_generate != "Generate":
                    # Ouvrir le fichier contenant la clé
                    with open(self.path_key_file, 'rb') as key_file:
                        self.key = key_file.read()
                else:
                    self.key = False

                # Si on crypte juste un fichier
                if self.file_or_folder == "File":
                    encrypt_thread = Thread(target=self.encrypt_decrypt_file.start_encrypt_file,
                                            args=(self.path_file_folder, self.type_of_encryption, self.key_size, self.mode, self.var_delete_files, self.key))
                    encrypt_thread.start()
                elif self.file_or_folder == "Folder":
                    encrypt_thread = Thread(target=self.encrypt_decrypt_folder.start_encrypt_folder,
                                            args=(self.path_file_folder, self.type_of_encryption, self.key_size, self.mode, self.var_delete_files, self.key))
                    encrypt_thread.start()

            # Si on déchiffre on rentre
            elif self.encrypt_or_decrypt == "Decrypt":
                # Fichier ou Dossier
                if self.file_or_folder == "File":
                    decrypt_thread = Thread(target=self.encrypt_decrypt_file.start_decrypt_file,
                                            args=(self.path_file_folder, self.type_of_encryption, self.path_key_file, self.mode, self.var_delete_files))
                    decrypt_thread.start()
                elif self.file_or_folder == "Folder":
                    decrypt_thread = Thread(target=self.encrypt_decrypt_folder.start_decrypt_folder,
                                            args=(self.path_file_folder, self.type_of_encryption, self.path_key_file, self.mode, self.var_delete_files))
                    decrypt_thread.start()

            # Si on génère une clé on rentre
            elif self.encrypt_or_decrypt == "Generate a key":

                generate_key_thread = Thread(target=self.encrypt_decrypt_file.generate_key,
                                             args=(self.key_size, True))
                generate_key_thread.start()

        except Exception as e:
            self.controller.stop_task()
            messagebox.showerror('Error', str(e))
