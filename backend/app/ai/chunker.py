from dataclasses import dataclass


@dataclass
class Chunk:
    index: int
    text: str
    char_start: int
    char_end: int

    @property
    def estimated_tokens(self) -> int:
        return len(self.text) // 4


class TextChunker:
    """Recursive character splitter with configurable size and overlap.

    Splits on: paragraphs → newlines → sentences → words (in order of preference).
    """

    _SEPARATORS = ["\n\n", "\n", ". ", "? ", "! ", " "]

    def split(
        self,
        text: str,
        chunk_size: int = 8000,
        overlap: int = 800,
    ) -> list[Chunk]:
        if not text.strip():
            return []

        raw_chunks = self._recursive_split(text.strip(), chunk_size)
        return self._apply_overlap(raw_chunks, text, overlap)

    def _recursive_split(self, text: str, chunk_size: int) -> list[str]:
        if len(text) <= chunk_size:
            return [text]

        for sep in self._SEPARATORS:
            if sep not in text:
                continue

            parts = text.split(sep)
            merged: list[str] = []
            current = ""

            for part in parts:
                candidate = current + sep + part if current else part
                if len(candidate) <= chunk_size:
                    current = candidate
                else:
                    if current:
                        merged.append(current)
                    # Part itself may be too large — recurse
                    if len(part) > chunk_size:
                        merged.extend(self._recursive_split(part, chunk_size))
                        current = ""
                    else:
                        current = part

            if current:
                merged.append(current)

            return merged if merged else [text]

        # No separator worked — hard split
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    def _apply_overlap(
        self, raw_chunks: list[str], original: str, overlap: int
    ) -> list[Chunk]:
        chunks: list[Chunk] = []
        cursor = 0

        for idx, chunk_text in enumerate(raw_chunks):
            start = original.find(chunk_text, cursor)
            if start == -1:
                start = cursor
            end = start + len(chunk_text)

            # Prepend tail of previous chunk for context overlap
            if idx > 0 and overlap > 0:
                prev_text = raw_chunks[idx - 1]
                tail = prev_text[-overlap:] if len(prev_text) > overlap else prev_text
                chunk_text = tail + "\n" + chunk_text

            chunks.append(Chunk(index=idx, text=chunk_text, char_start=start, char_end=end))
            cursor = end

        return chunks

    @staticmethod
    def select_relevant(chunks: list[Chunk], keywords: list[str], top_n: int = 8) -> list[Chunk]:
        """Return the top_n chunks most relevant to the given keywords by word overlap."""
        if not keywords:
            return chunks[:top_n]

        kw_set = {k.lower() for k in keywords}

        def score(chunk: Chunk) -> float:
            words = set(chunk.text.lower().split())
            return len(words & kw_set) / max(len(kw_set), 1)

        ranked = sorted(chunks, key=score, reverse=True)
        return sorted(ranked[:top_n], key=lambda c: c.index)
