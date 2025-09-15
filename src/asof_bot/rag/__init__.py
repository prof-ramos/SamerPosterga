"""
Módulo RAG (Retrieval-Augmented Generation)
Sistema de busca e indexação de documentos
"""

from .embeddings import EmbeddingService
from .ingest import DocumentProcessor
from .retriever import RAGRetriever

__all__ = ['EmbeddingService', 'DocumentProcessor', 'RAGRetriever']