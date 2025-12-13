import os
import requests
import html

class KingsText:
    def __init__(self):
        os.makedirs(os.path.join(os.getcwd(), "data"), exist_ok=True)        

    def read_chapter(self, book: str, chapter: int) -> str:
        filename = self.get_chapter_filename(book, chapter)
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Chapter file {filename} does not exist. Please download it first.")
        
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    def download_chapter(self, book: str, chapter: int) -> str:
        try:
            existing_text = self.read_chapter(book, chapter)
            print(f"Chapter {chapter} of {book} already downloaded.")
            return existing_text
        except FileNotFoundError:
            pass

        url = f"https://www.sefaria.org/api/v3/texts/{book}%20{chapter}?version=primary&return_format=text_only"
        print(f"Downloading text for book {book}, chapter {chapter}...")

        response = requests.get(url)

        if response.status_code==404:
            print(f"Chapter {chapter} of {book} not found.")
            return ""

        response.raise_for_status()

        json = response.json()

        text = json.get("versions")[0].get("text")
        print(f"Downloaded {len(text)} verses.")

        self.save_chapter(book, chapter, text)
        return text        

    def save_chapter(self, book: str, chapter: int, text: list):
        filename = self.get_chapter_filename(book, chapter)
        print(f"Saving chapter to {filename}...")
        with open(filename, "w", encoding="utf-8") as f:
            for verse in text:
                # Convert HTML entities to plain text
                verse = html.unescape(verse)
                f.write(verse + "\n")
        print("Save complete.")

    def get_chapter_filename(self, book: str, chapter: int) -> str:        
        return os.path.join(os.getcwd(), "data", f"{book}_{chapter}.text.txt")
        
    
    