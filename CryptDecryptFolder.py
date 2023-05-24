from itertools import count
from tkinter import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from tkinter import messagebox

import os


class EncryptDecryptFolder:
    def __init__(self, controller):
        # Instance Controlleur
        self.controller = controller
        self.stop_process_bool = False
    
    def stop_process(self):
        self.stop_process_bool = True

    def start_encrypt_folder(self, path, type_encryption, key_size, mode, delete, key):
        try:
            # Si le dossier n'existe pas on lance une exception
            if not os.path.exists(path):
                raise FileNotFoundError("Folder path does not exist: {}".format(path))

            # Si la clé est False alors on génére
            if not key:
                # Générer une clé de cryptage
                key_size = int(key_size)
                key = os.urandom(key_size // 8)

                # Sauvegarder la clé dans un fichier
                key_file_path = self.controller.save_key_file()

                with open(key_file_path, 'wb') as key_file:
                    key_file.write(key)

            # Parcourir tous les fichiers et dossiers récursivement
            for root, dirs, files in os.walk(path):
                for file_name in files:
                    # Si l'utilisateur arrête le processus on arrête
                    if self.stop_process_bool:
                        raise Exception("The process was terminated by the user.")

                    # Construire le chemin complet du fichier
                    file_path = os.path.join(root, file_name)

                    # Encrypter le fichier
                    self.encrypt_file(file_path, type_encryption, key, mode, delete)

            self.controller.update_task(100, 'Encryption complete.')
            
            if delete:
                self.controller.show_message(
                    'Finished task', 'The files have been successfully encrypted and the original files have been deleted.')
            else:
                self.controller.show_message(
                    'Finished task', 'The files were successfully encrypted, but the original files were not deleted.')
            # Arrêter la barre de progression
            self.controller.stop_task()
            self.stop_process_bool = False

        except Exception as e:
            # Stopper la barre
            self.controller.stop_task()
            # Si l'utilisateur a arrêté le processus on rentre
            if self.stop_process_bool:
                self.controller.show_message('Stopping the process', str(e))
            else: 
                messagebox.showerror('Error', str(e))
            self.stop_process_bool = False

    # Méthode qui sera appelée pour chaque fichier       
    def encrypt_file(self, file_path, type_encryption, key, mode, delete):
        try:
            
            self.controller.update_task(10, 'Encrypting: ' + file_path + ' ...')
            
            # Extraire le nom de fichier et l'extension
            file_name_without_extension, file_extension = os.path.splitext(file_path)

            # Initialiser le vecteur d'initialisation (IV) aléatoire ou nonce
            iv_nonce = os.urandom(16)  # Générer un IV aléatoire

            # Ouvrir le fichier source en mode lecture binaire
            with open(file_path, 'rb') as file:
                plaintext = file.read()

            self.controller.update_task(50, 'Encrypting: ' + file_path + ' ...')

            # Initialiser le chiffreur avec le mode de cryptage sélectionné
            if type_encryption == "AES":
                if mode in ['CBC', 'CFB', 'OFB']:
                    cipher = Cipher(algorithms.AES(key), getattr(modes, mode)(iv_nonce), backend=default_backend())
                else:
                    cipher = Cipher(algorithms.AES(key), getattr(modes, mode)(), backend=default_backend())

                # Remplir le texte en clair pour qu'il soit un multiple de la taille du bloc
                padder = padding.PKCS7(algorithms.AES.block_size).padder()
                padded_plaintext = padder.update(plaintext) + padder.finalize()

                encryptor = cipher.encryptor()
                ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

            elif type_encryption == "ChaCha20":
                cipher = Cipher(algorithms.ChaCha20(key, iv_nonce), mode=None, backend=default_backend())
                encryptor = cipher.encryptor()
                ciphertext = encryptor.update(plaintext) + encryptor.finalize()

            # Construire le nouveau nom de fichier chiffré
            encrypted_file_name = f"{file_name_without_extension}{file_extension}.enc"

            # Chemin complet du fichier chiffré
            encrypted_file_path = os.path.join(os.path.dirname(file_path), encrypted_file_name)

            # Écrire le fichier chiffré
            with open(encrypted_file_path, 'wb') as file:
                if mode in ['CBC', 'CFB', 'OFB']:
                    # Écrire le vecteur d'initialisation en premier
                    file.write(iv_nonce)

                file.write(ciphertext)

            self.controller.update_task(100, 'Encrypting: ' + file_path + ' ...')
            # Supprimer le fichier source si l'option de suppression est activée
            if delete:
                os.remove(file_path)
        
        except Exception as e:
            # Stopper la barre
            self.controller.stop_task()
            # Si l'utilisateur a arrêté le processus on rentre
            if self.stop_process_bool:
                self.controller.show_message('Stopping the process', str(e))
            else: 
                messagebox.showerror('Error', str(e))
            self.stop_process_bool = False
    
    # Décrypter les dossiers
    def start_decrypt_folder(self, path, type_encryption, key, mode, delete):
        try:
            # Ouvrir le fichier contenant la clé
            with open(key, 'rb') as key_file:
                key = key_file.read()

            # Parcourir récursivement tous les fichiers et dossiers
            for root, dirs, files in os.walk(path):
                # Parcourir tous les fichiers du dossier actuel
                for file_name in files:
                    # Si l'utilisateur arrête le processus on arrête
                    if self.stop_process_bool:
                        raise Exception("The process was terminated by the user.")
                
                    # Chemin complet du fichier source
                    file_path = os.path.join(root, file_name)

                    self.controller.update_task(10, 'Decrypting: ' + file_path + ' ...')

                    # Vérifier si le chemin correspond à un fichier avec l'extension .enc
                    if file_name.endswith(".enc"):
                        # Extraire le nom de fichier et l'extension
                        file_name_without_extension, _ = os.path.splitext(file_name)

                        # Ouvrir le fichier chiffré en mode lecture binaire
                        with open(file_path, 'rb') as file:
                            # Le vecteur d'initialisation est stocké dans les 16 premiers octets
                            iv_nonce = file.read(16)
                            ciphertext = file.read()

                        self.controller.update_task(50, 'Decrypting: ' + file_path + ' ...')

                        if type_encryption == "AES":
                            # Initialiser le déchiffreur AES avec la clé et le mode choisi
                            cipher = Cipher(algorithms.AES(key), getattr(modes, mode)(iv_nonce), backend=default_backend())
                            # Créer le déchiffreur AES en mode de déchiffrement
                            decryptor = cipher.decryptor()
                            # Déchiffrer le texte chiffré
                            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
                            # Créer un unpadder pour enlever le padding du texte déchiffré
                            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                            # Enlever le padding du texte déchiffré
                            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

                        elif type_encryption == "ChaCha20":
                            # Initialiser le déchiffreur ChaCha20 avec la clé et le nonce
                            cipher = Cipher(algorithms.ChaCha20(key, iv_nonce), mode=None, backend=default_backend())
                            # Créer le déchiffreur ChaCha20 en mode de déchiffrement
                            decryptor = cipher.decryptor()
                            # Déchiffrer le texte chiffré
                            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

                        self.controller.update_task(70, 'Decrypting: ' + file_path + ' ...')

                                                # Construire le nouveau nom de fichier déchiffré
                        decrypted_file_name = f"{file_name_without_extension}"

                        # Chemin complet du fichier déchiffré
                        decrypted_file_path = os.path.join(root, decrypted_file_name)

                        # Écrire le fichier déchiffré
                        with open(decrypted_file_path, 'wb') as file:
                            file.write(plaintext)

                        self.controller.update_task(90, 'Decrypting: ' + file_path + ' ...')

                        # Supprimer le fichier chiffré si l'option de suppression est activée
                        if delete:
                            os.remove(file_path)

            self.controller.update_task(100, 'Decryption complete.')
             # Message box
            if delete:
                self.controller.show_message(
                    'Finished task', 'The files were successfully decrypted and the encrypted file was deleted.')
            else:
                self.controller.show_message(
                    'Finished task', 'The files were successfully decrypted, but the encrypted files were not deleted.')
                
            # Stopper la barre
            self.controller.stop_task()
            self.stop_process_bool = False

        except Exception as e:
            # Stopper la barre
            self.controller.stop_task()
            # Si l'utilisateur a arrêté le processus on rentre
            if self.stop_process_bool:
                self.controller.show_message('Stopping the process', str(e))
            else: 
                messagebox.showerror('Error', str(e))
            self.stop_process_bool = False

