import logging
import os
import json
from RPA.Robocorp.WorkItems import WorkItems
from scraper import NewsScraper
from utils import save_to_excel


def main():
    logging.basicConfig(level=logging.INFO)

    if "RC_WORKSPACE_ID" in os.environ:
        work_items = WorkItems()
        work_items.get_input_work_item()

        search_phrase = work_items.get_work_item_variable("search_phrase")
        number_of_months = int(work_items.get_work_item_variable("number_of_months"))
    else:
        input_file_path = os.path.join("..", "devdata", "work_items", "input.json")
        with open(input_file_path, "r") as f:
            data = json.load(f)

        search_phrase = data.get("search_phrase")
        number_of_months = int(data.get("number_of_months"))

    scraper = NewsScraper(search_phrase, number_of_months)
    news_data = scraper.run()

    excel_path = save_to_excel(news_data, "output/news_data.xlsx")

    if "RC_WORKSPACE_ID" in os.environ:
        work_items.create_output_work_item({"output_file": excel_path})
        work_items.save_output_work_item()


if __name__ == "__main__":
    main()
