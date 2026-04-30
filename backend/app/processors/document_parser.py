import re
import unicodedata
from pathlib import Path


class DocumentParser:
    """Extract and clean plain text from supported document formats."""

    SUPPORTED_MIME = {
        "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    def parse_file(self, path: str | Path, mime_type: str) -> str:
        """Dispatch to format-specific parser and return clean text."""
        path = Path(path)
        if mime_type == "text/plain":
            return self._parse_txt(path)
        if mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return self._parse_docx(path)
        raise ValueError(f"Unsupported MIME type: {mime_type}")

    def parse_bytes(self, data: bytes, mime_type: str) -> str:
        """Parse from raw bytes without writing to disk."""
        if mime_type == "text/plain":
            return self._clean(data.decode("utf-8", errors="replace"))
        if mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return self._parse_docx_bytes(data)
        raise ValueError(f"Unsupported MIME type: {mime_type}")

    # ── Format parsers ────────────────────────────────────────

    def _parse_txt(self, path: Path) -> str:
        text = path.read_text(encoding="utf-8", errors="replace")
        return self._clean(text)

    def _parse_docx(self, path: Path) -> str:
        return self._parse_docx_bytes(path.read_bytes())

    @staticmethod
    def _parse_docx_bytes(data: bytes) -> str:
        import io
        from docx import Document

        doc = Document(io.BytesIO(data))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return DocumentParser._clean("\n\n".join(paragraphs))

    # ── Text cleaning ─────────────────────────────────────────

    @staticmethod
    def _clean(text: str) -> str:
        # Normalize unicode (NFC) and remove control characters except \n \t
        text = unicodedata.normalize("NFC", text)
        text = re.sub(r"[^\S\n\t ]+", " ", text)   # collapse unusual whitespace
        text = re.sub(r"\r\n?", "\n", text)          # normalize line endings
        text = re.sub(r"\n{4,}", "\n\n\n", text)     # max 3 consecutive newlines
        text = re.sub(r" {2,}", " ", text)            # collapse multiple spaces
        return text.strip()
