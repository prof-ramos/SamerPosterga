"""
Serviço de embeddings usando OpenAI
"""
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from ..config import Config
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