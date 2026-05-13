from flask import Flask, render_template, request, send_file
from newspaper import Article
from fpdf import FPDF
import io

app = Flask(__name__)

def generate_pdf_buffer(url):
    article = Article(url)
    article.download()
    article.parse()

    pdf = FPDF()
    pdf.add_page()
    
    # Title - Using a standard font
    pdf.set_font("Arial", 'B', 16)
    title = article.title.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, title)
    pdf.ln(10)
    
    # Body Text
    pdf.set_font("Arial", size=12)
    clean_text = article.text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    
    # Generate PDF in memory
    pdf_output = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_output)
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    article_url = request.form.get('url')
    if not article_url:
        return "Please provide a URL", 400
    
    try:
        pdf_file = generate_pdf_buffer(article_url)
        return send_file(
            pdf_file,
            as_attachment=True,
            download_name="article.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Error processing article: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
