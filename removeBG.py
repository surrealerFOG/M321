import http.client
from urllib.parse import urlencode, urlparse, parse_qs
import os

api_key = 'Y8kkF8kpYNWygMDjEKBM2stv'

# Create an array of image URLs
image_urls = [
    'https://cdn.discordapp.com/attachments/890943878276997140/1168958829002760243/MicrosoftTeams-image_7.png?ex=65aff1bf&is=659d7cbf&hm=bd3ada91107a8f0f738e2445ad53e5efb58626edcab3f48134ba0c9c423e9008&',
    'https://cdn.discordapp.com/attachments/899977696526864385/1152130212134408272/IMG_4246.png?ex=65b35260&is=65a0dd60&hm=b1bf561fd027aba85105e6d759fd9f26c95536c92866983f0e67214e3a5f3e2c&',
    'https://cdn.discordapp.com/attachments/1181714127815712891/1192905085253062676/IMG_0097.jpg?ex=65aac66f&is=6598516f&hm=8269c80567077e0c44bad8d14a8b6aca01999e46a8ce38711b1df10108b871ae&'
]

# API endpoint
endpoint = '/v1.0/removebg'

# Set up headers
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Api-Key': api_key,
}

# Create connection
conn = http.client.HTTPSConnection('api.remove.bg')

# Create the "pics" folder if it doesn't exist
pics_folder = 'pics'
os.makedirs(pics_folder, exist_ok=True)

for image_url in image_urls:
    # Set up the request data for each image URL
    data = {
        'image_url': image_url,
        'size': 'auto',
    }

    # Encode the data
    encoded_data = urlencode(data)

    # Send the POST request
    conn.request('POST', endpoint, body=encoded_data, headers=headers)

    # Get the response
    response = conn.getresponse()

    if response.status == 200:
        # Extract the filename from the URL
        parsed_url = urlparse(image_url)
        query_params = parse_qs(parsed_url.query)
        filename = os.path.splitext(os.path.basename(parsed_url.path))[0]
        without_bg_filename = os.path.join(pics_folder, f"{filename}_withoutBG.png")

        # Save the response content to a file in the "pics" folder
        with open(without_bg_filename, 'wb') as out:
            out.write(response.read())
        print(f"Processed {image_url} and saved as {without_bg_filename}")
    else:
        print(f"Error processing {image_url}: {response.status}, {response.read().decode()}")

# Close the connection
conn.close()
