"""
Testes para o cliente LLM
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.juridic_bot.llm.client import LLMClient


class TestLLMClient:
    """Testes da classe LLMClient"""

    @patch('src.juridic_bot.llm.client.OpenAI')
    def test_llm_client_initialization(self, mock_openai):
        """Testa inicialização do cliente LLM"""
        client = LLMClient()

        assert client.model == "deepseek/deepseek-chat-v3-0324"
        assert "jurídico amigável" in client.system_prompt
        mock_openai.assert_called_once()

    @patch('src.juridic_bot.llm.client.OpenAI')
    @patch('src.juridic_bot.config.Config.SYSTEM_PROMPT', "Prompt personalizado de teste")
    def test_llm_client_custom_system_prompt(self, mock_openai):
        """Testa uso de prompt personalizado via SYSTEM_PROMPT"""
        client = LLMClient()

        assert client.system_prompt == "Prompt personalizado de teste"
        mock_openai.assert_called_once()

    @patch('src.juridic_bot.llm.client.OpenAI')
    def test_generate_response_success(self, mock_openai):
        """Testa geração de resposta bem-sucedida"""
        # Mock da resposta da API
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Devido processo legal é..."
        mock_response.usage.total_tokens = 150

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = LLMClient()
        result = client.generate("O que é devido processo legal?")

        assert "Devido processo legal" in result
        mock_client.chat.completions.create.assert_called_once()

    @patch('src.juridic_bot.llm.client.OpenAI')
    def test_generate_with_context(self, mock_openai):
        """Testa geração com contexto RAG"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Baseado nos documentos..."
        mock_response.usage.total_tokens = 200

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = LLMClient()
        context = "Constituição Federal Art. 5º..."
        result = client.generate("O que é devido processo legal?", context)

        assert "Baseado nos documentos" in result
        # Verificar se contexto foi incluído na mensagem
        call_args = mock_client.chat.completions.create.call_args
        user_message = call_args[1]['messages'][1]['content']
        assert context in user_message

    @patch('src.juridic_bot.llm.client.OpenAI')
    def test_generate_error_handling(self, mock_openai):
        """Testa tratamento de erro na geração"""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client

        client = LLMClient()
        result = client.generate("Test query")

        assert "erro ao processar" in result.lower()

    @patch('src.juridic_bot.llm.client.OpenAI')
    def test_generate_conversational(self, mock_openai):
        """Testa método de geração conversacional"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Olá! Devido processo legal..."
        mock_response.usage.total_tokens = 180

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = LLMClient()
        result = client.generate_conversational("O que é devido processo legal?")

        assert "Olá!" in result

    @patch('src.juridic_bot.llm.client.OpenAI')
    def test_utf8_encoding_handling(self, mock_openai):
        """Testa tratamento de codificação UTF-8"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Resposta com acentuação: ção, ã, é"
        mock_response.usage.total_tokens = 100

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = LLMClient()
        result = client.generate("Pergunta com acentuação")

        assert "acentuação" in result
        assert "ção" in result

    def test_build_user_message_with_context(self):
        """Testa construção de mensagem com contexto"""
        with patch('src.juridic_bot.llm.client.OpenAI'):
            client = LLMClient()

            query = "O que é habeas corpus?"
            context = "Art. 5º, LXVIII da CF..."

            message = client._build_user_message(query, context)

            assert query in message
            assert context in message
            assert "documentos" in message.lower()

    def test_build_user_message_without_context(self):
        """Testa construção de mensagem sem contexto"""
        with patch('src.juridic_bot.llm.client.OpenAI'):
            client = LLMClient()

            query = "O que é mandado de segurança?"
            message = client._build_user_message(query, "")

            assert query in message
            assert "documentos" not in message.lower()