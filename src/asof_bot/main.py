"""
Ponto de entrada principal do Bot Jurídico para Concursos
"""
import asyncio
import logging

from .config import Config
from .rag.ingest import DocumentProcessor
from .bot.bot import bot

logger = logging.getLogger(__name__)


async def main():
    """Função principal"""
    try:
        # Validar configuração
        Config.validate()

        # Verificar se há documentos indexados
        if not Config.CHROMA_DIR.exists():
            logger.warning("Vectorstore não existe. Execute 'python -m src.asof_bot.main' primeiro!")
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