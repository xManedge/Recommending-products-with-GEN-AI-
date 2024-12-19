# Ad-recommendation-system-using-GenAI

# Project Documentation

## Overview
This project is an advertisement recommendation system that fetches products from eBay based on user interests, recommends a suitable product, and generates a creative advertisement with an image.

## Code Structure
The project is structured as follows:

- **main.py**: Contains the main application logic implemented using Streamlit.
- **fetch_ebay_products**: Function to fetch product data from eBay using RapidAPI.
- **recommend_product_from_list**: Function to recommend the most suitable product based on user interests.
- **generate_advertisement**: Function to generate a textual advertisement for the recommended product.
- **generate_advertisement_image**: Function to generate an image-based advertisement using OpenAI's image generation API.

## How to Prepare to Run

### Prerequisites

1. Install Python 3.7 or higher.
2. Set up API keys for OpenAI and eBay RapidAPI.
3. Install required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Clone the repository to your local machine.

   ```bash
   git clone https://github.com/Ad-recommendation-system-using-GenAI.git
   cd Ad-recommendation-system-using-GenAI
   ```

2. Install the dependencies as outlined above.

3. Run the Streamlit application:

   ```bash
   streamlit run main.py
   ```

4. Open the provided URL in your browser to interact with the application.

## What the Code Does

1. **Fetch Products**: Retrieves a list of products from eBay based on the user-provided interests.
2. **Recommend Product**: Selects the most relevant product using OpenAI's GPT model.
3. **Generate Advertisement**: Creates a textual advertisement for the recommended product.
4. **Generate Image**: Generates a creative image advertisement for the product.

---

For additional details, refer to the inline comments in the code or contact the project maintainer.
