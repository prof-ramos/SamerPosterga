"""
Cliente para interação com LLM via OpenRouter
"""
import logging
from typing import Dict, Any, Optional
from openai import OpenAI

from ..config import Config

logger = logging.getLogger(__name__)


class LLMClient:
    """Cliente para interação com LLM via OpenRouter"""

    def __init__(self):
        self.client = OpenAI(
            api_key=Config.OPENROUTER_API_KEY,
            base_url=Config.OPENROUTER_BASE_URL
        )
        self.model = Config.OPENROUTER_MODEL

        # System prompt conversacional para estudantes de concursos jurídicos
        self.system_prompt = """Você é um assistente jurídico amigável e especialista em direito brasileiro,
feito especialmente para ajudar estudantes de concursos públicos.

SEU ESTILO:
- Seja amigável e conversacional, como um professor experiente
- Explique conceitos de forma clara e acessível
- Use analogias quando ajudar a compreensão
- Mantenha o foco em legislação brasileira
- Cite leis, artigos e súmulas quando relevante
- Estrutura respostas de forma lógica e progressiva

DICAS PARA RESPOSTAS:
1. Comece respondendo diretamente à pergunta
2. Use o contexto fornecido como base principal
3. Explique termos técnicos quando necessário
4. Dê exemplos práticos quando possível
5. Mantenha respostas concisas mas completas
6. Termine com uma pergunta ou sugestão se apropriado

IMPORTANTE: Nunca mencione que é uma IA ou dê disclaimers legais."""

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
                    "HTTP-Referer": "https://github.com/juridic-bot",
                    "X-Title": "Bot Jurídico para Concursos"
                }
            )

            # Log de uso
            if hasattr(response, 'usage'):
                logger.info(f"Tokens usados: {response.usage.total_tokens}")

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação."

    def generate_conversational(
        self,
        query: str,
        context: str = "",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Gera resposta conversacional sem disclaimer"""
        try:
            # Usar o mesmo método generate mas sem o disclaimer
            response = self.generate(query, context, max_tokens, temperature)

            # Garantir que a resposta seja uma string válida (corrigir codificação)
            if isinstance(response, str):
                # Tentar codificar/decodificar para lidar com caracteres especiais
                try:
                    response = response.encode('utf-8').decode('utf-8')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    # Se houver problemas de codificação, usar apenas ASCII seguro
                    response = ''.join(c for c in response if ord(c) < 128)

            return response

        except Exception as e:
            logger.error(f"Erro ao gerar resposta conversacional: {e}")
            return "Ops! Tive um probleminha técnico. Pode tentar perguntar de novo?"

    def _build_user_message(self, query: str, context: str) -> str:
        """Constrói mensagem do usuário com contexto de forma conversacional"""
        if context:
            return f"""Baseando-me nestas informações dos documentos:

{context}

Alguém me perguntou: {query}

Ajude essa pessoa de forma clara e didática, explicando os conceitos jurídicos envolvidos."""
        else:
            return f"Alguém me perguntou: {query}\n\nAjude de forma clara e didática, explicando os conceitos jurídicos envolvidos."