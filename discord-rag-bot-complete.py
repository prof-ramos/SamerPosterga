"""
Discord Bot com RAG (Retrieval-Augmented Generation)
Sistema completo com OpenAI embeddings e OpenRouter para geração
Autor: Gabriel Ramos - ASOF
"""

# ========================
# requirements.txt
# ========================
"""
discord.py>=2.3.0
python-dotenv>=1.0.0
openai>=1.0.0
chromadb>=0.4.0
langchain>=0.1.0
langchain-community>=0.0.10
langchain-openai>=0.0.5
pypdf>=3.17.0
python-docx>=1.0.0
tiktoken>=0.5.0
psutil>=5.9.0
aiofiles>=23.0.0
"""

# ========================
# .env.example
# ========================
"""
# Discord Config
DISCORD_TOKEN=seu_token_aqui
DISCORD_APP_ID=seu_app_id_aqui
DISCORD_GUILD_ID=opcional_guild_id
DISCORD_OWNER_ID=seu_user_id_para_comandos_admin

# OpenRouter Config
OPENROUTER_API_KEY=seu_openrouter_key
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# OpenAI Config (para embeddings)
OPENAI_API_KEY=sua_openai_key
EMBEDDING_MODEL=text-embedding-3-small

# RAG Config
TOP_K=5
CHUNK_SIZE=1500
CHUNK_OVERLAP=200

# System Config
MAX_TOKENS=2000
TEMPERATURE=0.7
LOG_LEVEL=INFO
"""

# ========================
# config.py
# ========================
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Discord
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DISCORD_APP_ID = os.getenv("DISCORD_APP_ID")
    DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")
    DISCORD_OWNER_ID = int(os.getenv("DISCORD_OWNER_ID", "0"))
    
    # OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # RAG
    TOP_K = int(os.getenv("TOP_K", "5"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Paths
    BASE_DIR = Path(__file__).parent
    DOCUMENTS_DIR = BASE_DIR / "RRAG"
    CHROMA_DIR = BASE_DIR / ".chroma"
    
    # System
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        """Valida configurações essenciais"""
        required = [
            "DISCORD_TOKEN",
            "OPENROUTER_API_KEY", 
            "OPENAI_API_KEY"
        ]
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Variáveis de ambiente faltando: {', '.join(missing)}")

# ========================
# rag/embeddings.py
# ========================
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from config import Config
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Serviço de embeddings usando OpenAI"""
    
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.EMBEDDING_MODEL
        
        # Para LangChain
        self.langchain_embeddings = OpenAIEmbeddings(
            openai_api_key=Config.OPENAI_API_KEY,
            model=self.model
        )
        
        logger.info(f"Serviço de embeddings inicializado com modelo: {self.model}")
    
    def get_embeddings(self, texts):
        """Gera embeddings para uma lista de textos"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Erro ao gerar embeddings: {e}")
            raise
    
    def get_langchain_embeddings(self):
        """Retorna objeto de embeddings para uso com LangChain"""
        return self.langchain_embeddings

# ========================
# rag/ingest.py
# ========================
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

from config import Config
from rag.embeddings import EmbeddingService

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
        Config.DOCUMENTS_DIR.mkdir(exist_ok=True)
        Config.CHROMA_DIR.mkdir(exist_ok=True)
    
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

# ========================
# rag/retriever.py
# ========================
import logging
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from config import Config
from rag.embeddings import EmbeddingService

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
                logger.debug(f"Score: {score:.4f} | Fonte: {doc.metadata.get('source', 'N/A')}")
            
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
            chunk_info = f"[Chunk {doc.metadata.get('chunk_index', '?')}/{doc.metadata.get('total_chunks', '?')}]"
            
            context_parts.append(
                f"**Documento {i}** - {source} ({tipo}) {chunk_info}\n"
                f"{doc.page_content}\n"
                f"---"
            )
        
        return "\n\n".join(context_parts)
    
    def reload(self):
        """Recarrega o vectorstore (útil após reindexação)"""
        self.vectorstore = self.load_vectorstore()
        logger.info("Vectorstore recarregado")

# ========================
# llm/client.py
# ========================
import logging
from typing import Dict, Any, Optional
from openai import OpenAI

from config import Config

logger = logging.getLogger(__name__)

class LLMClient:
    """Cliente para interação com LLM via OpenRouter"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.OPENROUTER_API_KEY,
            base_url=Config.OPENROUTER_BASE_URL
        )
        self.model = Config.OPENROUTER_MODEL
        
        # System prompt para contexto jurídico/administrativo
        self.system_prompt = """Você é um assistente especializado em questões jurídicas e administrativas do Brasil, 
com foco especial no Serviço Exterior Brasileiro e trabalho de Oficiais de Chancelaria.

IMPORTANTE: 
- Os Oficiais de Chancelaria NÃO fazem parte da Diplomacia, mas sim do Serviço Exterior Brasileiro.
- Sempre use "Serviço Exterior Brasileiro" em vez de "Diplomacia" ao se referir ao trabalho dos Oficiais de Chancelaria.
- Seja preciso com termos técnicos e legislação brasileira.
- Cite as fontes dos documentos quando disponível.
- Mantenha um tom profissional mas acessível.

Quando responder:
1. Baseie-se nos documentos fornecidos como contexto
2. Cite artigos, leis e normativas quando relevante
3. Se não tiver certeza, indique claramente
4. Forneça respostas estruturadas e claras"""
        
        logger.info(f"LLM Client inicializado com modelo: {self.model}")
    
    def generate(
        self,
        query: str,
        context: str = "",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Gera resposta usando o LLM"""
        
        # Montar mensagem com contexto
        user_message = self._build_user_message(query, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_tokens or Config.MAX_TOKENS,
                temperature=temperature or Config.TEMPERATURE,
                # Headers recomendados pelo OpenRouter
                extra_headers={
                    "HTTP-Referer": "https://github.com/asof-brasil",
                    "X-Title": "ASOF Bot Jurídico"
                }
            )
            
            # Log de uso
            if hasattr(response, 'usage'):
                logger.info(f"Tokens usados: {response.usage.total_tokens}")
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação."
    
    def _build_user_message(self, query: str, context: str) -> str:
        """Constrói mensagem do usuário com contexto"""
        if context:
            return f"""Com base nos seguintes documentos:

{context}

Pergunta: {query}

Por favor, responda com base nos documentos fornecidos. Se a informação não estiver nos documentos, indique claramente."""
        else:
            return query
    
    def add_disclaimer(self, response: str) -> str:
        """Adiciona disclaimer legal às respostas"""
        disclaimer = "\n\n*⚖️ Nota: Esta é uma resposta gerada por IA com base em documentos disponíveis. Para questões legais específicas, consulte sempre um profissional qualificado.*"
        return response + disclaimer

# ========================
# bot.py - ARQUIVO PRINCIPAL
# ========================
import asyncio
import logging
from datetime import datetime
import discord
from discord.ext import commands
import psutil

from config import Config
from rag.ingest import DocumentProcessor
from rag.retriever import RAGRetriever
from llm.client import LLMClient

# Configurar logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JuridicBot(commands.Bot):
    """Bot Discord com capacidades RAG"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            application_id=Config.DISCORD_APP_ID
        )
        
        self.retriever = RAGRetriever()
        self.llm_client = LLMClient()
        self.start_time = datetime.now()
    
    async def setup_hook(self):
        """Configuração inicial do bot"""
        # Sincronizar comandos slash
        if Config.DISCORD_GUILD_ID:
            guild = discord.Object(id=int(Config.DISCORD_GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info(f"Comandos sincronizados para guild {Config.DISCORD_GUILD_ID}")
        else:
            await self.tree.sync()
            logger.info("Comandos globais sincronizados")
    
    async def on_ready(self):
        """Evento quando o bot está pronto"""
        logger.info(f'{self.user} está online!')
        logger.info(f'ID: {self.user.id}')
        logger.info(f'Servidores: {len(self.guilds)}')
        
        # Definir status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="questões jurídicas | @mention"
            )
        )
    
    async def on_message(self, message: discord.Message):
        """Processa mensagens"""
        # Ignorar mensagens do próprio bot
        if message.author == self.user:
            return
        
        # Verificar se o bot foi mencionado ou é DM
        if self.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            await self.handle_query(message)
        
        # Processar comandos normais
        await self.process_commands(message)
    
    async def handle_query(self, message: discord.Message):
        """Processa consultas ao RAG"""
        # Remover menção do bot da query
        query = message.content.replace(f'<@{self.user.id}>', '').strip()
        
        if not query:
            await message.reply("Por favor, faça uma pergunta após me mencionar!")
            return
        
        # Indicador de digitação
        async with message.channel.typing():
            try:
                # Buscar documentos relevantes
                documents = self.retriever.search(query)
                
                # Formatar contexto
                context = self.retriever.format_context(documents)
                
                # Gerar resposta
                response = self.llm_client.generate(query, context)
                
                # Adicionar disclaimer
                response = self.llm_client.add_disclaimer(response)
                
                # Adicionar fontes citadas
                if documents:
                    sources = list(set(doc.metadata.get('source', 'N/A') for doc in documents))
                    response += f"\n\n📚 **Fontes consultadas:** {', '.join(sources)}"
                
                # Enviar resposta (dividir se necessário)
                await self.send_long_message(message, response)
                
            except Exception as e:
                logger.error(f"Erro ao processar query: {e}")
                await message.reply("❌ Ocorreu um erro ao processar sua pergunta. Por favor, tente novamente.")
    
    async def send_long_message(self, message: discord.Message, content: str):
        """Envia mensagens longas divididas em chunks"""
        MAX_LENGTH = 2000
        
        if len(content) <= MAX_LENGTH:
            await message.reply(content)
            return
        
        # Dividir mensagem
        chunks = []
        current_chunk = ""
        
        for line in content.split('\n'):
            if len(current_chunk) + len(line) + 1 > MAX_LENGTH:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += '\n' + line if current_chunk else line
        
        if current_chunk:
            chunks.append(current_chunk)
        
        # Enviar chunks
        for i, chunk in enumerate(chunks):
            if i == 0:
                await message.reply(chunk)
            else:
                await message.channel.send(chunk)

# Instanciar bot
bot = JuridicBot()

# ========================
# COMANDOS SLASH
# ========================

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    """Verifica a latência do bot"""
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! Latência: {latency}ms")

@bot.tree.command(name="status")
async def status(interaction: discord.Interaction):
    """Mostra status do sistema"""
    # Informações do sistema
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    uptime = datetime.now() - bot.start_time
    
    embed = discord.Embed(
        title="📊 Status do Sistema",
        color=discord.Color.green()
    )
    embed.add_field(name="CPU", value=f"{cpu}%", inline=True)
    embed.add_field(name="RAM", value=f"{ram}%", inline=True)
    embed.add_field(name="Uptime", value=str(uptime).split('.')[0], inline=True)
    embed.add_field(name="Modelo LLM", value=Config.OPENROUTER_MODEL, inline=False)
    embed.add_field(name="Modelo Embeddings", value=Config.EMBEDDING_MODEL, inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reindex")
@commands.is_owner()
async def reindex(interaction: discord.Interaction):
    """Reindexa todos os documentos (apenas owner)"""
    if interaction.user.id != Config.DISCORD_OWNER_ID:
        await interaction.response.send_message("❌ Você não tem permissão para usar este comando.", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    try:
        processor = DocumentProcessor()
        vectorstore = processor.create_vectorstore()
        
        if vectorstore:
            bot.retriever.reload()
            await interaction.followup.send("✅ Documentos reindexados com sucesso!")
        else:
            await interaction.followup.send("⚠️ Nenhum documento foi indexado.")
            
    except Exception as e:
        logger.error(f"Erro ao reindexar: {e}")
        await interaction.followup.send(f"❌ Erro ao reindexar: {str(e)}")

@bot.tree.command(name="buscar_lei")
async def buscar_lei(interaction: discord.Interaction, numero: str, ano: str = None):
    """Busca uma lei específica"""
    await interaction.response.defer()
    
    query = f"Lei {numero}"
    if ano:
        query += f"/{ano}"
    
    try:
        documents = bot.retriever.search(query, k=3)
        
        if documents:
            context = bot.retriever.format_context(documents)
            response = f"📖 **Resultados para {query}:**\n\n{context[:1500]}..."
        else:
            response = f"❌ Não encontrei documentos sobre {query}"
        
        await interaction.followup.send(response)
        
    except Exception as e:
        logger.error(f"Erro na busca: {e}")
        await interaction.followup.send("❌ Erro ao buscar lei.")

@bot.tree.command(name="ajuda")
async def ajuda(interaction: discord.Interaction):
    """Mostra informações de ajuda"""
    embed = discord.Embed(
        title="🤖 Bot Jurídico ASOF - Ajuda",
        description="Assistente especializado em questões jurídicas e administrativas",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Como usar",
        value="• Me mencione (@bot) seguido de sua pergunta\n• Envie DM diretamente\n• Use os comandos slash disponíveis",
        inline=False
    )
    
    embed.add_field(
        name="Comandos",
        value="`/ping` - Verifica latência\n`/status` - Status do sistema\n`/buscar_lei` - Busca lei específica\n`/ajuda` - Este menu",
        inline=False
    )
    
    embed.add_field(
        name="Especialidades",
        value="• Serviço Exterior Brasileiro\n• Legislação administrativa\n• Normativas MRE/ASOF",
        inline=False
    )
    
    embed.set_footer(text="ASOF - Associação Nacional dos Oficiais de Chancelaria")
    
    await interaction.response.send_message(embed=embed)

# ========================
# MAIN
# ========================

async def main():
    """Função principal"""
    try:
        # Validar configuração
        Config.validate()
        
        # Verificar se há documentos indexados
        if not Config.CHROMA_DIR.exists():
            logger.warning("Vectorstore não existe. Execute 'python -m rag.ingest' primeiro!")
            processor = DocumentProcessor()
            processor.create_vectorstore()
        
        # Iniciar bot
        await bot.start(Config.DISCORD_TOKEN)
        
    except KeyboardInterrupt:
        logger.info("Encerrando bot...")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())

# ========================
# docker-compose.yml
# ========================
"""
version: '3.8'

services:
  bot:
    build: .
    container_name: asof-juridic-bot
    env_file: .env
    volumes:
      - ./RRAG:/app/RRAG
      - ./chroma_data:/app/.chroma
      - ./logs:/app/logs
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
    healthcheck:
      test: ["CMD", "python", "-c", "import psutil; exit(0 if psutil.cpu_percent() < 90 else 1)"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  chroma_data:
  logs:
"""

# ========================
# Dockerfile
# ========================
"""
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Comando para executar
CMD ["python", "discord-rag-bot-complete.py"]
"""