import os
import requests
from requests_oauthlib import OAuth1
import tkinter as tk
from tkinter import messagebox

# Etsy API credentials (placeholders, replace with your actual credentials)
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
OAUTH_TOKEN = 'your_oauth_token'
OAUTH_TOKEN_SECRET = 'your_oauth_token_secret'

# OAuth1 authentication
auth = OAuth1(API_KEY, API_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Etsy API endpoints
ETSY_CREATE_LISTING_URL = "https://openapi.etsy.com/v2/listings"
ETSY_UPLOAD_IMAGE_URL = "https://openapi.etsy.com/v2/listings/{listing_id}/images"

# Folder containing the product images
image_folder = "path/to/your/150_prototype_renders"

# Etsy fees information
listing_fee = 0.20
transaction_fee_percentage = 6.5
payment_processing_fee_us = 3.0
payment_processing_fee_flat = 0.25
num_products = 150
total_listing_fee = listing_fee * num_products

# Tkinter UI setup
def start_bot():
    # Confirm before starting the process
    start = messagebox.askyesno("Confirmation", f"Are you sure you want to list 150 products? This will cost you ${total_listing_fee:.2f} in listing fees.")
    if start:
        upload_products()

def upload_products():
    for idx, image_file in enumerate(os.listdir(image_folder)):
        image_path = os.path.join(image_folder, image_file)
        product_title = f"Prototype Product {idx + 1}"
        product_description = f"This is the detailed description for Prototype Product {idx + 1}"
        create_listing(product_title, product_description, '100.00', image_path)

def create_listing(product_title, product_description, price, image_path):
    data = {
        "title": product_title,
        "description": product_description,
        "price": price,
        "quantity": 10,
        "shipping_template_id": 123456789,  # Example template ID
        "who_made": "i_did",
        "is_supply": "false",
        "when_made": "made_to_order",
        "category_id": 69150344,  # Example category ID
        "tags": ['architecture', 'render', 'prototype'],
        "state": "draft",  # Set to 'active' to publish right away
    }

    response = requests.post(ETSY_CREATE_LISTING_URL, auth=auth, data=data)
    
    if response.status_code == 201:
        listing_id = response.json().get('listing_id')
        upload_image(listing_id, image_path)
    else:
        messagebox.showerror("Error", f"Failed to create listing: {response.status_code} - {response.text}")

def upload_image(listing_id, image_path):
    url = ETSY_UPLOAD_IMAGE_URL.format(listing_id=listing_id)
    files = {'image': open(image_path, 'rb')}
    
    response = requests.post(url, auth=auth, files=files)
    
    if response.status_code == 201:
        print(f"Image uploaded successfully for listing ID: {listing_id}")
    else:
        print(f"Failed to upload image: {response.status_code}, {response.text}")

# Create the Tkinter window
root = tk.Tk()
root.title("Etsy Automation Bot")
root.geometry("600x400")

# Display the fee information
info_text = f"""
Etsy Fee Information:
1. Listing Fee: $0.20 per product. Total for 150 products: ${total_listing_fee:.2f}
2. Transaction Fee: 6.5% of the sale price (including shipping and gift wrapping).
3. Payment Processing Fee (U.S.): 3% + $0.25 per transaction.
4. Optional: Additional costs if you use Etsy Ads for marketing.

Summary:
- You'll be charged ${total_listing_fee:.2f} for listing 150 products.
"""

label = tk.Label(root, text=info_text, justify="left")
label.pack(padx=10, pady=20)

# Create a "Connect" button that starts the bot
connect_button = tk.Button(root, text="Connect and Start Listing", command=start_bot, padx=10, pady=10, bg="green", fg="white")
connect_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
