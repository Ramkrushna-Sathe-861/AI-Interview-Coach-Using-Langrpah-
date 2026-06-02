from typing import Optional
from pathlib import Path
import pdfplumber

class ResumeParser:
    def extract_text(self, file_path: str) -> str:
        extension = Path(file_path).suffix.lower()
        if extension == ".pdf":
            return self._extract_pdf_text(file_path)
        if extension == ".txt":
            return Path(file_path).read_text(encoding="utf-8", errors="ignore")
        raise ValueError("Unsupported resume file format. Use PDF or TXT.")

    def _extract_pdf_text(self, file_path: str) -> str:
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)
