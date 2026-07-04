import os
import shutil
import subprocess

SKILLS_DIR = os.path.expanduser("~/.agents/skills")

# Skills remotas da SkillAI — adicione aqui quando publicar no GitHub.
# Por enquanto vazio: a SkillAI não depende de skills externas para funcionar,
# pois sua habilidade principal (criar skills) está no system prompt.
REMOTE_SKILLS = [
    # ("https://github.com/davilucena-dev/Skill-AlgumaCoisa.git", "alguma-coisa"),
]


def create_local_skills(progress_callback=None):
    """Cria as skills internas da SkillAI diretamente no disco."""

    os.makedirs(SKILLS_DIR, exist_ok=True)

    # ── Skill: leitura-referencias ───────────────────────────────────────────
    skill_dir = os.path.join(SKILLS_DIR, "leitura-referencias")
    os.makedirs(skill_dir, exist_ok=True)

    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("""\
---
name: leitura-referencias
description: >
  Use esta skill sempre que precisar ler ou listar arquivos da pasta
  Referências/ da SkillAI no Drive. Ativa quando o usuário pede para
  criar uma skill com base em um material, quando pergunta quais referências
  estão disponíveis, ou quando você precisa acessar o conteúdo de um arquivo
  antes de gerar um SKILL.md.
---
# Skill: Leitura de Referências — SkillAI

## Propósito
Listar e ler os arquivos de referência em
`/content/drive/My Drive/SkillAI/Referências/`
que o usuário forneceu como base para criação de skills.

## O que esta skill NÃO faz
- Não lê arquivos fora de `Referências/`
- Não interpreta o conteúdo — apenas o entrega para análise
- Não assume o que está num arquivo sem lê-lo primeiro

## Listagem de Arquivos
```python
import os

referencias_path = "/content/drive/My Drive/SkillAI/Referências"

if os.path.isdir(referencias_path):
    arquivos = os.listdir(referencias_path)
    if arquivos:
        for nome in arquivos:
            print(f"  - {nome}")
    else:
        print("⚠️ A pasta Referências/ está vazia.")
else:
    print("⚠️ Pasta Referências/ não encontrada.")
```

## Leitura por Tipo de Arquivo

### TXT / MD
```python
caminho = f"/content/drive/My Drive/SkillAI/Referências/arquivo.txt"
try:
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
except Exception as e:
    print(f"⚠️ Erro ao ler arquivo: {e}")
    conteudo = None
```

### PDF (texto puro — sem OCR)
```python
# Requer: pip install pypdf2
try:
    import PyPDF2
    with open(caminho, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        conteudo = "\\n".join(
            page.extract_text() or "" for page in reader.pages
        )
except Exception as e:
    print(f"⚠️ Erro ao ler PDF: {e}")
    conteudo = None
```

### JSON
```python
import json
try:
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = json.load(f)
except Exception as e:
    print(f"⚠️ Erro ao ler JSON: {e}")
    conteudo = None
```

## Regras
- Sempre liste os arquivos disponíveis e confirme com o usuário qual usar antes de ler.
- Se a pasta estiver vazia, oriente o usuário a colocar o material lá.
- Nunca assuma o conteúdo de um arquivo sem lê-lo primeiro.
- Se a leitura falhar, informe o erro e peça ao usuário para verificar o arquivo.
""")
    print("✅ Skill leitura-referencias criada.")
    if progress_callback:
        progress_callback("skill: leitura-referencias")

    # ── Skill: gestao-skills-geradas ─────────────────────────────────────────
    skill_dir = os.path.join(SKILLS_DIR, "gestao-skills-geradas")
    os.makedirs(skill_dir, exist_ok=True)

    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("""\
---
name: gestao-skills-geradas
description: >
  Use esta skill para salvar, listar ou revisar skills geradas pela SkillAI
  na pasta Skills Geradas/ do Drive. Ativa quando você termina de criar um
  SKILL.md e precisa salvá-lo, quando o usuário pergunta quais skills já foram
  criadas, ou quando pede para revisar uma skill existente.
---
# Skill: Gestão de Skills Geradas — SkillAI

## Propósito
Salvar, listar e organizar os arquivos `SKILL.md` gerados pela SkillAI
em `/content/drive/My Drive/SkillAI/Skills Geradas/`.

## O que esta skill NÃO faz
- Não publica no GitHub — apenas salva localmente no Drive
- Não sobrescreve arquivos sem confirmação do usuário

## Caminho Base
```python
import os
skills_path = "/content/drive/My Drive/SkillAI/Skills Geradas"
os.makedirs(skills_path, exist_ok=True)
```

## Nomenclatura dos Arquivos
```
skill_[nome-da-skill]_[DDMMAAAA].md

Exemplos:
  skill_api-bcb_28062026.md
  skill_formatacao-abnt_28062026.md
  skill_leitura-csv_28062026.md
```

## Salvar SKILL.md
```python
from datetime import datetime
import os

def salvar_skill(nome_skill, conteudo_md):
    skills_path = "/content/drive/My Drive/SkillAI/Skills Geradas"
    os.makedirs(skills_path, exist_ok=True)

    data = datetime.now().strftime("%d%m%Y")
    nome_arquivo = f"skill_{nome_skill}_{data}.md"
    caminho = os.path.join(skills_path, nome_arquivo)

    # Verifica se já existe
    if os.path.exists(caminho):
        print(f"⚠️ Arquivo já existe: {nome_arquivo}")
        print("Confirme se deseja sobrescrever antes de prosseguir.")
        return None

    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo_md)
        print(f"[📄 Arquivo Gerado] {nome_arquivo} — salvo em SkillAI/Skills Geradas/")
        return caminho
    except Exception as e:
        print(f"⚠️ Erro ao salvar skill: {e}")
        return None
```

## Listar Skills Geradas
```python
def listar_skills_geradas():
    skills_path = "/content/drive/My Drive/SkillAI/Skills Geradas"
    try:
        arquivos = sorted(os.listdir(skills_path))
        skills = [a for a in arquivos if a.endswith(".md")]
        if skills:
            print(f"📦 {len(skills)} skill(s) gerada(s):")
            for s in skills:
                print(f"  - {s}")
        else:
            print("Nenhuma skill gerada ainda.")
        return skills
    except Exception as e:
        print(f"⚠️ Erro ao listar skills: {e}")
        return []
```

## Registrar no Log
```python
from datetime import datetime

def registrar_log(nome_skill, referencia_usada, tipo="CRIAÇÃO"):
    log_path = "/content/drive/My Drive/SkillAI/Skills Geradas/log_skills.log"
    ts = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(
                f"[{ts}] {tipo} | {nome_skill} "
                f"| Referência: {referencia_usada}\\n"
            )
    except Exception as e:
        print(f"⚠️ Erro ao registrar log: {e}")
```

## Regras
- Nunca sobrescreva um arquivo existente sem confirmação explícita do usuário.
- Sempre registre no log após salvar qualquer skill.
- Ao salvar, exiba sempre:
  `[📄 Arquivo Gerado] NOME — salvo em SkillAI/Skills Geradas/`
- Se o caminho do Drive não estiver montado, informe o usuário.
""")
    print("✅ Skill gestao-skills-geradas criada.")
    if progress_callback:
        progress_callback("skill: gestao-skills-geradas")

    # ── Skill: avaliacao-complexidade ─────────────────────────────────────────
    skill_dir = os.path.join(SKILLS_DIR, "avaliacao-complexidade")
    os.makedirs(skill_dir, exist_ok=True)

    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("""\
---
name: avaliacao-complexidade
description: >
  Use esta skill antes de criar qualquer skill pedida pelo usuário.
  Ativa automaticamente quando o usuário pede a criação de uma skill,
  para decidir se ela pode ser criada diretamente (skill simples) ou
  se exige material de referência (skill complexa). Nunca pule esta
  avaliação.
---
# Skill: Avaliação de Complexidade — SkillAI

## Propósito
Avaliar se uma skill pedida pelo usuário pode ser criada com segurança
sem material de referência (skill simples) ou se exige referência
para não gerar código com erros (skill complexa).

## O que esta skill NÃO faz
- Não cria a skill — apenas avalia se é seguro criar
- Não substitui o julgamento sobre a qualidade do conteúdo

## Critérios de Classificação

### ✅ Skill Simples — pode criar diretamente
A habilidade é autocontida e não depende de comportamentos externos:
- Manipulação de texto, strings, arquivos locais
- Formatação, conversão ou estruturação de dados
- Fluxos lógicos com bibliotecas Python padrão (`os`, `json`, `csv`, `datetime`)
- Operações que não falham silenciosamente

### ⚠️ Skill Complexa — exige referência antes de criar
A habilidade envolve qualquer um dos itens abaixo:

| Indicador de complexidade | Exemplos |
|---|---|
| API externa | Banco Central, IBGE, OpenAlex, qualquer REST/GraphQL |
| Autenticação | OAuth, tokens, chaves de API, credenciais |
| Modelos estatísticos ou econométricos | regressão, séries temporais, modelos ML |
| Scraping ou automação de navegador | BeautifulSoup, Selenium, Playwright |
| Banco de dados | SQL, MongoDB, BigQuery, qualquer ORM |
| Bibliotecas de terceiros críticas | onde um parâmetro errado quebra silenciosamente |
| Área técnica especializada | onde você não tem certeza do comportamento correto |

## Fluxo de Avaliação

```
1. Leia o pedido do usuário.
2. Identifique a habilidade central que a skill precisa ter.
3. Verifique cada critério da tabela acima.
4. Se nenhum critério de complexidade for atendido → Skill Simples.
5. Se qualquer critério for atendido → Skill Complexa.
```

## Mensagem Padrão — Skill Complexa
```
⚠️ Esta skill envolve [descreva o motivo específico] e pode conter
erros se criada sem base documental.

Para garantir uma skill correta e sem falhas, coloque em:
  SkillAI/Referências/

...o material que ensina como fazer isso (documentação oficial,
artigo, livro técnico ou exemplo funcional comprovado).

Quando o arquivo estiver lá, me avise e eu crio a skill com base nele.
```

## Regras
- Sempre avalie antes de criar — nunca pule esta etapa.
- Em caso de dúvida, classifique como Complexa. É melhor pedir referência
  do que entregar uma skill com erro silencioso.
- Nunca tente criar uma skill complexa sem referência, mesmo que o usuário insista.
  Explique o risco e mantenha a posição.
""")
    print("✅ Skill avaliacao-complexidade criada.")
    if progress_callback:
        progress_callback("skill: avaliacao-complexidade")

    # ── Skill: formato-skill-md ───────────────────────────────────────────────
    skill_dir = os.path.join(SKILLS_DIR, "formato-skill-md")
    os.makedirs(skill_dir, exist_ok=True)

    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write("""\
---
name: formato-skill-md
description: >
  Use esta skill ao escrever o conteúdo de qualquer SKILL.md.
  Ativa quando você já avaliou a complexidade, já leu a referência
  (se houver) e está pronto para gerar o arquivo final.
  Garante que o SKILL.md gerado siga o formato correto e seja
  plugável em qualquer agente que use esta arquitetura.
---
# Skill: Formato de SKILL.md — SkillAI

## Propósito
Garantir que todo `SKILL.md` gerado pela SkillAI siga a estrutura
correta, com frontmatter YAML, seções obrigatórias e código funcional,
pronto para ser publicado num repositório GitHub e plugado em outra agente.

## O que esta skill NÃO faz
- Não define o conteúdo — apenas o formato
- Não valida se o código está correto — isso vem da referência

## Estrutura Obrigatória

```markdown
---
name: [nome-da-skill-em-kebab-case]
description: >
  [Quando o agente deve ativar esta skill. Seja específico:
   mencione os gatilhos, o que a skill entrega e para que serve.
   Esta descrição é lida pelo agente para decidir quando usar a skill.]
---
# Skill: [Nome Legível da Skill]

## Propósito
[O que esta skill faz. 2 a 4 linhas, direto ao ponto.]

## O que esta skill NÃO faz
- [Limitação 1 — o que está fora do escopo]
- [Limitação 2]

## [Seções específicas da habilidade]
[Número e nome das seções variam conforme a skill.
 Inclua o que for relevante entre:]
  - Instalação de dependências (se houver)
  - Pré-requisitos
  - Fluxo passo a passo
  - Exemplos de código funcionais
  - Tabelas de referência (endpoints, códigos, parâmetros)
  - Tratamento de erros

## Regras
### O que SEMPRE fazer
- [Regra 1]
- [Regra 2]

### O que NUNCA fazer
- [Regra 1]
- [Regra 2]

### Quando algo falhar
[Como o agente deve se comportar em caso de erro ou dado ausente.]
```

## Regras de Formato

### Frontmatter
- O bloco `---` é obrigatório — sem ele o OpenCode não reconhece a skill.
- `name` deve ser em kebab-case: `minha-skill`, não `MinhaSkill` nem `minha_skill`.
- `description` deve responder: *quando* usar, *para que* serve, *o que* entrega.
  Não descreva só o que a skill faz — diga ao agente *quando ativá-la*.

### Seções intermediárias
- Adapte ao tipo de habilidade. Não use sempre o mesmo template.
- Se a skill acessa recurso externo: inclua sempre instalação + tratamento de erro.
- Se a skill tem fluxo de múltiplos passos: numere-os explicitamente.
- Se há tabela de referência (endpoints, códigos): inclua-a antes do código.

### Código
- Todo código deve ser funcional e derivado do material de referência.
- Todo acesso externo (arquivo, API, banco) deve ter try/except.
- Nunca deixe `# TODO`, `pass` sem explicação ou `...` como placeholder.
- Dependências de terceiros: sempre inclua a instrução de instalação antes do uso.

### O que NÃO incluir
- Não inclua código que você não tem certeza que funciona.
- Não inclua seções genéricas que não se aplicam à habilidade.
- Não repita no corpo o que o frontmatter já diz.

## Exemplo de Frontmatter Correto
```yaml
---
name: formatacao-abnt
description: >
  Use esta skill quando precisar formatar referências bibliográficas
  no padrão ABNT NBR 6023:2018. Ativa quando o usuário pede referências
  formatadas, quando há lista de artigos para citar, ou quando a skill
  de busca de artigos precisa formatar seus resultados.
  Entrega strings formatadas prontas para uso em relatórios.
---
```

## Exemplo de Frontmatter Incorreto
```yaml
---
name: FormatacaoABNT          ← errado: não é kebab-case
description: Formata ABNT.   ← errado: não diz quando usar nem o que entrega
---
```
""")
    print("✅ Skill formato-skill-md criada.")
    if progress_callback:
        progress_callback("skill: formato-skill-md")


def install_skills(progress_callback=None):
    os.chdir("/tmp")
    print("🔧 Instalando skills da SkillAI...")

    create_local_skills(progress_callback=progress_callback)

    # Skills remotas do GitHub
    for repo_url, name in REMOTE_SKILLS:
        tmp = f"/tmp/skill_{name}"
        if os.path.exists(tmp):
            shutil.rmtree(tmp)
        result = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, tmp],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            dest = os.path.join(SKILLS_DIR, name)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(tmp, dest, dirs_exist_ok=True)
            print(f"✅ {name} instalada do GitHub.")
            if progress_callback:
                progress_callback(f"skill remota: {name}")
        else:
            print(f"❌ Falha ao clonar {repo_url}")

    total = len(REMOTE_SKILLS) + 4  # 4 skills locais
    print(f"\n🎉 Todas as skills da SkillAI instaladas! ({total} no total)")
    return total


if __name__ == "__main__":
    install_skills()
