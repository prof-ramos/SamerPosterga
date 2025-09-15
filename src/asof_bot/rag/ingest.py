"""
Processamento e indexação de documentos para o RAG
"""
import os
import hashlib
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    Docx2txtLoader
)
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from ..config import Config
from .embeddings import EmbeddingService

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processa e indexa documentos para o RAG"""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", "Art.", "§", ".", " "],
            length_function=len,
        )

        # Criar diretórios se não existirem
        Config.create_directories()

    def load_document(self, file_path: Path) -> List[Document]:
        """Carrega documento baseado na extensão"""
        ext = file_path.suffix.lower()

        try:
            if ext == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif ext == '.txt':
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif ext == '.md':
                loader = UnstructuredMarkdownLoader(str(file_path))
            elif ext in ['.docx', '.doc']:
                loader = Docx2txtLoader(str(file_path))
            else:
                logger.warning(f"Tipo de arquivo não suportado: {ext}")
                return []

            documents = loader.load()
            logger.info(f"Carregado: {file_path.name} ({len(documents)} páginas/seções)")
            return documents

        except Exception as e:
            logger.error(f"Erro ao carregar {file_path}: {e}")
            return []

    def enrich_metadata(self, doc: Document, file_path: Path) -> Document:
        """Adiciona metadados aos documentos"""
        doc.metadata.update({
            "source": file_path.name,
            "tipo_documento": self.identificar_tipo_documento(doc.page_content),
            "data_indexacao": datetime.now().isoformat(),
            "hash_documento": hashlib.md5(doc.page_content.encode()).hexdigest()[:8],
            "caminho_completo": str(file_path)
        })

        # Detectar contexto ASOF/Serviço Exterior
        if self.is_documento_servico_exterior(doc.page_content):
            doc.metadata["contexto"] = "servico_exterior"

        return doc

    def identificar_tipo_documento(self, content: str) -> str:
        """Identifica o tipo de documento jurídico"""
        content_lower = content.lower()

        if "lei" in content_lower and "art." in content_lower:
            return "lei"
        elif "decreto" in content_lower:
            return "decreto"
        elif "portaria" in content_lower:
            return "portaria"
        elif "resolução" in content_lower:
            return "resolucao"
        elif "instrução normativa" in content_lower:
            return "instrucao_normativa"
        elif "oficial de chancelaria" in content_lower or "serviço exterior" in content_lower:
            return "documento_servico_exterior"
        else:
            return "documento_geral"

    def is_documento_servico_exterior(self, content: str) -> bool:
        """Verifica se é documento relacionado ao Serviço Exterior"""
        termos = [
            "oficial de chancelaria",
            "serviço exterior brasileiro",
            "MRE", "Itamaraty",
            "ASOF"
        ]
        content_lower = content.lower()
        return any(termo.lower() in content_lower for termo in termos)

    def process_all_documents(self) -> List[Document]:
        """Processa todos os documentos do diretório"""
        all_documents = []

        if not Config.DOCUMENTS_DIR.exists():
            logger.warning(f"Diretório {Config.DOCUMENTS_DIR} não existe")
            return all_documents

        # Extensões suportadas
        extensions = ['.pdf', '.txt', '.md', '.docx', '.doc']
        files = [f for f in Config.DOCUMENTS_DIR.iterdir()
                if f.is_file() and f.suffix.lower() in extensions]

        logger.info(f"Encontrados {len(files)} documentos para processar")

        for file_path in files:
            docs = self.load_document(file_path)

            # Enriquecer metadados
            docs = [self.enrich_metadata(doc, file_path) for doc in docs]

            # Dividir em chunks
            chunks = self.text_splitter.split_documents(docs)

            # Adicionar índice do chunk aos metadados
            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_index"] = i
                chunk.metadata["total_chunks"] = len(chunks)

            all_documents.extend(chunks)

        logger.info(f"Total de chunks criados: {len(all_documents)}")
        return all_documents

    def create_vectorstore(self, documents: List[Document] = None) -> Chroma:
        """Cria ou atualiza o vectorstore"""
        if documents is None:
            documents = self.process_all_documents()

        if not documents:
            logger.warning("Nenhum documento para indexar")
            return None

        # Criar/atualizar Chroma DB
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_service.get_langchain_embeddings(),
            persist_directory=str(Config.CHROMA_DIR),
            collection_metadata={"hnsw:space": "cosine"}
        )

        vectorstore.persist()
        logger.info(f"Vectorstore criado/atualizado com {len(documents)} chunks")

        return vectorstore