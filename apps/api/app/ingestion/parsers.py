"""Parser skeletons. Replace stub logic with production extraction rules."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup


@dataclass
class ParsedDocument:
    text: str
    content_hash: str


def parse_html(url: str) -> ParsedDocument:
    response = httpx.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return ParsedDocument(text=text[:50000], content_hash=hashlib.sha256(text.encode()).hexdigest())


def parse_xlsx(file_path: str) -> dict:
    return {"status": "todo", "file_path": file_path}


def parse_pdf(file_path: str) -> dict:
    return {"status": "todo", "file_path": file_path}


def parse_university_page(url: str) -> ParsedDocument:
    return parse_html(url)


def import_manual_csv(file_path: str) -> dict:
    return {"status": "todo", "file_path": file_path}
