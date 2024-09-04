# Thoughtful Automation Challenge

## Overview

This repository contains the solution for the Thoughtful Automation Challenge. The goal of this challenge is to automate the process of extracting news articles from a specific news website, saving the extracted data into an Excel file, and configuring the automation to run on Robocorp Control Room.

## Prerequisites

To run this project locally or on Robocorp Control Room, you will need the following:

- **Python 3.8+**: Make sure Python is installed on your system.
- **pip**: Python's package installer.
- **Robocorp Automation Studio (Optional)**: If you are using Robocorp for deployment.
- **Git**: To clone the repository and manage version control.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/guilhermepontual/GuilhermePontual_Thoughtful-Challenge.git
   cd ThoughtfulChallenge
   
2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate

3. **Install the required dependencies**:
   ```bash
   If using pip:
        pip install -r requirements.txt
   
## Configuration

The input parameters for the automation are provided either through a JSON file for local execution or via Robocorp Work Items in the cloud environment.

### Input JSON Configuration (Local Execution)

Create or modify the input.json file located at devdata/work_items/input.json

1. **Install the required dependencies**:
   ```bash
   {
     "search_phrase": "technology",
     "number_of_months": 2
   }

- **search_phrase**: The phrase to search for in the news articles.
- **number_of_months**: The number of months for which you want to retrieve news articles.

### Local Execution

1. **Run the automation**:
   ```bash
   python src/main.py
   
2. **Output**:
   ```bash
   The extracted news data will be saved in an Excel file located at src/output/news_data.xlsx
