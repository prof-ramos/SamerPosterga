"""
Implementação do Bot Discord com capacidades RAG
"""
import asyncio
import logging
from datetime import datetime
import discord
from discord.ext import commands
import psutil

from ..config import Config
from ..rag.ingest import DocumentProcessor
from ..rag.retriever import RAGRetriever
from ..llm.client import LLMClient

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
        try:
            if Config.DISCORD_GUILD_ID and Config.DISCORD_GUILD_ID.strip():
                guild = discord.Object(id=int(Config.DISCORD_GUILD_ID))
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                logger.info(f"Comandos sincronizados para guild {Config.DISCORD_GUILD_ID}")
            else:
                await self.tree.sync()
                logger.info("Comandos globais sincronizados")
        except Exception as e:
            logger.error(f"Erro ao sincronizar comandos: {e}")
            logger.info("Continuando sem sincronização de comandos")

    async def on_ready(self):
        """Evento quando o bot está pronto"""
        logger.info(f'{self.user} está online!')
        logger.info(f'ID: {self.user.id}')
        logger.info(f'Servidores: {len(self.guilds)}')

        # Definir status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="dúvidas de concurso | @mention"
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
        """Processa consultas ao RAG de forma conversacional"""
        # Remover menção do bot da query
        query = message.content.replace(f'<@{self.user.id}>', '').strip()

        if not query:
            # Resposta amigável quando não há pergunta específica
            responses = [
                "Olá! 👋 Sou um assistente jurídico especializado em concursos públicos. Como posso te ajudar hoje?",
                "Oi! 😊 Estou aqui para ajudar com dúvidas sobre direito. O que você gostaria de saber?",
                "Olá! 📚 Pronto para tirar dúvidas sobre legislação e direito. Qual é sua pergunta?"
            ]
            await message.reply(responses[hash(message.author.id) % len(responses)])
            return

        # Indicador de digitação
        async with message.channel.typing():
            try:
                # Buscar documentos relevantes
                documents = self.retriever.search(query, k=3)

                if not documents:
                    # Resposta quando não encontra documentos
                    responses = [
                        "Hmm, não encontrei informações específicas sobre isso nos meus documentos. Poderia reformular a pergunta ou dar mais detalhes?",
                        "Não tenho informações precisas sobre esse tema ainda. Que tal tentar uma pergunta mais específica sobre direito?",
                        "Ops, parece que não tenho dados suficientes sobre isso. Tente perguntar sobre algum aspecto específico do direito brasileiro!"
                    ]
                    await message.reply(responses[hash(query) % len(responses)])
                    return

                # Formatar contexto
                context = self.retriever.format_context(documents)

                # Gerar resposta conversacional
                response = self.llm_client.generate_conversational(query, context)

                # Limitar tamanho para evitar problemas
                if len(response) > 1800:
                    response = response[:1800] + "..."

                await message.reply(response)

            except Exception as e:
                logger.error(f"Erro ao processar query: {e}")
                # Resposta de erro mais amigável
                error_responses = [
                    "Desculpe, tive um probleminha técnico. Pode tentar perguntar de novo?",
                    "Ops! Algo deu errado. Tente reformular sua pergunta, por favor!",
                    "Hmm, parece que houve um erro. Que tal tentar novamente?"
                ]
                await message.reply(error_responses[hash(str(e)) % len(error_responses)])

    async def send_long_message(self, message: discord.Message, content: str):
        """Envia mensagens longas divididas em chunks"""
        MAX_LENGTH = 2000

        if len(content) <= MAX_LENGTH:
            await message.reply(content)
            return

        # Dividir mensagem
        chunks = []
        current_chunk = ""
        lines = content.split('\n')

        for line in lines:
            if len(current_chunk) + len(line) + 1 > MAX_LENGTH:
                if current_chunk:
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
    embed.add_field(name="CPU", value=".1f", inline=True)
    embed.add_field(name="RAM", value=".1f", inline=True)
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


@bot.tree.command(name="pergunta")
async def pergunta(interaction: discord.Interaction, pergunta: str):
    """Faça uma pergunta jurídica ao bot"""
    await interaction.response.defer()

    try:
        # Buscar documentos relevantes
        documents = bot.retriever.search(pergunta, k=5)

        if not documents:
            await interaction.followup.send("❌ Não encontrei informações relevantes para sua pergunta. Tente reformular ou adicionar mais detalhes.")
            return

        # Formatar contexto
        context = bot.retriever.format_context(documents)

        # Gerar resposta usando LLM
        response = bot.llm_client.generate(pergunta, context)

        # Adicionar disclaimer
        response = bot.llm_client.add_disclaimer(response)

        # Adicionar fontes citadas
        if documents:
            sources = list(set(doc.metadata.get('source', 'N/A') for doc in documents))
            response += f"\n\n📚 **Fontes consultadas:** {', '.join(sources[:3])}"  # Limitar a 3 fontes

        # Verificar tamanho da resposta
        if len(response) > 1900:  # Discord limit
            response = response[:1900] + "\n\n... (resposta truncada)"

        await interaction.followup.send(response)

    except Exception as e:
        logger.error(f"Erro ao processar pergunta: {e}")
        await interaction.followup.send("❌ Desculpe, ocorreu um erro ao processar sua solicitação.\n\n⚖️ Nota: Esta é uma resposta gerada por IA com base em documentos disponíveis. Para questões legais específicas, consulte sempre um profissional qualificado.")


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
        title="🤖 Bot Jurídico para Concursos - Ajuda",
        description="Assistente especializado em questões jurídicas para estudantes de concursos públicos",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Como usar",
        value="• Me mencione (@bot) seguido de sua pergunta\n• Envie DM diretamente\n• Use os comandos slash disponíveis",
        inline=False
    )

    embed.add_field(
        name="Comandos",
        value="`/pergunta` - Faça perguntas jurídicas\n`/ping` - Verifica latência\n`/status` - Status do sistema\n`/buscar_lei` - Busca lei específica\n`/ajuda` - Este menu",
        inline=False
    )

    embed.add_field(
        name="Especialidades",
        value="• Direito Constitucional\n• Direito Administrativo\n• Direito Penal\n• Direito Civil\n• Direito Processual\n• E muito mais!",
        inline=False
    )

    embed.set_footer(text="Bot desenvolvido para auxiliar estudantes de concursos públicos")

    await interaction.response.send_message(embed=embed)