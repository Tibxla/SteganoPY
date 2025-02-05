from flask import Flask, render_template, request, send_file, make_response, jsonify
import tempfile
from PIL import Image
import base64
import tempfile
import binascii


app = Flask(__name__)


def encode_file_in_image(image_path, file_to_hide_path, target_bit):
    # Ouvrir l'image et la convertir en mode RGB si nécessaire
    image = Image.open(image_path).convert("RGB")

    with open(file_to_hide_path, "rb") as file_to_hide:
        hidden_data = file_to_hide.read()

    # Encoder le contenu du fichier en une chaîne de caractères
    hidden_data_str = base64.b64encode(hidden_data).decode()

    # Vérifier si l'image est assez grande pour contenir toutes les données
    required_pixels = len(hidden_data_str) * 8 + 32  # 32 bits pour la longueur du message
    required_pixels += 1  # Réserver 1 pixel pour le numéro du bit cible
    if required_pixels > image.width * image.height:
        print("L'image n'est pas assez grande pour contenir toutes les données.")
        return False

    # Vérifier si le bit cible est valide
    if target_bit not in range(8):
        print("Le bit cible doit être compris entre 0 et 7.")
        return False

    # Ajouter la longueur du message au début du fichier caché
    hidden_data_length = len(hidden_data_str)
    hidden_data = hidden_data_length.to_bytes(4, byteorder="big") + hidden_data_str.encode()

    new_image = image.copy()
    pixel_index = 1  # Commencer après le pixel réservé pour le numéro du bit cible

    for data_byte in hidden_data:
        for bit_index in range(8):
            data_bit = (data_byte >> (7 - bit_index)) & 1
            x = pixel_index % image.width
            y = pixel_index // image.width
            r, g, b = new_image.getpixel((x, y))
            new_r = (r & ~(1 << target_bit)) | (data_bit << target_bit)
            new_image.putpixel((x, y), (new_r, g, b))
            pixel_index += 1

    # Enregistrer le numéro du bit utilisé dans le pixel réservé
    x = 0
    y = 0
    r, g, b = image.getpixel((x, y))
    new_r = (r & ~7) | target_bit  # Utiliser les 3 bits de poids faible du canal rouge
    new_image.putpixel((x, y), (new_r, g, b))

    # Enregistrer l'image de sortie au format PNG
    new_image.save("image.png", format="PNG")
    print("Le fichier a été caché dans l'image avec succès.")
    return True

def decode_file_from_image(image_path):
  # Ouvrir l'image et la convertir en mode RGB si nécessaire
  image = Image.open(image_path).convert("RGB")

  # Récupérer le numéro du bit utilisé à partir du pixel réservé
  x = 0
  y = 0
  r, g, b = image.getpixel((x, y))
  target_bit = r & 7  # Utiliser les 3 bits de poids faible du canal rouge

  width, height = image.size

  # Calculer la taille du fichier caché
  hidden_data_size = ((width * height - 1) * 8) // 8
  hidden_data = bytearray(hidden_data_size)

  # Décoder le fichier caché à partir de l'image
  pixel_index = 1  # Commencer après le pixel réservé
  while pixel_index < width * height:
      x = pixel_index % width
      y = pixel_index // width
      r, g, b = image.getpixel((x, y))
      bit = (r >> target_bit) & 1
      current_byte_index = (pixel_index - 1) // 8  # Ajuster pour le pixel réservé
      current_byte_bit_index = 7 - ((pixel_index - 1) % 8)
      hidden_data[current_byte_index] |= (bit << current_byte_bit_index)
      pixel_index += 1

  # Récupérer la longueur du fichier caché à partir des premiers octets
  hidden_data_length = int.from_bytes(hidden_data[:4], byteorder="big")

  # Extraire le message caché
  if 4 + hidden_data_length <= len(hidden_data):
      hidden_data = hidden_data[4:4 + hidden_data_length]
      # Décoder la chaîne de caractères en contenu de fichier
      try:
          hidden_data_str = hidden_data.decode("utf-8")
          hidden_data = base64.b64decode(hidden_data_str)
      except UnicodeDecodeError:
          print("Erreur de décodage : le fichier texte n'est pas encodé en UTF-8.")
          return False, None
      except binascii.Error:
          print("Erreur de décodage : la chaîne de caractères encodée en base64 n'est pas valide.")
          return False, None
      # Déterminer l'extension du fichier à partir du contenu
      file_extension = ""
      if hidden_data.startswith(b"\x89PNG"):
          file_extension = ".png"
      elif hidden_data.startswith(b"%PDF"):
          file_extension = ".pdf"
      elif hidden_data.startswith(b"MZ"):
          file_extension = ".exe"
      elif hidden_data.startswith(b"\xD0\xCf\x11\xE0\xA1\xB1\x1A\xE1"):
          file_extension = ".doc"
      elif hidden_data.startswith(b"\x50\x4B\x03\x04"):
          file_extension = ".zip"
      elif hidden_data.startswith(b"\xFF\xD8\xFF"):
          file_extension = ".jpg"
      elif hidden_data.startswith(b"ID3"):
          file_extension = ".mp3"
      elif hidden_data_str.isprintable():
          file_extension = ".txt"
      else:
          print("Le type de fichier caché n'est pas pris en charge.")
          return False, None
      # Écrire le contenu du fichier dans un fichier avec l'extension appropriée
      with open("ficherdecode" + file_extension, "wb") as output_file:
          output_file.write(hidden_data)
        
      print("Le fichier a été extrait de l'image avec succès.")
      return True, file_extension
  else:
      print("Aucun fichier n'a été trouvé dans l'image.")
      return False, None


@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        image_file = request.files['image']
        file_to_hide = request.files['file']
        target_bit = int(request.form['target_bit'])
        output_name = request.form.get('output_name')

        with tempfile.NamedTemporaryFile(delete=False) as tmp_image, tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            image_file.save(tmp_image.name)
            file_to_hide.save(tmp_file.name)

            if encode_file_in_image(tmp_image.name, tmp_file.name, target_bit):
                if output_name:
                    return send_file("image.png", as_attachment=True, download_name=f"{output_name}.png")
                else:
                    return send_file("image.png", as_attachment=True, download_name="encoded_image.png")
            else:
                return jsonify({"error": "L'image n'est pas assez grande pour contenir toutes les données"}), 400                
    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        image_file = request.files['image']

        with tempfile.NamedTemporaryFile(delete=False) as tmp_image:
            image_file.save(tmp_image.name)

            success, file_extension = decode_file_from_image(tmp_image.name)

            if success:
                output_name = request.form.get('output_name')
                response = make_response(send_file(f"ficherdecode{file_extension}" if file_extension else "", as_attachment=True, download_name=f"{output_name}{file_extension}" if output_name and file_extension else f"decoded_file{file_extension}" if file_extension else ""))
                response.headers.add('X-Decoded-File-Extension', str(file_extension) if file_extension is not None else '')
                return response
            else:
                return jsonify({"error": "Aucun fichier n'a été trouvé dans l'image"}), 400 

    return render_template('decode.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@app.route('/')
def home():
    return render_template('home.html')  # Utilisation d'un template pour l'HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)