import os
import PyPDF2
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from collections import defaultdict
import argparse


def extract_words(pdf_path, blacklist):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Create a dictionary to store words and their page numbers
        word_pages = defaultdict(set)

        # Go through each page
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            words = page.extract_text().split()

            # Store each word and its page number
            for word in words:
                if word not in blacklist:
                    word_pages[word].add(page_num + 1)  # add 1 to start pages at 1

    return word_pages


def create_index_pdf(word_pages, dir_path):
    # Create the index.pdf file
    index_pdf_path = os.path.join(dir_path, "index.pdf")
    c = canvas.Canvas(index_pdf_path, pagesize=letter)

    # Sort the words
    sorted_words = sorted(word_pages.keys(), key=lambda word: word.lower())

    textobject = c.beginText()
    textobject.setFont("Helvetica", 10)
    textobject.setTextOrigin(10, 750)

    # Write each word and its pages
    for word in sorted_words:
        pages = sorted(word_pages[word])
        textobject.textLine(f"{word}: {', '.join(map(str, pages))}")

        # Start a new page if the current one is full
        if textobject.getY() <= 50:
            c.drawText(textobject)
            c.showPage()
            textobject = c.beginText()
            textobject.setFont("Helvetica", 10)
            textobject.setTextOrigin(10, 750)

    # Draw the last text object and save the PDF
    c.drawText(textobject)
    c.save()


def main(args):
    pdf_path = args.pdf
    blacklist_path = args.blacklist
    dir_path = args.dir

    # Read the blacklist words
    with open(blacklist_path, 'r') as file:
        blacklist = set(line.strip() for line in file)

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
