# slate_text_extraction.py

import slate

def extract_text_from_pdf(pdf_path):
    with open(pdf_path) as fh:
        document = slate.PDF(fh, password='', just_text=1)

        for pasd in document:
            print(page)

if __name__ == '__main__':
    extract_text_from_pdf('L200.pdf')
