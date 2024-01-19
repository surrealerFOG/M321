import os
import requests
import json
import base64

image_folder = "pictures"
output_folder = "processedPictures"
host = "https://api-us.idphotoapp.com"
url = host + "/v2/makeIdPhoto"
API_KEY = 'udRf8vk238f0tm'
API_SECRET = '102230f75f4f1682ff582a78961861f'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if __name__ == '__main__':
    for filename in os.listdir(image_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            
            with open(image_path, 'rb') as f:
                pic = f.read()

            data = {
                "specCode": "australia-passport",
                "imageBase64": base64.b64encode(pic).decode(),
                "apiKey": API_KEY,
                "apiSecret": API_SECRET
            }
            
            data_json = json.dumps(data)
            response = requests.post(url, data=data_json)
            
            result = response.json()
            id_photo_url = result.get('idPhotoUrl')

            # Herunterladen und Speichern des bearbeiteten Bildes
            if id_photo_url:
                id_photo_response = requests.get(id_photo_url)
                if id_photo_response.status_code == 200:
                    output_path = os.path.join(output_folder, f"processed_{filename}")
                    with open(output_path, 'wb') as output_file:
                        output_file.write(id_photo_response.content)

                    os.remove(image_path)

                    print(f"Bearbeitetes Bild für {filename} wurde in {output_path} gespeichert. \nDas Originalbild wurde gelöscht.\n")

                else:
                    print(f"Fehler beim Herunterladen des bearbeiteten Bildes für {filename}")
            else:
                print(f"Fehler bei der Verarbeitung des Bildes {filename}: {result}")
