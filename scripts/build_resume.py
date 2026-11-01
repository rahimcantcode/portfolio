"""Build the public résumé and its preview from the same source.

Run from any directory: python3 scripts/build_resume.py
Requires reportlab and PyMuPDF (see requirements-resume.txt).
"""
from pathlib import Path
from xml.sax.saxutils import escape

import fitz
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / 'files' / 'Rahim_Latreche_Resume.pdf'
PREVIEW = ROOT / 'images' / 'resume-preview.png'

styles = {
    'name': ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=19, leading=22, alignment=TA_CENTER),
    'contact': ParagraphStyle('contact', fontName='Helvetica', fontSize=8.5, leading=12, alignment=TA_CENTER),
    'section': ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor('#123b55'), spaceBefore=9, spaceAfter=4),
    'role': ParagraphStyle('role', fontName='Helvetica-Bold', fontSize=9.5, leading=12, spaceBefore=4),
    'meta': ParagraphStyle('meta', fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor('#444444'), spaceAfter=3),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=3),
    'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=9, leading=12, leftIndent=10, firstLineIndent=-8, spaceAfter=3),
}
story = []
def add(text, style='body'):
    story.append(Paragraph(text, styles[style]))
def section(text):
    add(text, 'section')
def role(title, meta, bullets):
    block = [Paragraph(escape(title), styles['role']), Paragraph(escape(meta), styles['meta'])]
    block.extend(Paragraph('- ' + escape(b), styles['bullet']) for b in bullets)
    story.append(KeepTogether(block))

add('Abderrahim (Rahim) Latreche', 'name')
add('<link href="mailto:alatreche@smu.edu">alatreche@smu.edu</link> | Dallas, TX | 469-922-5033', 'contact')
add('<link href="https://github.com/rahimcantcode">github.com/rahimcantcode</link> | <link href="https://www.linkedin.com/in/abderrahimlatreche">linkedin.com/in/abderrahimlatreche</link>', 'contact')
section('Education')
add('<b>Southern Methodist University</b> | Dallas, TX')
add('M.S. Computer Science, AI/ML Specialization | Expected Dec 2026')
add('B.S. Computer Science (AI/ML Track) and Data Science | Dec 2025 | GPA: 3.9/4.0')
section('Technical Skills')
add('<b>AI / Data:</b> Python, SQL, Snowflake Cortex Analyst/Search/Agents, Snowpark, semantic modeling, RAG, vector search, LangGraph, FAISS, scikit-learn, TensorFlow, Hugging Face')
add('<b>Engineering:</b> JavaScript, React, Next.js, Node.js, Express, FastAPI, REST APIs, Git, Linux, Nginx, systemd, Azure DevOps')
section('Experience')
role('CBRE SmartFM | Data Science Intern', 'Jun 2026 - Aug 2026 | Dallas, TX | Insights Explorer', [
    'Owned the maintenance-data-to-agent workflow using Snowflake Cortex Analyst, Search, and Agents for conversational analytics.',
    'Built a semantic model with 10 logical tables, 13 relationships, 60+ facts, dimensions, and metrics, and 12 verified SQL templates for grounded text-to-SQL.',
    'Fixed VARIANT-derived join keys through staging-view columns to enable building-level rollups; automated version-preserving deployment across 5 LLM variants.',
    'Built a Snowpark pipeline for irregular Excel tables using structural heuristics and selective LLM assistance; added fallback, quality/cost telemetry, and custom test fixtures. Kept client data inside Snowflake.',
])
role('CBRE | Software Engineering Intern', 'Jun 2025 - Aug 2025 | Dallas, TX', [
    'Cleaned and transformed 5M+ HVAC time-series records into features and labeled datasets for fault-detection model development and evaluation against domain-expert rules.',
    'Built semantic sensor matching with FAISS and embeddings to map natural-language HVAC fault rules to equipment metadata across enterprise portfolios.',
])
role('Toyota Financial Services | Data Engineer, Sponsored Senior Design', 'Aug 2025 - Dec 2025 | Plano, TX | Academic project', [
    'Developed Quorra, a React, Python, and REST API query portal with authenticated access, query history, result previews, and downloads.',
    'Built schema inspection, column summaries, and portfolio analytics workflows for data exploration and SQL query construction.',
])
role('Southern Methodist University | SURF Research Fellow, NLP', 'May 2025 - Aug 2025 | Dallas, TX', [
    'Built an AI advising assistant with transformer-based NLP and curated advising datasets; evaluated intent classification and retrieval with precision, recall, and latency.',
])
section('Selected Projects')
role('Bias Checker | Hugging Face, FastAPI, Next.js', 'github.com/rahimcantcode/biasCheck', [
    'Built article, sentence, and paragraph predictions with inline passage coloring and inspectable model scores; deployed on a Linux VPS with Nginx, HTTPS, and systemd.',
])
role('Logistic Regression from Scratch | Python, NumPy, scikit-learn', 'Optimization, regularization, and dimensionality reduction', [
    'Implemented multiclass logistic regression with gradient ascent, SGD, and Newton\'s method; explored L1/L2/ElasticNet and PCA retaining 95% variance with 10 of 23 features.',
])

def main():
    # An invariant PDF timestamp makes regeneration reproducible.
    doc = SimpleDocTemplate(str(PDF), pagesize=letter, rightMargin=36, leftMargin=36,
                            topMargin=28, bottomMargin=28, title='Abderrahim Latreche - Resume',
                            author='Abderrahim Latreche', invariant=1)
    doc.build(story)
    with fitz.open(PDF) as pdf:
        if len(pdf) != 1:
            raise ValueError(f'Resume must fit on one page, got {len(pdf)}')
        pdf[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).save(PREVIEW)
    print(f'Built {PDF.relative_to(ROOT)} and {PREVIEW.relative_to(ROOT)}')

if __name__ == '__main__':
    main()
