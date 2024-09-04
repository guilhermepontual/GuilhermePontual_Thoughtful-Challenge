import pandas as pd
import re
import requests
import os
import logging


def save_to_excel(news_data, file_path):
    df = pd.DataFrame(news_data)

    df.to_excel(file_path, index=False, engine='openpyxl')

    logging.info(f"Save Data in {file_path}")
    return file_path


def contains_money(text):
    pattern = r'\$\d+(,\d{3})*(\.\d{2})?|\d+ dollars|\d+ USD'
    return bool(re.search(pattern, text))


def get_image_src(image_element):
    return image_element.get_attribute("src")
