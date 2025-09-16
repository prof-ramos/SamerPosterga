# Deploy no Portainer

Este diretório contém os arquivos necessários para deploy do Juridic Bot no Portainer.

## Arquivos

- `portainer-stack.yml` - Stack completa para Portainer
- `environment-template.env` - Template de variáveis de ambiente

## Instruções de Deploy

### 1. Preparar Ambiente

1. Copie `environment-template.env` para `.env`
2. Configure todas as variáveis obrigatórias:
   - `DISCORD_TOKEN`
   - `OPENAI_API_KEY`
   - `OPENROUTER_API_KEY`
   - `DISCORD_OWNER_ID`

### 2. Deploy no Portainer

1. Acesse Portainer → Stacks → Add Stack
2. Cole o conteúdo de `portainer-stack.yml`
3. Configure as variáveis de ambiente
4. Deploy da stack

### 3. Adicionar Documentos

Os documentos agora são incluídos diretamente na imagem do Docker. Para atualizar a base de conhecimento, é necessário reconstruir a imagem.



## Monitoramento

- **Logs**: Portainer → Containers → juridic-concursos-bot → Logs
- **Status**: Health check automático configurado
- **Recursos**: Container → Stats

## Variáveis Importantes

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `DISCORD_TOKEN` | ✅ | Token do bot Discord |
| `OPENAI_API_KEY` | ✅ | API OpenAI para embeddings |
| `OPENROUTER_API_KEY` | ✅ | API OpenRouter para LLM |
| `DISCORD_OWNER_ID` | ✅ | ID do usuário administrador |
| `SYSTEM_PROMPT` | ❌ | Prompt personalizado do bot |
| `TOP_K` | ❌ | Número de documentos na busca (padrão: 5) |

## Suporte

Para dúvidas, consulte a [documentação completa](../../docs/) ou abra uma issue no repositório.