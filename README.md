# Cat Image Scraper and Breed Predictor

## Project Overview

This project combines data from two sources to create a dataset of cat images and associated breed information:

1. **TheCatAPI**: This API provides images of cats along with detailed breed information, including breed name, temperament, description, origin, life span, and weight.
2. **iStock Web Scraping**: We scrape cat images from iStock, a popular image repository. These images do not come with breed information, so we use an AI model (ResNet50) to predict the breed based on the image.

The main purpose of this project is to gather cat images and predict their breeds using AI to create a comprehensive dataset for researchers, developers, and cat enthusiasts.

### Why We Chose These Sources

- **TheCatAPI**: This API provides high-quality cat images with detailed breed information. It's useful for providing labeled data for known cat breeds.
- **iStock**: A large repository of public images that doesn't have breed information, making it an ideal candidate for AI-based breed prediction. By scraping iStock, we gather more images of cats in diverse settings, expanding the dataset beyond the curated content of TheCatAPI.

### Value of the Dataset

This dataset provides value in multiple ways:
- **AI Breed Prediction**: By combining scraped images and an AI model for breed prediction, this dataset offers insights into cat breed recognition using machine learning.
- **Non-publicly Available Data**: The combination of iStock images with AI-predicted breeds is not available publicly, offering a unique resource for developers or researchers interested in cat breeds, computer vision, or AI-based classification.
- **Enrichment**: Users can access detailed information such as breed temperament, description, origin, life span, and weight for CatAPI-provided images, which can be beneficial for further studies in animal science or pet-related research.

### Installation and Setup

To run this project on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/cat-image-scraper.git
   cd cat-image-scraper
   ```
Install dependencies:

```bash
Copy code
pip install -r requirements.txt
```

Set up TheCatAPI key: You need an API key from TheCatAPI. Replace the placeholder in the code with your API key:

```
api_key = "YOUR_CATAPI_KEY"
```

Run the main script:

```bash
python main.py
```
Output
The program scrapes images from iStock, gathers images from TheCatAPI, predicts cat breeds using ResNet50, and combines the data into a CSV file. The CSV contains the following fields:

image_url: The URL of the cat image.
alt_text: Alternative text for the iStock images.
ai_prediction: The predicted breed from the AI model.
breed_from_catapi: The actual breed from TheCatAPI (if available).
temperament, description, origin, life_span, weight: Detailed information provided for TheCatAPI images.
The CSV file is saved as cat_images_data.csv in the project folder.

