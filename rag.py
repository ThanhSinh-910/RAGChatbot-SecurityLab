"""Shared document indexing and RAG helpers for the CLI and Streamlit apps."""

import hashlib
import json
import math
import os
from pathlib import Path
import re

# Tự động nạp biến môi trường từ file .env nếu có (hỗ trợ python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv chưa cài — vẫn dùng được nếu đặt biến môi trường thủ công

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent
INDEX_DIR = BASE_DIR / ".rag_index"
REAL_VKU_DIR = BASE_DIR / "experiments" / "data" / "real_vku"
REAL_VKU_CORPUS = REAL_VKU_DIR / "chunks" / "QD1416-demo-corpus.jsonl"
REAL_VKU_FULL_CORPUS = REAL_VKU_DIR / "chunks" / "QD1416-full-corpus.jsonl"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
def get_embeddings():
    """Create the local embedding model. Hugging Face caches its files separately."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def get_real_vku_fingerprint(corpus_type: str = "demo") -> str:
    """Hash the reviewed VKU chunk corpus and embedding settings."""
    corpus_path = REAL_VKU_FULL_CORPUS if corpus_type == "full" else REAL_VKU_CORPUS
    if not corpus_path.exists():
        if corpus_type == "full" and REAL_VKU_CORPUS.exists():
            corpus_path = REAL_VKU_CORPUS
        else:
            raise FileNotFoundError(f"Không tìm thấy corpus QĐ1416: {corpus_path}")
    digest = hashlib.sha256()
    with corpus_path.open("rb") as corpus_file:
        for block in iter(lambda: corpus_file.read(1024 * 1024), b""):
            digest.update(block)
    digest.update(EMBEDDING_MODEL.encode("utf-8"))
    digest.update(corpus_type.encode("utf-8"))
    return digest.hexdigest()


def get_real_vku_vectorstore(fingerprint: str | None = None, embeddings=None, corpus_type: str = "demo") -> FAISS:
    """Load/build a separate FAISS index from the page-tagged QD1416 chunks."""
    fingerprint = fingerprint or get_real_vku_fingerprint(corpus_type)
    sub_dir = "real_vku_qd1416_full" if corpus_type == "full" else "real_vku_qd1416"
    index_dir = INDEX_DIR / sub_dir
    manifest_path = index_dir / "manifest.json"
    faiss_path = index_dir / "index.faiss"
    pickle_path = index_dir / "index.pkl"
    embeddings = embeddings or get_embeddings()

    corpus_path = REAL_VKU_FULL_CORPUS if corpus_type == "full" and REAL_VKU_FULL_CORPUS.exists() else REAL_VKU_CORPUS

    if manifest_path.exists() and faiss_path.exists() and pickle_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("fingerprint") == fingerprint:
                vectorstore = FAISS.load_local(
                    str(index_dir),
                    embeddings,
                    allow_dangerous_deserialization=True,
                )
                return vectorstore
        except Exception:
            # A missing or invalid local index is rebuilt from the JSONL source.
            pass

    rows = [
        json.loads(line)
        for line in corpus_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not rows:
        raise ValueError(f"Corpus QĐ1416 đang rỗng: {corpus_path}")

    from langchain_core.documents import Document

    docs = [
        Document(
            page_content=row["text"],
            metadata={key: value for key, value in row.items() if key != "text"},
        )
        for row in rows
    ]
    vectorstore = FAISS.from_documents(docs, embeddings)
    index_dir.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(index_dir))
    manifest_path.write_text(
        json.dumps({"fingerprint": fingerprint}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return vectorstore


def get_real_vku_retriever(fingerprint: str | None = None, corpus_type: str = "demo"):
    """Return the hybrid top-5 retriever over reviewed QD1416 chunks."""
    vectorstore = get_real_vku_vectorstore(fingerprint, corpus_type=corpus_type)
    return RealVKUHybridRetriever(vectorstore, k=5)



_VIETNAMESE_STOPWORDS = {
    "và", "là", "của", "cho", "các", "những", "nào", "này", "được", "với",
    "trong", "theo", "tại", "đến", "thì", "khi", "nếu", "một", "có", "về",
    "ra", "từ", "đó", "như", "để", "hoặc", "bao", "nhiêu", "gì", "nào",
}


def _terms(text: str) -> list[str]:
    return [
        term for term in re.findall(r"\w+", text.casefold(), flags=re.UNICODE)
        if len(term) > 1 and term not in _VIETNAMESE_STOPWORDS
    ]


def search_real_vku(question: str, vectorstore: FAISS, k: int = 5):
    """Fuse semantic FAISS ranking with BM25-style lexical ranking."""
    docs = list(vectorstore.docstore._dict.values())
    if not docs:
        return []

    dense_ranked = vectorstore.similarity_search(question, k=len(docs))
    query_terms = _terms(question)
    tokenized_docs = [_terms(doc.page_content) for doc in docs]
    doc_count = len(docs)
    average_length = sum(map(len, tokenized_docs)) / max(doc_count, 1)
    document_frequency = {}
    for terms in tokenized_docs:
        for term in set(terms):
            document_frequency[term] = document_frequency.get(term, 0) + 1

    lexical_scores = []
    for doc, terms in zip(docs, tokenized_docs):
        term_counts = {}
        for term in terms:
            term_counts[term] = term_counts.get(term, 0) + 1
        score = 0.0
        for term in query_terms:
            frequency = term_counts.get(term, 0)
            if not frequency:
                continue
            df = document_frequency[term]
            inverse_frequency = math.log1p(
                (doc_count - df + 0.5) / (df + 0.5)
            )
            denominator = frequency + 1.5 * (
                1 - 0.75 + 0.75 * len(terms) / max(average_length, 1)
            )
            score += inverse_frequency * frequency * 2.5 / denominator
        lexical_scores.append((score, doc))

    lexical_ranked = [doc for score, doc in sorted(lexical_scores, key=lambda item: item[0], reverse=True)]
    fused_scores = {}
    for ranking in (dense_ranked, lexical_ranked):
        for rank, doc in enumerate(ranking, start=1):
            doc_id = doc.metadata.get("doc_id", id(doc))
            fused_scores[doc_id] = fused_scores.get(doc_id, 0.0) + 1.0 / (60 + rank)
    by_id = {doc.metadata.get("doc_id", id(doc)): doc for doc in docs}
    ordered_ids = sorted(fused_scores, key=fused_scores.get, reverse=True)
    return [by_id[doc_id] for doc_id in ordered_ids[:k]]


class RealVKUHybridRetriever:
    """Small invoke-compatible retriever used by the Streamlit chat UI."""

    def __init__(self, vectorstore: FAISS, k: int = 5):
        self.vectorstore = vectorstore
        self.k = k

    def invoke(self, question: str):
        return search_real_vku(question, self.vectorstore, self.k)


def format_docs(docs) -> str:
    """Include source filename and page so answers can be checked."""
    sections = []
    for doc in docs:
        source = Path(doc.metadata.get("source", "Tài liệu không rõ tên")).name
        pages = doc.metadata.get("pages")
        page_number = doc.metadata.get("page_number")
        page = doc.metadata.get("page")
        if isinstance(pages, list) and pages:
            page_label = f", trang {pages[0]}–{pages[-1]}"
        elif isinstance(page_number, int):
            page_label = f", trang {page_number}"
        else:
            page_label = f", trang {page + 1}" if isinstance(page, int) else ""
        sections.append(f"[Nguồn: {source}{page_label}]\n{doc.page_content}")
    return "\n\n".join(sections)


def get_api_key() -> str:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "Chưa cấu hình GOOGLE_API_KEY. Hãy đặt biến môi trường này rồi chạy lại ứng dụng."
        )
    return api_key


def make_source_list(docs) -> list[str]:
    sources = []
    for doc in docs:
        name = Path(doc.metadata.get("source", "Tài liệu không rõ tên")).name
        pages = doc.metadata.get("pages")
        page_number = doc.metadata.get("page_number")
        page = doc.metadata.get("page")
        if isinstance(pages, list) and pages:
            label = f"{name}, trang {pages[0]}–{pages[-1]}"
        elif isinstance(page_number, int):
            label = f"{name}, trang {page_number}"
        else:
            label = f"{name}, trang {page + 1}" if isinstance(page, int) else name
        if label not in sources:
            sources.append(label)
    return sources
