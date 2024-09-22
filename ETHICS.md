### **`ETHICS.md`**

```markdown
# Ethical Considerations

## Data Collection

This project uses two sources of data:
1. **TheCatAPI**: Data from this API is accessed via an API key, adhering to TheCatAPI's terms of service. The API provides high-quality, publicly available images with detailed breed metadata.
2. **iStock Web Scraping**: The project scrapes publicly available images from iStock, ensuring that the scraping respects the website’s `robots.txt` file. Only a limited number of non-premium images are gathered for educational and research purposes.

The data collected is used solely for non-commercial research and educational purposes. All sources are credited appropriately.

## Consent and Copyright

The project carefully adheres to the following considerations:
- **API Use Compliance**: TheCatAPI allows developers to use its API under specific terms. We follow their usage guidelines and do not violate their terms.
- **iStock Scraping**: We scrape publicly available images while respecting the website’s terms and conditions. The scraped images are not used for redistribution or any commercial purposes. We ensure that only non-premium, publicly available images are accessed.
  
The project clearly states that the scraped images from iStock are used solely for the purpose of building an educational dataset and are not meant for any redistribution or commercial use. We encourage users of this dataset to follow the same principles.

## AI and Bias

The AI model (ResNet50) used for breed prediction may have biases due to the limitations of the training data used in the original ImageNet dataset. The breed predictions are not always 100% accurate, and users are informed of the potential for misclassification.

We acknowledge that the breed prediction is AI-based and may not always reflect the actual breed. We recommend using this information for educational purposes only and not for any real-world decision-making regarding cats.

## Privacy

No personally identifiable information (PII) is collected or processed in this project. The dataset only includes publicly available images of animals (cats).

## Accessibility and Fair Use

This project is intended for educational purposes only. Users are encouraged to use the dataset under fair use guidelines for research, education, or personal projects, and not for commercial purposes.

The dataset created should not be misused to infringe on the rights of the original content creators. We encourage ethical use of all resources and adherence to copyright laws.
```
