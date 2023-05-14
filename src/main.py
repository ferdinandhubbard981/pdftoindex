import os
import re
import PyPDF2
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from collections import defaultdict
import argparse
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


def extract_words(pdf_path, blacklist):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Create a dictionary to store words and their page numbers
        word_pages = defaultdict(set)

        # Go through each page
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            words = re.findall(r'\b\w+\b', page.extract_text())

            # Store each word and its page number
            for word in words:
                word = word.lower()  # make word lowercase
                if word not in blacklist:
                    word_pages[word].add(page_num + 1)  # add 1 to start pages at 1

    return word_pages


def create_index_pdf(word_pages, dir_path):
    # Create the index.pdf file
    index_pdf_path = os.path.join(dir_path, "index.pdf")

    doc = SimpleDocTemplate(index_pdf_path, pagesize=letter)
    Story = []
    styles = getSampleStyleSheet()

    # Sort the words
    sorted_words = sorted(word_pages.keys(), key=lambda word: word.lower())

    # Write each word and its pages
    for word in sorted_words:
        pages = sorted(word_pages[word])
        text = f"{word}: {', '.join(map(str, pages))}"
        para = Paragraph(text, styles["BodyText"])
        Story.append(para)
        Story.append(Spacer(1, 12))

    doc.build(Story)


def main(args):
    pdf_path = args.pdf
    blacklist_path = args.blacklist
    dir_path = args.dir

    # Read the blacklist words
    with open(blacklist_path, 'r') as file:
        blacklist = set(line.strip().lower() for line in file)  # make blacklist words lowercase

    # Extract the words and their pages from the PDF
    word_pages = extract_words(pdf_path, blacklist)

    # Create the index.pdf file
    create_index_pdf(word_pages, dir_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a PDF file and create an index PDF.")
    parser.add_argument("--pdf", help="Path to the PDF file")
    parser.add_argument("--blacklist", help="Path to the blacklist file")
    parser.add_argument("--dir", help="Path to the output directory")
    args = parser.parse_args()

    main(args)
