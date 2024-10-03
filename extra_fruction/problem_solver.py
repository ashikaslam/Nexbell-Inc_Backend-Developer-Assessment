import secrets
import string
import requests






def generate_token(length=30):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))








def upload_image_to_imgbb(file):
    try:
        api_key = "01d4e13ce09166077b3f74004ee91206"
        api_url = f"https://api.imgbb.com/1/upload?key={api_key}"

        # Prepare the file for the request (ensure it is read as binary data)
        files = {'image': (file.name, file.read(), file.content_type)}

        # Post the file to ImgBB
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                image_url = data['data']['url']
                return image_url
        return None
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None








