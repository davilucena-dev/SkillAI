import sys
import os
import shutil

REPO_URL = "https://github.com/davilucena-dev/SkillAI.git"

# Etapas exatas do carregamento — uma por chamada de avancar_etapa()
ETAPAS = [
    "🔐 Autenticando no Google Drive",
    "📦 Instalando dependências",
    "🎨 Configurando tema e agente",
    "⚙️  Instalando skills internas",
    "🚀 Iniciando interface",
]

_etapa_atual = 0
_display_id  = None


def ensure_in_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False


# ── Barra de progresso ────────────────────────────────────────────────────────

def _render_barra(etapa_idx, mensagem=None):
    total      = len(ETAPAS)
    pct        = int((etapa_idx / total) * 100)
    concluidas = etapa_idx

    itens_html = ""
    for i, nome in enumerate(ETAPAS):
        if i < concluidas:
            cor   = "#4ecb71"   # verde — concluída
            icone = "✓"
            opac  = "1"
        elif i == concluidas:
            cor   = "#4ecb71"   # verde — em andamento (piscando via CSS)
            icone = "›"
            opac  = "1"
            nome  = f'<span style="animation:pulse 1.2s ease infinite">{nome}</span>'
        else:
            cor   = "#2a3a2e"   # cinza-verde — pendente
            icone = "·"
            opac  = "0.4"

        itens_html += f"""
        <div style="display:flex;align-items:center;gap:10px;
                    padding:6px 0;opacity:{opac};transition:opacity .35s;">
          <span style="color:{cor};font-size:13px;width:16px;
                       text-align:center;font-weight:700;flex-shrink:0;">{icone}</span>
          <span style="color:{cor};font-family:monospace;font-size:12px;">{nome}</span>
        </div>"""

    msg_html = ""
    if mensagem:
        msg_html = f"""
        <div style="margin-top:14px;padding:8px 12px;
                    background:rgba(78,203,113,.06);
                    border-left:2px solid rgba(78,203,113,.4);
                    border-radius:3px;
                    color:#718a76;font-family:monospace;font-size:11px;">
          {mensagem}
        </div>"""

    concluido_html = ""
    if etapa_idx >= total:
        concluido_html = """
        <div style="margin-top:18px;display:flex;align-items:center;gap:8px;
                    color:#4ecb71;font-family:monospace;font-size:13px;font-weight:600;">
          <span>✓</span><span>SkillAI pronta — clique no botão abaixo!</span>
        </div>"""

    return f"""
<style>
  @keyframes pulse {{
    0%,100% {{ opacity:1; }}
    50%      {{ opacity:.45; }}
  }}
</style>
<div style="
  background:#090f0b;
  border:1px solid rgba(78,203,113,.12);
  border-radius:10px;
  padding:22px 26px;
  max-width:500px;
  margin:14px 0;
  font-family:monospace;
  box-shadow:0 4px 24px rgba(0,0,0,.4);
">
  <!-- Logo -->
  <div style="display:flex;align-items:baseline;gap:3px;margin-bottom:18px;">
    <span style="font-family:'Syne',sans-serif;font-weight:800;
                 font-size:17px;color:#e4ede6;">Skill</span>
    <span style="font-family:'Syne',sans-serif;font-weight:800;
                 font-size:17px;color:#4ecb71;">AI</span>
    <span style="font-size:10px;color:#2a3a2e;margin-left:8px;
                 border:1px solid rgba(78,203,113,.12);
                 border-radius:3px;padding:1px 6px;color:#4ecb71;opacity:.5;">v1.0</span>
    <span style="margin-left:10px;font-size:10.5px;
                 color:#344a38;letter-spacing:.04em;">· Criadora de Skills</span>
  </div>

  <!-- Barra percentual -->
  <div style="margin-bottom:16px;">
    <div style="display:flex;justify-content:space-between;
                margin-bottom:6px;font-size:10px;color:#344a38;">
      <span>carregando</span><span style="color:#4ecb71;">{pct}%</span>
    </div>
    <div style="background:#0d1510;border-radius:6px;height:5px;
                overflow:hidden;border:1px solid rgba(78,203,113,.08);">
      <div style="
        width:{pct}%;height:100%;
        background:linear-gradient(90deg,#163320,#4ecb71);
        border-radius:6px;
        transition:width .5s ease;
      "></div>
    </div>
  </div>

  <!-- Lista de etapas -->
  <div style="border-top:1px solid rgba(78,203,113,.07);padding-top:12px;">
    {itens_html}
  </div>

  {msg_html}
  {concluido_html}
</div>"""


def _init_barra():
    """Exibe a barra pela primeira vez no Colab, guardando o display_id para updates."""
    global _display_id
    if not ensure_in_colab():
        print("⏳ Carregando SkillAI...")
        return
    from IPython.display import display, HTML
    import uuid
    _display_id = str(uuid.uuid4()).replace("-", "")
    display(HTML(_render_barra(0)), display_id=_display_id)


def avancar_etapa(mensagem=None):
    """Avança uma etapa e re-renderiza a barra no mesmo lugar."""
    global _etapa_atual
    _etapa_atual = min(_etapa_atual + 1, len(ETAPAS))

    if ensure_in_colab() and _display_id:
        from IPython.display import update_display, HTML
        update_display(
            HTML(_render_barra(_etapa_atual, mensagem)),
            display_id=_display_id,
        )
    else:
        nome = ETAPAS[min(_etapa_atual - 1, len(ETAPAS) - 1)]
        sufixo = f" — {mensagem}" if mensagem else ""
        print(f"  [{_etapa_atual}/{len(ETAPAS)}] {nome}{sufixo}")


def finalizar_barra():
    """Marca todas as etapas como concluídas."""
    global _etapa_atual
    _etapa_atual = len(ETAPAS)
    if ensure_in_colab() and _display_id:
        from IPython.display import update_display, HTML
        update_display(HTML(_render_barra(_etapa_atual)), display_id=_display_id)
    else:
        print("✅ SkillAI pronta!")


# ── Autenticação e Drive ──────────────────────────────────────────────────────

def setup_auth_first():
    try:
        from google.colab import drive, auth
        from googleapiclient.discovery import build
    except ImportError:
        print("⚠️  Não está no Colab. Pulando autenticação.")
        return None, "https://drive.google.com/drive/my-drive"

    DRIVE_FOLDER = "SkillAI"
    MOUNT_PATH   = "/content/drive"
    FOLDER_PATH  = os.path.join(MOUNT_PATH, "My Drive", DRIVE_FOLDER)
    FALLBACK_URL = "https://drive.google.com/drive/my-drive"
    url_direta   = FALLBACK_URL

    if not os.path.exists(os.path.join(MOUNT_PATH, "My Drive")):
        try:
            drive.mount(MOUNT_PATH, force_remount=False)
        except Exception as e:
            print(f"⚠️  Aviso ao montar Drive: {e}")
            os.makedirs("/tmp/skillai_work", exist_ok=True)
            return "/tmp/skillai_work", FALLBACK_URL

    try:
        auth.authenticate_user()
    except Exception as e:
        print(f"⚠️  Aviso na autenticação: {e}")

    for subpasta in ["Referências", "Skills Geradas", "Backups"]:
        os.makedirs(os.path.join(FOLDER_PATH, subpasta), exist_ok=True)

    os.chdir(FOLDER_PATH)

    try:
        service   = build("drive", "v3")
        query     = (
            f"name = '{DRIVE_FOLDER}' "
            "and mimeType = 'application/vnd.google-apps.folder' "
            "and trashed = false"
        )
        resultado = service.files().list(q=query, fields="files(id)").execute()
        arquivos  = resultado.get("files", [])
        if arquivos:
            url_direta = f"https://drive.google.com/drive/folders/{arquivos[0]['id']}"
    except Exception:
        pass

    return FOLDER_PATH, url_direta


# ── Entrada ───────────────────────────────────────────────────────────────────

def run():
    _init_barra()

    # ── Etapa 1: Drive ────────────────────────────────────────────────────────
    folder_path, drive_url = setup_auth_first()
    avancar_etapa("Drive autenticado")

    # ── Etapa 2: Dependências ─────────────────────────────────────────────────
    from setup_dependencies import install_opencode, create_directories
    install_opencode()
    create_directories()
    avancar_etapa("OpenCode e libs instalados")

    # ── Etapa 3: Tema e agente ────────────────────────────────────────────────
    from setup_dependencies import setup_theme, setup_agent
    setup_theme()
    setup_agent()
    avancar_etapa("Tema e agente configurados")

    # ── Etapa 4: Skills ───────────────────────────────────────────────────────
    from setup_skills import install_skills
    install_skills()
    avancar_etapa("Skills instaladas")

    # ── Etapa 5: Interface ────────────────────────────────────────────────────
    from launch_app import launch, set_drive_info
    set_drive_info(folder_path, drive_url)
    avancar_etapa("Interface pronta")

    finalizar_barra()
    launch()


if __name__ == "__main__":
    run()
