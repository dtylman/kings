from analyzer import ChapterSummary
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

class Summarizer:
    doc = None
    
    def __init__(self):
        self.doc = Document()
        # Add a title
        title = self.doc.add_heading('Book of Kings - Chapter Summaries', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    def set_summary(self, summary: ChapterSummary):
        # Add chapter heading
        heading = self.doc.add_heading(summary.chapter, level=1)
        
        # Add synopsis paragraph
        synopsis_heading = self.doc.add_heading('Synopsis:', level=2)
        synopsis_para = self.doc.add_paragraph(summary.synopsis)
        
        # Add characters section
        if summary.characters:
            chars_heading = self.doc.add_heading('Characters:', level=2)
            for char in summary.characters:
                char_para = self.doc.add_paragraph(style='List Bullet')
                char_para.add_run(f"{char.name}: ").bold = True
                char_para.add_run(char.description)
        
        # Add places section
        if summary.places:
            places_heading = self.doc.add_heading('Places:', level=2)
            for place in summary.places:
                place_para = self.doc.add_paragraph(style='List Bullet')
                place_para.add_run(f"{place.name}: ").bold = True
                place_para.add_run(place.description)
        
        # Add page break after each chapter (except we'll handle this in save)
        self.doc.add_paragraph()
    
    def save(self, filename='kings_summary.docx'):
        self.doc.save(filename)
        print(f"Summary saved to {filename}")