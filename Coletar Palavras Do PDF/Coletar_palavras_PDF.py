import fitz  # PyMuPDF
from pdfminer.high_level import extract_text


import chardet
def detect_encoding(caminho):
    doc = fitz.open(caminho)
    page = doc[26]
    text = page.get_text("words")
    text = text[32][4]
    print(text)
    result = chardet.detect(text.encode())
    print(result['encoding'])
    input('---:> ')
    # return result['encoding']




def extract_bold_words(pdf_path):
    print('[#] Abrindo o PDF')
    with open(pdf_path, 'r', encoding='ascii') as file:
        pdf_bytes = file.read()

    # Transformar texto em binário (bytes)
    pdf_bytes = pdf_bytes.encode("ascii")

    doc = fitz.open('pdf', pdf_bytes)
    bold_words = []

    # num_paginas = doc.page_count
    print('[#] Iniciando varedura do PDF')
    num_paginas = 30+1
    for page_number in range(26, num_paginas):
        page = doc[page_number]
        words = page.get_text("words")

        for word in words:
            if "font" in word and word["font"].is_bold():
                bold_words.append(word["text"])

    doc.close()
    print('[#] Varedura finalizada PDF')
    return bold_words

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

if __name__ == "__main__":
    pdf_path = r".\Coletar Palavras Do PDF\31552-pdf.pdf"
    # detect_encoding(pdf_path)

    # Extrair palavras em negrito usando PyMuPDF
    print('[#] Iniciando coleta de dados do PDF')
    bold_words = extract_bold_words(pdf_path)
    print("Palavras em negrito (PyMuPDF):", bold_words)


    input('\n\n----::>> ')
    # Extrair todo o texto do PDF usando pdfminer
    all_text = extract_text_from_pdf(pdf_path)
    print("Texto completo (pdfminer):", all_text)
