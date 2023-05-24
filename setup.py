from cx_Freeze import setup, Executable

# Liste des fichiers sources de ton programme
# Assure-toi d'inclure tous les fichiers nécessaires
# tels que les fichiers de contrôleur, de modèle et de vue
files = ['controller.py', 'model.py', 'view.py', 'CryptDecrypt/CryptDecryptFile.py', 'CryptDecrypt/CryptDecryptFolder.py', 'CryptDecrypt/ControllerAsym.py', 'CryptDecrypt/ModelAsym.py', 'CryptDecrypt/ViewAsym.py']

# Paramètres de configuration de cx_Freeze
options = {
    'build_exe': {
        'include_files': files,
        'packages': ['cryptography', 'PIL'],
    },
}

# Création de l'exécutable
executables = [
    Executable('main.py', base=None, icon='locked.ico')
]

setup(
    name='SecureAsym',
    version='1.0',
    description='AsymSecure v1.0 is a powerful software designed to ensure the security and confidentiality of your sensitive files. This program utilizes both symmetric and asymmetric encryption algorithms, combining the best of both worlds to offer robust protection.',
    options=options,
    executables=executables
)