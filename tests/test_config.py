"""
Testes para o módulo de configuração
"""
import pytest
from unittest.mock import patch
from src.juridic_bot.config import Config


class TestConfig:
    """Testes da classe Config"""

    @patch.dict('os.environ', {
        'DISCORD_TOKEN': 'test_token',
        'OPENROUTER_API_KEY': 'test_openrouter_key',
        'OPENAI_API_KEY': 'test_openai_key',
        'DISCORD_APP_ID': '123456789',
        'DISCORD_OWNER_ID': '987654321'
    })
    def test_config_validation_success(self):
        """Testa validação bem-sucedida da configuração"""
        # Quando todas as variáveis obrigatórias estão presentes
        try:
            Config.validate()
            assert True  # Se não lançou exceção, está ok
        except ValueError:
            pytest.fail("Configuração deveria ser válida")

    def test_config_validation_missing_required(self):
        """Testa validação com variáveis obrigatórias faltando"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                Config.validate()

            assert "faltando" in str(exc_info.value)

    @patch.dict('os.environ', {
        'DISCORD_TOKEN': 'test_token',
        'OPENROUTER_API_KEY': 'test_openrouter_key',
        'OPENAI_API_KEY': 'test_openai_key'
    })
    def test_config_default_values(self):
        """Testa valores padrão da configuração"""
        assert Config.OPENROUTER_MODEL == "anthropic/claude-3.5-sonnet"
        assert Config.TOP_K == 5
        assert Config.CHUNK_SIZE == 1500
        assert Config.MAX_TOKENS == 2000
        assert Config.TEMPERATURE == 0.7
        assert Config.LOG_LEVEL == "INFO"