import streamlit as st
import openai
import requests
import http.client
import json
from PIL import Image
from io import BytesIO

# Set your API keys
openai.api_key = "openai-api-key"
EBAY_API_KEY = "ebay-api-key"

def fetch_ebay_products(query, country="US"):
    conn = http.client.HTTPSConnection("ebay38.p.rapidapi.com")
    headers = {
        "x-rapidapi-key": EBAY_API_KEY,
        "x-rapidapi-host": "ebay38.p.rapidapi.com"
    }
    conn.request("GET", f"/search?query={query}&country={country}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    try:
        return json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        return []

def recommend_product_from_list(user_interests, ebay_products):
    product_list = "\n".join([
        f"{i+1}. {product['title']} - {product.get('buyItNowPrice', 'No Price')} {product.get('currency', 'USD')}"
        for i, product in enumerate(ebay_products)
    ])

    prompt = f"""
    The user is interested in the topic: {user_interests}.
    Here is a list of products fetched from eBay based on their interests:

    {product_list}

    Select the best product for the user and provide a short one-sentence description of why this product is suitable.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful product recommendation assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

def generate_advertisement(user_interests, product_name, product_description):
    prompt = f"""
    The user is interested in the following topics: {user_interests}.
    Create a compelling advertisement for the following product in one sentence:

    Product Name: {product_name}
    Product Description: {product_description}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative advertising assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content.strip()

def generate_advertisement_image(product_name, product_description):
    try:
        prompt = f"""
        Create an artistic and visually engaging image to advertise the product '{product_name}'.
        The product is described as: {product_description}.
        """

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256",
            response_format="url"
        )
        return response['data'][0]['url']
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

# Streamlit App
st.title("Advertise Recommendation System")
st.sidebar.title("User Input")

# User Input
user_interests = st.sidebar.text_input("Enter your interests (e.g., fitness, technology, yoga):", "fitness")

if st.sidebar.button("Fetch Products and Generate Recommendations"):
    with st.spinner("Fetching products from eBay..."):
        ebay_data = fetch_ebay_products(user_interests)

    if not ebay_data:
        st.error("No products found on eBay for your interests.")
    else:
        st.subheader("Fetched eBay Products:")
        for i, product in enumerate(ebay_data):
            title = product.get('title', 'No Title')
            price = product.get('buyItNowPrice', 'No Price')
            currency = product.get('currency', 'USD')
            url = product.get('url', 'No URL')

            st.markdown(f"{i+1}. **{title}**")
            st.markdown(f"   - Price: {price} {currency}")
            st.markdown(f"   - [Product Link]({url})")

        # Recommendation
        recommendation = recommend_product_from_list(user_interests, ebay_data)
        st.subheader("Recommended Product:")
        st.write(recommendation)

        # Parse recommendation
        try:
            product_name = recommendation.split(" - ")[0]
            product_description = recommendation.split(": ")[-1]
        except IndexError:
            product_name = "Unknown Product"
            product_description = "No Description Available"

        # Advertisement
        ad_text = generate_advertisement(user_interests, product_name, product_description)
        st.subheader("Generated Advertisement:")
        st.write(ad_text)

        # Advertisement Image
        ad_image_url = generate_advertisement_image(product_name, product_description)
        if ad_image_url:
            st.image(ad_image_url, caption="Generated Advertisement Image")
