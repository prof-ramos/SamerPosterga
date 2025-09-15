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