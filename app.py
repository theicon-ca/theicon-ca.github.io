import nltk
from newspaper import Article, Config

# This only needs to run once when the server starts
nltk.download('punkt')

def generate_pdf_buffer(url):
    # 1. Setup a "User-Agent" to mimic a real browser
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10 # Don't wait forever

    # 2. Initialize and Download
    article = Article(url, config=config)
    article.download()
    article.parse()
    
    # NLP helps the library identify the actual 'body' of text
    article.nlp()

    # 3. Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Formatting Title
    pdf.set_font("Arial", 'B', 16)
    title = article.title.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, title)
    pdf.ln(10)
    
    # Formatting Body
    pdf.set_font("Arial", size=12)
    # We use article.text which is the cleaned version
    body_text = article.text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, body_text)
    
    # Generate buffer
    pdf_output = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_output)
    buffer.seek(0)
    return buffer
