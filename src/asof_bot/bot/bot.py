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