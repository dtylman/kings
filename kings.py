#!/usr/bin/env python3

import os
from kings_text import KingsText
from analyzer import Analyzer
from summarizer import Summarizer


def main():
    # if API key is not set - tell user and exit
    if not os.getenv("GEMINI_API_KEY"):
        print("Please set the GEMINI_API_KEY environment variable.")
        print("You can get an API key from https://aistudio.google.com/api-keys")
        return
    
    kings = KingsText()
    analyzer = Analyzer()
    summarizer = Summarizer()
    for chapter in range(1, 9):
        txt = kings.download_chapter("I_Kings", chapter)        
        summary = analyzer.summarize_chapter("I_Kings", chapter, txt)
        summarizer.set_summary(chapter, summary)
    
    summarizer.save()
    
if __name__ == "__main__":        
    main()
