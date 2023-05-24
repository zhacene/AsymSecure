from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from tkinter import messagebox

class ModelAsym:
    def __init__(self, controller):
        self.controller = controller
        self.key_size = 2048
    
    def generate_key_pair(self):
        try:
            
            self.controller.start_task("Generating a key ...")
            # Demander à l'utilisateur l'emplacement de sauvegarde de la clé privée
            private_key_path = self.controller.view.save_file("Select private key save location", "PEM private key", ".pem")
            
            # Demander à l'utilisateur l'emplacement de sauvegarde de la clé publique
            public_key_path = self.controller.view.save_file("Select public key save location", "PEM public key", ".pem")
            
            # Obtenir la taille de clé sélectionnée dans la liste déroulante
            key_size = int(self.key_size)
            
            # Générer une paire de clés RSA avec la taille sélectionnée
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=default_backend()
            )
            
            # Enregistrer la clé privée dans un fichier
            with open(private_key_path, 'wb') as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            # Récupérer la clé publique depuis la clé privée
            public_key = private_key.public_key()
            
            # Enregistrer la clé publique dans un fichier
            with open(public_key_path, 'wb') as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
                
            self.controller.view.message_box("Finish !", "Finish generating a key.")
            self.controller.stop_task()
        
        except Exception as e:
            self.controller.stop_task()
            messagebox.showerror('Error', str(e))


    def encrypt_file(self):
        try:
            self.controller.start_task("Encrypting a file ...")

            # Ouvrir une boîte de dialogue pour sélectionner le fichier à chiffrer
            file_path = self.controller.view.open_file("Select a file to encrypt", ".*")
            
            # Charger la clé publique depuis un fichier
            public_key_path = self.controller.view.open_file("Select the public key", ".pem")
            
            with open(public_key_path, 'rb') as f:
                public_key = serialization.load_pem_public_key(
                    f.read(),
                    backend=default_backend()
                )
            
            # Lire le contenu du fichier à chiffrer
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Chiffrer les données du fichier
            encrypted_data = public_key.encrypt(
                file_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Ouvrir une boîte de dialogue pour sélectionner l'emplacement de sauvegarde du fichier chiffré
            encrypted_file_path = self.controller.view.save_file("Select where to save the encrypted file", "Encrypted file", ".bin")
            
            # Enregistrer les données chiffrées dans un fichier
            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_data)
            
            self.controller.view.message_box("Finish !", "Finish encrypting a file.")
            self.controller.stop_task()
            
        except Exception as e:
                self.controller.stop_task()
                messagebox.showerror('Error', str(e))

    def decrypt_file(self):
        try:
            self.controller.start_task("Decrypting a file ...")
            # Ouvrir une boîte de dialogue pour sélectionner le fichier à déchiffrer
            file_path = self.controller.view.open_file("Select a file to decrypt", ".bin")
            
            # Ouvrir une boîte de dialogue pour sélectionner la clé privée
            private_key_path = self.controller.view.open_file("Select the private key", ".pem")
            
            # Charger la clé privée depuis un fichier
            with open(private_key_path, 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
            
            # Lire les données chiffrées du fichier
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Déchiffrer les données
            decrypted_data = private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        
            # Ouvrir une boîte de dialogue pour sélectionner l'emplacement de sauvegarde du fichier déchiffré
            decrypted_file_path = self.controller.view.save_file("Select where to save the decrypted file", "Decrypted file", ".*")
        
            # Enregistrer les données déchiffrées dans un fichier
            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_data)
            
            self.controller.view.message_box("Finish !", "Finish decrypting a file.")
            self.controller.stop_task()
        
        except Exception as e:
            self.controller.stop_task()
            messagebox.showerror('Error', str(e))
