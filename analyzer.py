import json
import os
from prompt_toolkit import prompt
from pydantic import BaseModel, Field
from typing import List
from google import genai
from hebrew_numbers import int_to_gematria

class ImportantDetail(BaseModel):
    name : str = Field(description="Put here the name of the character")
    description: str = Field(description="Put here a one or two lines description of the character")
    
class ChapterSummary(BaseModel):
    chapter : str = Field(description="Put here the book and chapter number in Hebrew, e.g., מלכים ב פרק א")
    synopsis : str = Field(description="Put here 100 words synopsis of the chapter. ")
    characters: List[ImportantDetail] = Field(description="Put here a list *ALL* characters mentioned in the chapter")
    places: List[ImportantDetail] = Field(description="Put here a list places mentioned in the chapter")

class Analyzer:
    
    def __init__(self):
        self.client = genai.Client()
        
        
    def load_summary(self, book: str, chapter: int) -> ChapterSummary:
        filename = self.get_summary_filename(book, chapter)
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Summary file {filename} does not exist. Please summarize the chapter first.")
        
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return ChapterSummary.model_validate(data)
        
    def summarize_chapter(self, book_number:str, chapter_number: int, chapter_text: str) -> ChapterSummary:      
        try:
            existing_summary = self.load_summary(book_number, chapter_number)
            print(f"Chapter {chapter_number} of {book_number} already summarized.")
            return existing_summary
        except FileNotFoundError:
            pass        
        
        prompt = self.load_prompt_template("prompt.tmpl",{
            "CHAPTER":int_to_gematria(chapter_number),
            "BOOK_NAME":convert_book_name_to_hebrew(book_number),
            "JSON_SAMPLE": load_response_sample(),
            "TEXT": chapter_text
            }
            )
        
        system_instruction = self.load_prompt_template("system_instructions.tmpl",{})
        
        print(f"Chapter {book_number} {chapter_number} sending to Gemini for summarization...")
        
        try: 
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "system_instruction":system_instruction,
                    "response_mime_type": "application/json",
                    "response_json_schema": ChapterSummary.model_json_schema(),
                }
            )
            summary = ChapterSummary.model_validate(json.loads(response.text))
        except Exception as e:
            print("Error during summarization:", e)
            print("Response was:", response.text)
        
        # word_count = len(summary.synopsis.split())
        # if word_count < 80 or word_count > 150:
        #         print(f"Synopsis word count ({word_count}) out of range (80-150). Requesting again...")
        #         return self.summarize_chapter(book_number, chapter_number, chapter_text)
        
        print(summary.synopsis)
        
        self.save_summary(book_number, chapter_number, summary)
        print(f"Chapter {book_number} {chapter_number} summarization complete.")    
        return summary
        
    def load_prompt_template(self, template_path: str, variables: dict) -> str:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        for key, value in variables.items():
            template = template.replace(key, str(value))
        return template
    
    def save_summary(self, book: str, chapter: int, summary: ChapterSummary):
        filename = self.get_summary_filename(book, chapter)
        print(f"Saving summary to {filename}...")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(summary.model_dump_json(indent=4, ensure_ascii=False))
        print("Save complete.")
        
    def get_summary_filename(self, book: str, chapter: int) -> str:                  
        return os.path.join(os.getcwd(), "data", f"{book}_{chapter}.summary.json")
        
    
def convert_book_name_to_hebrew(book_name: str) -> str:
    book_mapping = {
        "I_Kings": "מלכים א",
        "II_Kings": "מלכים ב",
    }
    return book_mapping.get(book_name, book_name)

def load_response_sample() -> str:
    with open("response.tmpl", "r", encoding="utf-8") as f:
        return f.read()