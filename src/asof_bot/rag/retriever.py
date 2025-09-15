"""
Sistema de recuperação de documentos
"""
import logging
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from ..config import Config
from .embeddings import EmbeddingService

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Sistema de recuperação de documentos"""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vectorstore = self.load_vectorstore()

    def load_vectorstore(self) -> Chroma:
        """Carrega o vectorstore existente"""
        try:
            vectorstore = Chroma(
                persist_directory=str(Config.CHROMA_DIR),
                embedding_function=self.embedding_service.get_langchain_embeddings()
            )
            logger.info("Vectorstore carregado com sucesso")
            return vectorstore
        except Exception as e:
            logger.error(f"Erro ao carregar vectorstore: {e}")
            return None

    def search(self, query: str, k: int = None) -> List[Document]:
        """Busca documentos similares"""
        if not self.vectorstore:
            logger.error("Vectorstore não está disponível")
            return []

        k = k or Config.TOP_K

        try:
            # Busca com score
            results_with_scores = self.vectorstore.similarity_search_with_score(query, k=k)

            # Log dos resultados
            for doc, score in results_with_scores:
                logger.debug(".4f")

            # Retornar apenas documentos (sem scores)
            return [doc for doc, _ in results_with_scores]

        except Exception as e:
            logger.error(f"Erro na busca: {e}")
            return []

    def format_context(self, documents: List[Document]) -> str:
        """Formata documentos para contexto do LLM"""
        if not documents:
            return ""

        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', 'Desconhecido')
            tipo = doc.metadata.get('tipo_documento', 'documento')
            chunk_info = "[Chunk {}/{}]".format(
                doc.metadata.get('chunk_index', '?'),
                doc.metadata.get('total_chunks', '?')
            )

            context_parts.append(
                "**Documento {}** - {} ({}) {}\n"
                "{}\n"
                "---".format(i, source, tipo, chunk_info, doc.page_content)
            )

        return "\n\n".join(context_parts)

    def reload(self):
        """Recarrega o vectorstore (útil após reindexação)"""
        self.vectorstore = self.load_vectorstore()
        logger.info("Vectorstore recarregado")