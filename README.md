# 🛠️ SkillAI — Criadora de Skills Baseada em Referências

A **SkillAI** é uma agente executada no Google Colab especializada em **criar skills**
para outras agentes de IA. Lê materiais de referência fornecidos pelo usuário — artigos,
livros, documentações técnicas — e gera arquivos `SKILL.md` completos, corretos e
prontos para serem publicados em repositórios GitHub e plugados em qualquer outra agente.

Ela nunca inventa, nunca completa código por completar, e nunca entrega uma skill
passível de erro silencioso. Se a habilidade pedida for complexa demais para criar
com segurança, ela avisa e pede material de referência antes de prosseguir.

---

## 🛡️ Vantagens

| # | Benefício | Detalhe |
|---|-----------|---------|
| 1 | **100% Gratuito** | Roda na infraestrutura do Google + provedores de IA gratuitos |
| 2 | **Sem Instalação** | Pronto para uso direto no navegador |
| 3 | **Drive Integrado** | Skills geradas e referências salvas automaticamente |
| 4 | **Baseada em Evidências** | Nunca inventa — só cria a partir do que você fornece |
| 5 | **Sem Erros Silenciosos** | Skills complexas exigem referência documental antes de criar |

---

## 🚀 Como Iniciar

1. No menu superior, clique em **Ambiente de execução → Executar tudo** (ou `Ctrl + F9`).
2. Aguarde enquanto a barra de progresso mostra cada etapa sendo concluída.
3. Clique no botão que irá aparecer e a SkillAI abrirá em uma nova aba.
4. Na primeira vez, clique em **"+ provedor IA"** e insira sua chave de API
   (Groq, Anthropic, OpenAI, Gemini, entre outros).

---

## ℹ️ Informações Importantes

- **Navegador:** Use preferencialmente o **Google Chrome**.
- **Internet:** Conexão estável é obrigatória.
- **Google Drive:** Os dados ficam em `Meu Drive/SkillAI/`.
  - `Referências/` — material que você fornece para basear a criação de uma skill
  - `Skills Geradas/` — arquivos `SKILL.md` prontos, gerados pela agente
  - `Backups/` — backups de sessão e configuração
- **Permissões:** Conceda todas as permissões solicitadas pelo Colab.

---

## 📁 Estrutura do Drive

```
Meu Drive/
└── SkillAI/
    ├── Referências/      ← você coloca aqui o material de base
    ├── Skills Geradas/   ← a agente salva os SKILL.md prontos aqui
    └── Backups/          ← backups de sessão e configuração
```

---

## 🧠 Como a SkillAI Decide Criar uma Skill

| Tipo | Quando acontece | Comportamento |
|---|---|---|
| **Skill Simples** | Habilidade autocontida (texto, arquivos locais, formatação, fluxos lógicos) | Cria diretamente, sem precisar de referência |
| **Skill Complexa** | Envolve API externa, autenticação, modelos estatísticos/econométricos, scraping, banco de dados | Para e pede que você coloque material de referência em `Referências/` antes de criar |

---

## 💬 Exemplos de comandos para o chat

```
"Cria uma skill para formatar datas no padrão brasileiro."

"Cria uma skill para buscar dados da API do Banco Central."

"O que tenho em Referências?"

"Quais skills já criei?"

"Revisa a skill api-bcb."
```

---

## 📦 Como Usar uma Skill Gerada em Outra Agente

1. Pegue o arquivo `SKILL.md` salvo em `SkillAI/Skills Geradas/`.
2. Publique-o num repositório GitHub próprio.
3. No `setup_skills.py` da agente que vai usar a skill, adicione a URL em `REMOTE_SKILLS`:

```python
REMOTE_SKILLS = [
    # ... skills existentes ...
    ("https://github.com/seu-usuario/Skill-NomeDaSkill.git", "nome-da-skill"),
]
```

4. Na próxima execução dessa agente no Colab, a skill é clonada e instalada automaticamente.

---

## Célula de execução (cole no Colab):

```python
import os, sys, subprocess, shutil

REPO_URL = "https://github.com/davilucena-dev/SkillAI.git"
WORK_DIR = "/tmp/skillai"

print("⏳ Carregando a SkillAI...")

if os.path.exists(WORK_DIR):
    shutil.rmtree(WORK_DIR)

print("📥 Baixando arquivos...")
subprocess.run(["git", "clone", "--depth", "1", REPO_URL, WORK_DIR], capture_output=True)

os.chdir(WORK_DIR)
sys.path.insert(0, WORK_DIR)

from main import run
run()
```

---

## ⚠️ Limitações e Privacidade

A SkillAI **não substitui** revisão técnica especializada para skills de alta complexidade.
Toda skill gerada é baseada exclusivamente no que você fornece ou em comportamento Python
padrão de certeza — a agente não inventa, não especula e não completa código sem base.

> **Segurança:** Skills que envolvem acesso externo, autenticação ou modelos estatísticos
> só são criadas com material de referência documentado. Em caso de dúvida, a SkillAI
> sempre opta por pedir mais informação em vez de arriscar um erro silencioso.

---

## Citação / Créditos

Desenvolvido por **Davi Lucena da Silva**, doutorando em Economia Aplicada — UFV.
Contato: davilucenas99@gmail.com · (88) 99864-2605

Baseado na arquitetura do **PesquisAI** (Gustavo Bastos Braga, UFV, 2026).
Adaptado para criação automatizada de skills de agentes de IA.

---

*SkillAI · v1.0 · Criadora de Skills Baseada em Referências*
