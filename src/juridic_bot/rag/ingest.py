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
from langchain_chroma import Chroma
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
        # Identificar área do direito baseada no caminho do arquivo
        area_direito = self.identificar_area_direito(file_path)

        doc.metadata.update({
            "source": file_path.name,
            "tipo_documento": self.identificar_tipo_documento(doc.page_content),
            "area_direito": area_direito,
            "data_indexacao": datetime.now().isoformat(),
            "hash_documento": hashlib.md5(doc.page_content.encode()).hexdigest()[:8],
            "caminho_completo": str(file_path)
        })

        return doc

    def identificar_area_direito(self, file_path: Path) -> str:
        """Identifica a área do direito baseada no caminho do arquivo"""
        path_parts = file_path.parts

        # Procurar por pastas de área do direito
        areas_conhecidas = [
            "direito_administrativo", "direito_constitucional", "direito_penal",
            "direito_civil", "direito_processual", "direito_tributario",
            "direito_trabalhista", "direito_previdenciario", "direito_eleitoral",
            "direito_internacional", "direito_ambiental", "direito_consumidor"
        ]

        for part in path_parts:
            for area in areas_conhecidas:
                if area in part.lower():
                    return area.replace("direito_", "").replace("_", " ").title()

        return "Direito Geral"

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
        elif "súmula" in content_lower:
            return "sumula"
        elif "jurisprudência" in content_lower or "julgado" in content_lower:
            return "jurisprudencia"
        elif "doutrina" in content_lower:
            return "doutrina"
        else:
            return "documento_geral"

    def get_processed_files_hash(self) -> set:
        """Retorna um set com os hashes dos arquivos já processados"""
        processed_hashes = set()

        # Verificar se existe vectorstore
        if not Config.CHROMA_DIR.exists():
            return processed_hashes

        try:
            # Tentar carregar o vectorstore existente
            vectorstore = Chroma(
                persist_directory=str(Config.CHROMA_DIR),
                embedding_function=self.embedding_service.get_langchain_embeddings()
            )

            # Obter todos os documentos e seus metadados
            results = vectorstore.get()
            for metadata in results['metadatas']:
                if metadata and 'hash_documento' in metadata:
                    processed_hashes.add(metadata['hash_documento'])

        except Exception as e:
            logger.warning(f"Erro ao carregar vectorstore existente: {e}")

        return processed_hashes

    def process_all_documents(self) -> List[Document]:
        """Processa todos os documentos do diretório, pulando os já processados"""
        all_documents = []

        if not Config.DOCUMENTS_DIR.exists():
            logger.warning(f"Diretório {Config.DOCUMENTS_DIR} não existe")
            return all_documents

        # Obter hashes dos arquivos já processados
        processed_hashes = self.get_processed_files_hash()

        # Extensões suportadas
        extensions = ['.pdf', '.txt', '.md', '.docx', '.doc']

        # Coletar todos os arquivos recursivamente (incluindo subpastas)
        all_files = []
        for ext in extensions:
            all_files.extend(list(Config.DOCUMENTS_DIR.rglob(f'*{ext}')))

        logger.info(f"Encontrados {len(all_files)} documentos no diretório")

        # Filtrar arquivos não processados
        new_files = []
        for file_path in all_files:
            # Calcular hash do arquivo baseado no caminho e tamanho
            file_hash = hashlib.md5(f"{file_path}:{file_path.stat().st_size}".encode()).hexdigest()[:8]

            if file_hash not in processed_hashes:
                new_files.append((file_path, file_hash))
            else:
                logger.info(f"Pulando arquivo já processado: {file_path.name}")

        logger.info(f"{len(new_files)} arquivos novos para processar")

        for file_path, file_hash in new_files:
            docs = self.load_document(file_path)

            # Enriquecer metadados
            docs = [self.enrich_metadata(doc, file_path) for doc in docs]

            # Adicionar hash do arquivo aos metadados
            for doc in docs:
                doc.metadata["file_hash"] = file_hash

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