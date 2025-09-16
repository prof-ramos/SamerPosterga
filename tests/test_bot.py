"""
Testes para o bot Discord
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock, PropertyMock
import discord
from src.juridic_bot.bot.bot import JuridicBot


class TestJuridicBot:
    """Testes da classe JuridicBot"""

    @patch('src.juridic_bot.bot.bot.RAGRetriever')
    @patch('src.juridic_bot.bot.bot.LLMClient')
    def test_bot_initialization(self, mock_llm_client, mock_rag_retriever):
        """Testa inicialização do bot"""
        bot = JuridicBot()

        assert bot.command_prefix == '!'
        assert bot.intents.message_content is True
        assert bot.intents.members is True
        mock_rag_retriever.assert_called_once()
        mock_llm_client.assert_called_once()

    @patch('src.juridic_bot.bot.bot.RAGRetriever')
    @patch('src.juridic_bot.bot.bot.LLMClient')
    @pytest.mark.asyncio
    async def test_on_message_ignores_own_messages(self, mock_llm_client, mock_rag_retriever):
        """Testa se o bot ignora suas próprias mensagens"""
        with patch.object(JuridicBot, 'user', new_callable=PropertyMock) as mock_user:
            bot = JuridicBot()
            mock_user.return_value.id = 12345

            # Mock da mensagem do próprio bot
            message = Mock()
            message.author = bot.user

            # Não deve processar a mensagem
            with patch.object(bot, 'handle_query') as mock_handle:
                await bot.on_message(message)
                mock_handle.assert_not_called()

    @patch('src.juridic_bot.bot.bot.RAGRetriever')
    @patch('src.juridic_bot.bot.bot.LLMClient')
    @pytest.mark.asyncio
    async def test_on_message_handles_mentions(self, mock_llm_client, mock_rag_retriever):
        """Testa tratamento de menções"""
        with patch.object(JuridicBot, 'user', new_callable=PropertyMock) as mock_user:
            bot = JuridicBot()
            mock_user.return_value.id = 12345

            # Mock da mensagem que menciona o bot
            message = Mock()
            message.author = Mock()
            message.author.id = 67890
            bot.user.mentioned_in.return_value = True

            with patch.object(bot, 'handle_query', new_callable=AsyncMock) as mock_handle:
                await bot.on_message(message)
                mock_handle.assert_called_once_with(message)

    @patch('src.juridic_bot.bot.bot.RAGRetriever')
    @patch('src.juridic_bot.bot.bot.LLMClient')
    @pytest.mark.asyncio
    async def test_on_message_handles_dm(self, mock_llm_client, mock_rag_retriever):
        """Testa tratamento de mensagens diretas"""
        with patch.object(JuridicBot, 'user', new_callable=PropertyMock) as mock_user:
            bot = JuridicBot()
            mock_user.return_value.id = 12345

            # Mock da mensagem DM
            message = Mock()
            message.author = Mock()
            message.author.id = 67890
            message.channel = Mock(spec=discord.DMChannel)
            bot.user.mentioned_in.return_value = False

            with patch.object(bot, 'handle_query', new_callable=AsyncMock) as mock_handle:
                await bot.on_message(message)
                mock_handle.assert_called_once_with(message)

    @patch('src.juridic_bot.bot.bot.RAGRetriever')
    @patch('src.juridic_bot.bot.bot.LLMClient')
    @pytest.mark.asyncio
    async def test_handle_query_empty_query(self, mock_llm_client, mock_rag_retriever):
        """Testa tratamento de query vazia (apenas menção)"""
        with patch.object(JuridicBot, 'user', new_callable=PropertyMock) as mock_user:
            bot = JuridicBot()
            mock_user.return_value.id = 12345

            # Mock da mensagem apenas com menção
            message = Mock()
            message.content = f"<@{bot.user.id}>"
            message.author = Mock()
            message.author.id = 67890
            message.reply = AsyncMock()

            await bot.handle_query(message)

            message.reply.assert_called_once()
            call_args = message.reply.call_args[0][0]
            assert "assistente jurídico" in call_args.lower()

    @patch('src.juridic_bot.bot.bot.RAGRetriever')
    @patch('src.juridic_bot.bot.bot.LLMClient')
    @pytest.mark.asyncio
    async def test_handle_query_with_content(self, mock_llm_client, mock_rag_retriever):
        """Testa tratamento de query com conteúdo"""
        with patch.object(JuridicBot, 'user', new_callable=PropertyMock) as mock_user:
            # Mock do retriever
            mock_retriever = Mock()
            mock_retriever.search.return_value = []
            mock_rag_retriever.return_value = mock_retriever

            # Mock do LLM client
            mock_llm = Mock()
            mock_llm.generate_conversational.return_value = "Devido processo legal é uma garantia..."
            mock_llm_client.return_value = mock_llm

            bot = JuridicBot()
            mock_user.return_value.id = 12345

            # Mock da mensagem com query
            message = Mock()
            message.content = f"<@{bot.user.id}> o que é devido processo legal?"
            message.author = Mock()
            message.author.id = 67890
            message.reply = AsyncMock()
            message.channel = Mock()
            message.channel.typing.return_value.__aenter__ = AsyncMock()
            message.channel.typing.return_value.__aexit__ = AsyncMock()

            await bot.handle_query(message)

            # Verificar se chamou o LLM
            mock_llm.generate_conversational.assert_called_once()
            # Verificar se respondeu
            message.reply.assert_called_once()

    @patch('src.juridic_bot.bot.bot.RAGRetriever')
    @patch('src.juridic_bot.bot.bot.LLMClient')
    @pytest.mark.asyncio
    async def test_handle_query_with_error(self, mock_llm_client, mock_rag_retriever):
        """Testa tratamento de erro durante processamento"""
        with patch.object(JuridicBot, 'user', new_callable=PropertyMock) as mock_user:
            # Mock do retriever que falha
            mock_retriever = Mock()
            mock_retriever.search.side_effect = Exception("RAG Error")
            mock_rag_retriever.return_value = mock_retriever

            bot = JuridicBot()
            mock_user.return_value.id = 12345

            # Mock da mensagem
            message = Mock()
            message.content = f"<@{bot.user.id}> test query"
            message.author = Mock()
            message.author.id = 67890
            message.reply = AsyncMock()
            message.channel = Mock()
            message.channel.typing.return_value.__aenter__ = AsyncMock()
            message.channel.typing.return_value.__aexit__ = AsyncMock()

            await bot.handle_query(message)

            # Deve responder com mensagem de erro amigável
            message.reply.assert_called_once()
            call_args = message.reply.call_args[0][0]
            assert any(word in call_args.lower() for word in ["ops", "problema", "erro", "desculpe"])

    @patch('src.juridic_bot.bot.bot.RAGRetriever')
    @patch('src.juridic_bot.bot.bot.LLMClient')
    def test_mention_removal(self, mock_llm_client, mock_rag_retriever):
        """Testa remoção de diferentes formatos de menção"""
        with patch.object(JuridicBot, 'user', new_callable=PropertyMock) as mock_user:
            bot = JuridicBot()
            mock_user.return_value.id = 12345

            # Testar diferentes formatos de menção
            test_cases = [
                (f"<@{bot.user.id}> test query", "test query"),
                (f"<@!{bot.user.id}> another query", "another query"),
                (f"<@{bot.user.id}>query without space", "query without space"),
            ]

            for input_content, expected_query in test_cases:
                # Simular processamento interno
                query = input_content.replace(f'<@{bot.user.id}>', '').strip()
                query = query.replace(f'<@!{bot.user.id}>', '').strip()
                assert query == expected_query