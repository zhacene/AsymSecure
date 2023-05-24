import tkinter
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.backends import default_backend
import os
from tkinter import messagebox



class EncryptDecryptFile:
    def __init__(self, controller):
        # Instance Controlleur
        self.controller = controller
        self.stop_process_bool = False

    def stop_process(self):

        self.stop_process_bool = True

    def start_encrypt_file(self, path, type_encryption, key_size, mode, delete, key):

        try:
            # Extraire le nom de fichier et l'extension
            file_name, file_extension = os.path.splitext(path)
            
            # Ouvrir le fichier source en mode lecture binaire
            with open(path, 'rb') as file:
                plaintext = file.read()

            # Except pour quitter le programme
            if self.stop_process_bool:
                raise Exception("The process was terminated by the user.")
            
            # Si la clé est False alors on génère
            if not key:
                key = self.generate_key(key_size, False)

            # Mettre à jour la barre de progression
            self.controller.update_task(
                10, 'Encrypting : ' + file_name + ' ...')
            
            # Initialiser le vecteur d'initialisation (IV) aléatoire ou nonce
            iv_nonce = os.urandom(16)
            
            # Mettre à jour la barre de progression
            self.controller.update_task(
                30, 'Encrypting : ' + file_name + ' ...')

            # Initialiser le chiffreur avec le mode de cryptage sélectionné
            if type_encryption == "AES":
            
                cipher = Cipher(algorithms.AES(key), modes.ECB() if mode == "ECB" else getattr(
                    modes, mode)(iv_nonce), backend=default_backend())

                # Créer un padder pour remplir le texte en clair
                padder = padding.PKCS7(algorithms.AES.block_size).padder()

                # Remplir le texte en clair pour qu'il soit un multiple de la taille du bloc
                padded_plaintext = padder.update(plaintext) + padder.finalize()

                # Créer le chiffreur en mode de chiffrement
                encryptor = cipher.encryptor()

                # Except pour quitter le programme
                if self.stop_process_bool:
                    raise Exception("The process was terminated by the user.")
                # Chiffrer le texte en clair
                ciphertext = encryptor.update(
                    padded_plaintext) + encryptor.finalize()

            elif type_encryption == "ChaCha20":
                cipher = Cipher(algorithms.ChaCha20(
                    key, nonce=iv_nonce), mode=None, backend=default_backend())
                # Chiffrement du texte en clair
                encryptor = cipher.encryptor()

                # Except pour quitter le programme
                if self.stop_process_bool:
                    raise Exception("The process was terminated by the user.")

                ciphertext = encryptor.update(plaintext) + encryptor.finalize()

            # Except pour quitter le programme
            if self.stop_process_bool:
                    raise Exception("The process was terminated by the user.")

            # Mettre à jour la barre de progression
            self.controller.update_task(
                60, 'Encrypting : ' + file_name + ' ...')

            # Construire le nouveau nom de fichier chiffré
            encrypted_file_name = f"{file_name}{file_extension}.enc"

            # Chemin complet du fichier chiffré
            encrypted_file_path = os.path.join(
                os.path.dirname(path), encrypted_file_name)
            # Except pour quitter le programme
            if self.stop_process_bool:
                raise Exception("The process was terminated by the user.")

            # Écrire le fichier chiffré
            with open(encrypted_file_path, 'wb') as file:
                # Écrire le vecteur d'initialisation en premier
                if type_encryption in ["AES", "ChaCha20"]:
                    file.write(iv_nonce)
                file.write(ciphertext)

            # Mettre à jour la barre de progression
            self.controller.update_task(
                100, 'Encryption complete : ' + file_name + ' ...')

            # Confirmer la suppression du fichier
            if delete:
                # Supprimer le fichier original
                os.remove(path)
                self.controller.show_message(
                    'Finished task', 'The file has been successfully encrypted and the original file has been deleted.')
            else:
                self.controller.show_message(
                    'Finished task', 'The file was successfully encrypted, but the original file was not deleted.')

            # Arrêter la progresse barre
            self.controller.stop_task()
            self.stop_process_bool = False

        except Exception as e:
            # Stopper la barre
            self.controller.stop_task()
            # Si l'utilisateur a arrete le processus on rentre
            if self.stop_process_bool:
                self.controller.show_message('Stopping the process', str(e))
            else:
                messagebox.showerror('Error', str(e))

            self.stop_process_bool = False

    def start_decrypt_file(self, path, type_encryption, key, mode, delete):
        try:

            # Extraire le nom de fichier et l'extension
            file_name, file_extension = os.path.splitext(path)

            # Mettre à jour la barre de progression
            self.controller.update_task(
                10, 'Decrypting : ' + file_name + ' ...')

            # Ouvrir le fichier chiffré en mode lecture binaire
            with open(path, 'rb') as file:
                # Le vecteur d'initialisation est stocké dans les 16 premiers octets
                iv_nonce = file.read(16)
                ciphertext = file.read()

            # Ouvrir le fichier contenant la clé
            with open(key, 'rb') as key_file:
                key = key_file.read()

            # Except pour quitter le programme
            if self.stop_process_bool:
                raise Exception("The process was terminated by the user.")

            # Mettre à jour la barre de progression
            self.controller.update_task(
                30, 'Decrypting : ' + file_name + ' ...')

            if type_encryption == "AES":

                # Initialiser le déchiffreur AES avec la clé et le mode Choisi
                cipher = Cipher(algorithms.AES(key), modes.ECB() if mode == "ECB" else getattr(modes, mode)(iv_nonce),
                                backend=default_backend())

                # Créer le déchiffreur AES en mode de déchiffrement
                decryptor = cipher.decryptor()

                # Déchiffrer le texte chiffré
                padded_plaintext = decryptor.update(
                    ciphertext) + decryptor.finalize()

                # Créer un unpadder pour enlever le padding du texte déchiffré
                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

                # Enlever le padding du texte déchiffré
                plaintext = unpadder.update(
                    padded_plaintext) + unpadder.finalize()

                # Mettre à jour la barre de progression
                self.controller.update_task(
                    60, 'Decrypting : ' + file_name + ' ...')

            elif type_encryption == "ChaCha20":
                # Initialiser le déchiffreur ChaCha20 avec la clé et le nonce
                cipher = Cipher(algorithms.ChaCha20(key, iv_nonce),
                                mode=None, backend=default_backend())

                # Créer le déchiffreur ChaCha20 en mode de déchiffrement
                decryptor = cipher.decryptor()

                # Déchiffrer le texte chiffré
                plaintext = decryptor.update(ciphertext) + decryptor.finalize()

                # Mettre à jour la barre de progression
                self.controller.update_task(
                    60, 'Decrypting : ' + file_name + ' ...')

            # Except pour quitter le programme
            if self.stop_process_bool:
                raise Exception("The process was terminated by the user.")

            # Obtenir le dossier parent du fichier chiffré
            parent_directory = os.path.dirname(path)

            # Construire le chemin complet du fichier déchiffré
            decrypted_file_path = os.path.join(parent_directory, file_name)

            # Écrire le fichier déchiffré
            with open(decrypted_file_path, 'wb') as file:
                file.write(plaintext)
            # Except pour quitter le programme
            if self.stop_process_bool:
                raise Exception("The process was terminated by the user.")

            # Mettre à jour la barre de progression
            self.controller.update_task(
                100, 'Decryption complete : ' + file_name + ' ...')

            # confirmer la suppression du fichier
            if delete:
                # Supprimer le fichier chiffré
                os.remove(path)
                self.controller.show_message(
                    'Finished task', 'The file was successfully decrypted and the encrypted file was deleted.')
            else:
                self.controller.show_message(
                    'Finished task', 'The file was successfully decrypted, but the encrypted file was not deleted.')

            # Arreter la progresse barre
            self.controller.stop_task()
            self.stop_process_bool = False

        except Exception as e:
            # Stopper la barre
            self.controller.stop_task()
            # Si l'utilisateur a arrete le processus on rentre
            if self.stop_process_bool:
                self.controller.show_message('Stopping the process', str(e))
            else:
                messagebox.showerror('Error', str(e))

    def generate_key(self, key_size, just_generate):
        try:
            # Except pour quitter le programme
            if self.stop_process_bool:
                raise Exception("The process was terminated by the user.")
            
            # Mettre à jour la barre de progression
            self.controller.update_task(10, 'Creating a key file...')

            key_size = int(key_size)
            # Sauvegarder la clé dans un fichier
            key_file_path = self.controller.save_key_file()
        
            # Générer une clé de cryptage AES ChaCha20
            key = os.urandom(key_size // 8)
            
            #Engistrement de la clé
            with open(key_file_path, 'wb') as key_file:
                    key_file.write(key)

            # Mettre à jour la barre de progression
            self.controller.update_task(100, 'Creating a key file...')
            self.controller.show_message(
                'Creating a key file', 'The key has been created successfully.')
            # Arrêter la progresse barre
            self.controller.stop_task()
            self.stop_process_bool = False

            if not just_generate:
                return key
        
        except Exception as e:
            # Stopper la barre
            self.controller.stop_task()
            # Si l'utilisateur a arrête le processus on rentre
            if self.stop_process_bool:
                self.controller.show_message('Stopping the process', str(e))
            else:
                messagebox.showerror('Error', str(e))

            self.stop_process_bool = False
