# 📚 Documentação - Bot Jurídico Conversacional

Esta pasta contém a documentação completa do projeto, servida diretamente pelo GitHub Pages.

## 🚀 Como Usar

### Para Desenvolvedores

1. **Instalar dependências de documentação:**
   ```bash
   uv sync --group docs
   ```

2. **Servir documentação localmente:**
   ```bash
   uv run mkdocs serve
   ```

3. **Fazer deploy para GitHub Pages:**
   ```bash
   ./scripts/deploy-docs.sh
   ```

### Para Usuários Finais

A documentação está disponível online em: [https://prof-ramos.github.io/SamerPosterga](https://prof-ramos.github.io/SamerPosterga)

## 📁 Estrutura

```
docs/
├── index.md                      # Página inicial
├── instalacao/                   # Guias de instalação
├── implantacao/                  # Guias de implantação
├── assets/                       # Recursos estáticos
├── .nojekyll                     # Desabilita processamento Jekyll
└── README.md                     # Este arquivo
```

## 🔧 Configuração do GitHub Pages

Para ativar o GitHub Pages neste repositório:

1. Vá para **Settings** > **Pages**
2. Em "Source", selecione **"Deploy from a branch"**
3. Em "Branch", selecione **main** e pasta **/docs**
4. Clique em **Save**

## 📝 Editando Documentação

### Arquivos Fonte
- Todos os arquivos `.md` são os arquivos fonte
- Os arquivos `.html` são gerados automaticamente
- **Nunca edite os arquivos `.html` diretamente**

### Adicionando Novo Conteúdo
1. Crie ou edite arquivos `.md` na estrutura apropriada
2. Execute `./scripts/deploy-docs.sh` para atualizar
3. Faça commit e push das mudanças

### Navegação
A navegação é controlada pelo arquivo `mkdocs.yml` na raiz do projeto.

## 🎨 Tema e Personalização

- **Tema**: Material Design (MkDocs-Material)
- **Idioma**: Português brasileiro
- **CSS personalizado**: `assets/stylesheets/extra.css`
- **Paleta**: Azul com tema claro/escuro

## 🔍 Plugins Utilizados

- **Search**: Busca full-text
- **Git Revision Date**: Mostra datas de modificação
- **Git Committers**: Mostra autores das páginas
- **Minify**: Otimiza arquivos CSS/JS

## 📊 Status da Documentação

- ✅ **Páginas básicas**: Criadas
- ✅ **GitHub Pages**: Configurado
- ✅ **Deploy script**: Funcionando
- 🔄 **Páginas avançadas**: Em desenvolvimento
- 📋 **TODO**: Completar todas as seções planejadas

## 🤝 Contribuição

Para contribuir com a documentação:

1. Siga os padrões de escrita em português brasileiro
2. Use markdown consistente
3. Teste localmente antes de commitar
4. Mantenha links atualizados

---

**💡 Dica**: Use `uv run mkdocs serve` para preview local antes de fazer deploy.