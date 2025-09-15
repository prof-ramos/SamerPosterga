"""
Testes para o sistema RAG Retriever
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from langchain.schema import Document
from src.juridic_bot.rag.retriever import RAGRetriever


class TestRAGRetriever:
    """Testes da classe RAGRetriever"""

    @patch('src.juridic_bot.rag.retriever.EmbeddingService')
    @patch('src.juridic_bot.rag.retriever.Chroma')
    def test_retriever_initialization_success(self, mock_chroma, mock_embedding_service):
        """Testa inicialização bem-sucedida do retriever"""
        mock_vectorstore = Mock()
        mock_vectorstore._collection.count.return_value = 5
        mock_chroma.return_value = mock_vectorstore

        retriever = RAGRetriever()

        assert retriever.vectorstore is not None
        mock_chroma.assert_called_once()
        mock_embedding_service.assert_called_once()

    @patch('src.juridic_bot.rag.retriever.EmbeddingService')
    @patch('src.juridic_bot.rag.retriever.Chroma')
    def test_retriever_initialization_failure(self, mock_chroma, mock_embedding_service):
        """Testa falha na inicialização do retriever"""
        mock_chroma.side_effect = Exception("ChromaDB error")

        retriever = RAGRetriever()

        assert retriever.vectorstore is None

    @patch('src.juridic_bot.rag.retriever.EmbeddingService')
    @patch('src.juridic_bot.rag.retriever.Chroma')
    def test_search_with_vectorstore_available(self, mock_chroma, mock_embedding_service):
        """Testa busca com vectorstore disponível"""
        # Mock dos documentos retornados
        doc1 = Document(
            page_content="Devido processo legal é garantia fundamental...",
            metadata={"source": "cf_art5.pdf", "tipo_documento": "constituicao"}
        )
        doc2 = Document(
            page_content="O processo administrativo deve observar...",
            metadata={"source": "lei_9784.pdf", "tipo_documento": "lei"}
        )

        mock_vectorstore = Mock()
        mock_vectorstore.similarity_search_with_score.return_value = [
            (doc1, 0.85), (doc2, 0.78)
        ]
        mock_chroma.return_value = mock_vectorstore

        retriever = RAGRetriever()
        results = retriever.search("devido processo legal", k=2)

        assert len(results) == 2
        assert "garantia fundamental" in results[0].page_content
        assert results[0].metadata["source"] == "cf_art5.pdf"

    @patch('src.juridic_bot.rag.retriever.EmbeddingService')
    @patch('src.juridic_bot.rag.retriever.Chroma')
    def test_search_without_vectorstore(self, mock_chroma, mock_embedding_service):
        """Testa busca sem vectorstore disponível"""
        mock_chroma.side_effect = Exception("No vectorstore")

        retriever = RAGRetriever()
        results = retriever.search("test query")

        assert results == []

    @patch('src.juridic_bot.rag.retriever.EmbeddingService')
    @patch('src.juridic_bot.rag.retriever.Chroma')
    def test_search_with_error(self, mock_chroma, mock_embedding_service):
        """Testa busca com erro durante a operação"""
        mock_vectorstore = Mock()
        mock_vectorstore.similarity_search_with_score.side_effect = Exception("Search error")
        mock_chroma.return_value = mock_vectorstore

        retriever = RAGRetriever()
        results = retriever.search("test query")

        assert results == []

    def test_format_context_with_documents(self):
        """Testa formatação de contexto com documentos"""
        with patch('src.juridic_bot.rag.retriever.EmbeddingService'), \
             patch('src.juridic_bot.rag.retriever.Chroma'):

            retriever = RAGRetriever()

            docs = [
                Document(
                    page_content="Conteúdo do primeiro documento",
                    metadata={
                        "source": "doc1.pdf",
                        "tipo_documento": "lei",
                        "chunk_index": 1,
                        "total_chunks": 3
                    }
                ),
                Document(
                    page_content="Conteúdo do segundo documento",
                    metadata={
                        "source": "doc2.pdf",
                        "tipo_documento": "constituicao",
                        "chunk_index": 2,
                        "total_chunks": 5
                    }
                )
            ]

            context = retriever.format_context(docs)

            assert "Documento 1" in context
            assert "Documento 2" in context
            assert "doc1.pdf" in context
            assert "doc2.pdf" in context
            assert "Conteúdo do primeiro documento" in context
            assert "Conteúdo do segundo documento" in context
            assert "[Chunk 1/3]" in context
            assert "[Chunk 2/5]" in context

    def test_format_context_empty_documents(self):
        """Testa formatação de contexto sem documentos"""
        with patch('src.juridic_bot.rag.retriever.EmbeddingService'), \
             patch('src.juridic_bot.rag.retriever.Chroma'):

            retriever = RAGRetriever()
            context = retriever.format_context([])

            assert context == ""

    @patch('src.juridic_bot.rag.retriever.EmbeddingService')
    @patch('src.juridic_bot.rag.retriever.Chroma')
    def test_reload_vectorstore(self, mock_chroma, mock_embedding_service):
        """Testa recarregamento do vectorstore"""
        # Primeira chamada - inicialização
        mock_vectorstore1 = Mock()
        # Segunda chamada - reload
        mock_vectorstore2 = Mock()
        mock_chroma.side_effect = [mock_vectorstore1, mock_vectorstore2]

        retriever = RAGRetriever()
        assert retriever.vectorstore == mock_vectorstore1

        retriever.reload()
        assert retriever.vectorstore == mock_vectorstore2
        assert mock_chroma.call_count == 2

    def test_format_context_with_missing_metadata(self):
        """Testa formatação com metadados faltando"""
        with patch('src.juridic_bot.rag.retriever.EmbeddingService'), \
             patch('src.juridic_bot.rag.retriever.Chroma'):

            retriever = RAGRetriever()

            docs = [
                Document(
                    page_content="Documento sem metadados completos",
                    metadata={}  # Metadados vazios
                )
            ]

            context = retriever.format_context(docs)

            assert "Documento 1" in context
            assert "Desconhecido" in context  # source padrão
            assert "documento" in context  # tipo_documento padrão
            assert "[Chunk ?/?]" in context  # chunk info padrão