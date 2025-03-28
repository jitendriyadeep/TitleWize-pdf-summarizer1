import os
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import google.generativeai as genai # type: ignore
from django.conf import settings

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    output = StringIO()
    with open(pdf_path, 'rb') as pdf_file:
        extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='text', codec=None)
    return output.getvalue()

def generate_summary(text, length='medium'):
    """Generate professional legal summary with HTML formatting."""
    word_limits = {
        'short': 500,
        'medium': 2000,
        'long': 5000
    }
    
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        if length == 'short':
            prompt = f"""
            Create a concise legal summary of this document with the following structure:

            === STRUCTURED ANALYSIS ===
            <div class="legal-section">
            <h3>Parties</h3>
            <ul>
              <li><strong>Vendor:</strong> [Full details with PAN]</li>
              <li><strong>Purchaser:</strong> [Full details with PAN]</li>
            </ul>

            <h3>Property Particulars</h3>
            <ul>
              <li><strong>Survey No:</strong> [Details]</li>
              <li><strong>Extent:</strong> [Measurement]</li>
            </ul>

            <h3>Financial Terms</h3>
            <ul>
              <li><strong>Total Consideration:</strong> ₹[Amount]</li>
              <li><strong>Payment Schedule:</strong> [Details]</li>
            </ul>
            </div>

            === PROFESSIONAL LEGAL SUMMARY ===
            <div class="legal-summary">
            <p>[Concise 1-2 paragraph summary highlighting:</p>
            <ul>
              <li>Nature of transaction</li>
              <li>Key legal clauses</li>
              <li>Important obligations</li>
              <li>Notable restrictions</li>
              <li>Governing laws</li>
            </ul>
            <p>Include exact quotes of critical legal language marked with <blockquote> tags]</p>
            </div>

            Formatting Rules:
            1. Use proper HTML tags (<strong>, <ul>, <li>)
            2. Wrap legal quotes in <blockquote class="legal-quote">
            3. Highlight governing laws with <span class="law-reference">
            4. Never use markdown (**), only HTML
            5. Preserve all exact numerical values
            """
        elif length == 'medium':
            prompt = f"""
            Create a comprehensive legal summary of this document with the following structure:

            === STRUCTURED ANALYSIS ===
            <div class="legal-section">
            <h3>Parties</h3>
            <ul>
              <li><strong>Vendor:</strong> [Full details with PAN]</li>
              <li><strong>Purchaser:</strong> [Full details with PAN]</li>
            </ul>

            <h3>Property Particulars</h3>
            <ul>
              <li><strong>Survey No:</strong> [Details]</li>
              <li><strong>Extent:</strong> [Measurement]</li>
            </ul>

            <h3>Financial Terms</h3>
            <ul>
              <li><strong>Total Consideration:</strong> ₹[Amount]</li>
              <li><strong>Payment Schedule:</strong> [Details]</li>
            </ul>
            </div>

            === PROFESSIONAL LEGAL SUMMARY ===
            <div class="legal-summary">
            <p>[Concise 3-5 paragraph summary highlighting:</p>
            <ul>
              <li>Nature of transaction</li>
              <li>Key legal clauses</li>
              <li>Important obligations</li>
              <li>Notable restrictions</li>
              <li>Governing laws</li>
            </ul>
            <p>Include exact quotes of critical legal language marked with <blockquote> tags]</p>
            </div>

            Formatting Rules:
            1. Use proper HTML tags (<strong>, <ul>, <li>)
            2. Wrap legal quotes in <blockquote class="legal-quote">
            3. Highlight governing laws with <span class="law-reference">
            4. Never use markdown (**), only HTML
            5. Preserve all exact numerical values
            """
        elif length == 'long':
            prompt = f"""
            Create a detailed legal analysis of this document with the following structure:

            === STRUCTURED ANALYSIS ===
            <div class="legal-section">
            <h3>Parties</h3>
            <ul>
              <li><strong>Vendor:</strong> [Full details with PAN]</li>
              <li><strong>Purchaser:</strong> [Full details with PAN]</li>
            </ul>

            <h3>Property Particulars</h3>
            <ul>
              <li><strong>Survey No:</strong> [Details]</li>
              <li><strong>Extent:</strong> [Measurement]</li>
            </ul>

            <h3>Financial Terms</h3>
            <ul>
              <li><strong>Total Consideration:</strong> ₹[Amount]</li>
              <li><strong>Payment Schedule:</strong> [Details]</li>
            </ul>
            </div>

            === PROFESSIONAL LEGAL SUMMARY ===
            <div class="legal-summary">
            <p>[Detailed 5-10 paragraph summary highlighting:</p>
            <ul>
              <li>Nature of transaction</li>
              <li>Key legal clauses</li>
              <li>Important obligations</li>
              <li>Notable restrictions</li>
              <li>Governing laws</li>
            </ul>
            <p>Include exact quotes of critical legal language marked with <blockquote> tags]</p>
            </div>

            Formatting Rules:
            1. Use proper HTML tags (<strong>, <ul>, <li>)
            2. Wrap legal quotes in <blockquote class="legal-quote">
            3. Highlight governing laws with <span class="law-reference">
            4. Never use markdown (**), only HTML
            5. Preserve all exact numerical values
            """
        
        # Adjust the prompt based on the desired length
        prompt += f"\nGenerate a summary of approximately {word_limits[length]} words."
        
        response = model.generate_content(prompt + text[:50000])
        summary = response.text
        
        # Ensure the summary does not exceed the word limit
        words = summary.split()
        if len(words) > word_limits[length]:
            summary = ' '.join(words[:word_limits[length]])
        summary = summary.strip()
        summary = ' '.join(summary.split())
        
        return summary
        
    except Exception as e:
        print(f"Error: {e}")
        return None