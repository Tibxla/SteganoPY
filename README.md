# SteganoPY

Application web de stéganographie LSB : cache n'importe quel fichier dans une image PNG, et le récupère depuis cette même image.

---

## Ce que fait le projet

SteganoPY applique la technique **LSB (Least Significant Bit)** pour dissimuler des données dans les pixels d'une image. Le fichier à cacher est encodé en base64, précédé de sa longueur sur 4 octets, puis distribué bit par bit dans le canal rouge des pixels de l'image de couverture. Le premier pixel stocke le numéro du bit utilisé (0–7), ce qui rend le décodage autonome : l'image encodée se suffit à elle-même.

L'interface est une application Flask accessible via navigateur.

---

## Stack technique

| Composant   | Technologie              |
|-------------|--------------------------|
| Backend     | Python 3.10+, Flask      |
| Traitement image | Pillow              |
| Frontend    | HTML/CSS vanilla, JS fetch API |
| Serveur dev | Flask built-in (port 5000) |

---

## Prérequis

- Python 3.8 ou supérieur
- pip

---

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-utilisateur/SteganoPY.git
cd SteganoPY

# 2. (Optionnel) Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
```

---

## Lancement

```bash
python main.py
```

L'application est accessible à l'adresse : [http://localhost:5000](http://localhost:5000)

---

## Structure du projet

```
SteganoPY/
├── main.py              # Application Flask : routes et logique métier LSB
├── requirements.txt     # Dépendances Python (Flask, Pillow)
├── static/
│   ├── style.css        # Styles (thème sombre, violet)
│   └── script.js        # Soumission AJAX des formulaires, gestion du téléchargement
└── templates/
    ├── home.html        # Page d'accueil
    ├── encode.html      # Formulaire d'encodage
    ├── decode.html      # Formulaire de décodage
    ├── 404.html         # Page d'erreur 404
    └── 500.html         # Page d'erreur 500
```

---

## Fonctionnalités

### Encoder un fichier dans une image

1. Aller sur `/encode`
2. Sélectionner une image de couverture (PNG ou JPG)
3. Sélectionner le fichier à cacher
4. Choisir le bit cible (0 = moins visible, 7 = modifications les plus perceptibles)
5. Optionnel : donner un nom au fichier de sortie
6. Cliquer sur **Encoder** — l'image modifiée est téléchargée au format PNG

**Contrainte de taille :** l'image de couverture doit contenir suffisamment de pixels pour stocker les données. La formule est : `(taille_base64 * 8 + 33) pixels minimum`.

### Décoder un fichier depuis une image

1. Aller sur `/decode`
2. Sélectionner une image PNG préalablement encodée par SteganoPY
3. Optionnel : donner un nom au fichier extrait
4. Cliquer sur **Décoder** — le fichier caché est téléchargé avec son extension détectée automatiquement

### Détection automatique du type de fichier

Le décodage identifie le type du fichier caché par ses magic bytes :

| Type    | Signature                        |
|---------|----------------------------------|
| PNG     | `\x89PNG`                        |
| JPG     | `\xFF\xD8\xFF`                   |
| PDF     | `%PDF`                           |
| ZIP     | `PK\x03\x04`                     |
| DOC     | `\xD0\xCF\x11\xE0...`            |
| EXE     | `MZ`                             |
| MP3     | `ID3`                            |
| TXT     | texte UTF-8 valide (fallback)    |

---

## Notes techniques

- L'image de couverture doit être fournie au format PNG ou JPG. Elle est toujours sauvegardée en **PNG** pour éviter les pertes de compression.
- Les fichiers temporaires sont créés et supprimés en mémoire/disque pour chaque requête — aucun fichier intermédiaire n'est conservé sur le serveur.
- L'encodage en base64 augmente la taille des données d'environ 33 %, ce qui influe sur la taille minimale requise de l'image.
- Bit 0 : modification imperceptible à l'œil nu. Bit 7 : altération visible des couleurs.

---

## Licence

Ce projet n'inclut pas de fichier de licence explicite.
