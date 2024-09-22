import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import numpy as np
import pandas as pd
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import matplotlib.pyplot as plt

load_dotenv()
API_KEY = os.getenv("API_KEY")


# Set up Chrome options to ignore SSL errors (if necessary)
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

# Set up Selenium WebDriver with the correct ChromeDriver path using Service and ChromeOptions
chrome_service = Service(r'C:\Users\Vir Malhotra\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Function to scrape cat images from iStock
def scrape_cat_images():
    website_url = 'https://www.istockphoto.com/photos/cats'
    driver.get(website_url)
    
    time.sleep(5)  # Let the page load

    # Scroll down to load more images if necessary
    for _ in range(3):  # Adjust scroll range based on content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # Find and extract image elements using the updated class selector
    images = driver.find_elements(By.CSS_SELECTOR, 'img.bOaTkZcdqgXxzJCZECTz')  # iStock image selector based on the class
    image_data = []

    for img in images[:10]:  # Scraping the first 10 images for this example
        src = img.get_attribute('src')
        alt = img.get_attribute('alt')
        if src:
            image_data.append({
                'image_url': src,
                'alt_text': alt
            })

    return image_data

# Function to fetch cat images from TheCatAPI and additional breed information
def fetch_from_catapi(api_key, limit=5):
    api_url = 'https://api.thecatapi.com/v1/images/search'
    headers = {'x-api-key': API_KEY}
    params = {'has_breeds': 1, 'limit': limit}
    
    response = requests.get(api_url, headers=headers, params=params)
    data = response.json()

    cat_data = []
    for cat in data:
        image_url = cat['url']
        breed_info = cat['breeds'][0] if 'breeds' in cat and len(cat['breeds']) > 0 else None
        if breed_info:
            breed_name = breed_info.get('name', 'Unknown')
            temperament = breed_info.get('temperament', 'Unknown')
            description = breed_info.get('description', 'No description available')
            origin = breed_info.get('origin', 'Unknown')
            life_span = breed_info.get('life_span', 'Unknown')
            weight = breed_info.get('weight', {}).get('imperial', 'Unknown')
        else:
            breed_name = temperament = description = origin = life_span = weight = 'Unknown'
        
        cat_data.append({
            'image_url': image_url,
            'breed': breed_name,
            'temperament': temperament,
            'description': description,
            'origin': origin,
            'life_span': life_span,
            'weight': weight
        })
    
    return cat_data

# AI-based breed identification using ResNet50
def predict_breed(img_url):
    try:
        # Load pre-trained ResNet50 model
        model = ResNet50(weights='imagenet')

        # Load and preprocess image
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((224, 224))  # ResNet50 input size
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Predict breed using ResNet50
        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        
        print(f"Top predictions for {img_url}:")
        for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
            print(f"{i + 1}: {label} ({score:.2f})")

        # Optionally display the image
        plt.imshow(img)
        plt.axis('off')
        plt.show()

        return decoded_predictions

    except Exception as e:
        print(f"Error processing image: {img_url} -> {e}")
        return [("unknown", "unknown", 0)]

# Function to combine data from TheCatAPI, scraped data, and AI predictions
def combine_data(catapi_data, scraped_data):
    combined_dataset = []

    # Process scraped data, using AI to predict the breed
    for data in scraped_data:
        image_url = data['image_url']
        alt_text = data['alt_text']
        print(f"Processing scraped image: {image_url}")  # Debugging: Ensure we are processing scraped data
        ai_prediction = predict_breed(image_url)

        combined_dataset.append({
            'image_url': image_url,
            'alt_text': alt_text,
            'ai_prediction': ai_prediction[0][1],  # Take top AI prediction label
            'breed_from_catapi': 'unsure',  # For scraped images, the actual breed is unknown
            'temperament': 'N/A',
            'description': 'N/A',
            'origin': 'N/A',
            'life_span': 'N/A',
            'weight': 'N/A'
        })

    # Process TheCatAPI data, using both the actual breed and AI prediction
    for data in catapi_data:
        image_url = data['image_url']
        breed_name = data['breed']
        ai_prediction = predict_breed(image_url)

        combined_dataset.append({
            'image_url': image_url,
            'alt_text': None,
            'ai_prediction': ai_prediction[0][1],
            'breed_from_catapi': breed_name,  # For TheCatAPI images, the actual breed is known
            'temperament': data['temperament'],
            'description': data['description'],
            'origin': data['origin'],
            'life_span': data['life_span'],
            'weight': data['weight']
        })

    return combined_dataset

# Function to save the combined data to a CSV file
def save_to_csv(combined_data, filename='cat_images_data.csv'):
    df = pd.DataFrame(combined_data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main code to run everything
if __name__ == "__main__":
    # 1. Scrape images from iStock
    scraped_data = scrape_cat_images()

    # 2. Fetch data from TheCatAPI
    catapi_data = fetch_from_catapi(api_key="YOUR_CATAPI_KEY", limit=5)  # Replace with your TheCatAPI key

    # 3. Combine the data
    combined_dataset = combine_data(catapi_data, scraped_data)

    # 4. Output the final combined dataset
    for entry in combined_dataset:
        print(f"Image URL: {entry['image_url']}")
        print(f"AI Predicted Breed: {entry['ai_prediction']}")
        if entry['breed_from_catapi']:
            print(f"Breed from CatAPI (or 'unsure'): {entry['breed_from_catapi']}")
        print(f"Temperament: {entry['temperament']}")
        print(f"Description: {entry['description']}")
        print(f"Origin: {entry['origin']}")
        print(f"Life Span: {entry['life_span']}")
        print(f"Weight: {entry['weight']}")
        if entry['alt_text']:
            print(f"Alt Text from Scraped Data: {entry['alt_text']}")
        print("\n")

    # 5. Save the combined dataset to a CSV file
    save_to_csv(combined_dataset)

    # Close the Selenium WebDriver
    driver.quit()
