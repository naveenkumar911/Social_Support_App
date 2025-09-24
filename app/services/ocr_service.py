from pathlib import Path
try:
    import easyocr
    READER = easyocr.Reader(['en'])
except Exception:
    READER = None
    try:
        import pytesseract
        from PIL import Image
    except Exception:
        pytesseract = None

def extract_text_from_image(path: str):
    p = Path(path)
    if READER is not None:
        res = READER.readtext(str(p))
        # easyocr returns list of (bbox,text,confidence)
        texts = [r[1] for r in res]
        return "\\n".join(texts)
    if 'pytesseract' in globals() and pytesseract is not None:
        img = Image.open(path)
        txt = pytesseract.image_to_string(img)
        return txt
    # fallback mock: read file as text if it's a .txt, else return placeholder
    if p.suffix.lower() == '.txt':
        return p.read_text()
    return 'OCR not available in environment - please install easyocr or pytesseract.'