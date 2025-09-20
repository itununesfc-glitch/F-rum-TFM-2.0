<!--- README.md for F-rum (TFM) --->

# 🚀 F-rum (TFM) — Repositório do servidor e fórum

> **Transformice private server + fórum integrado** — servidor de jogo em Python + módulo de fórum (Django) + frontend React.

![status-badge](https://img.shields.io/badge/status-development-yellow) ![python](https://img.shields.io/badge/python-3.11%2B-blue) ![license](https://img.shields.io/badge/license-MIT-brightgreen) ![docker](https://img.shields.io/badge/docker-ready-lightgrey)

---

### 📌 Objetivo deste README

* Documentar o conteúdo do repositório de forma clara, prática e navegável.
* Dar instruções rápidas para executar em ambiente de desenvolvimento (shims inclusos).
* Fornecer checklists de debug, segurança / compliance, e próximos passos para deploy.

---

## 📚 Sumário

1. [Visão geral](#-vis%C3%A3o-geral)
2. [Destaques desta versão do README](#-destaques-desta-vers%C3%A3o-do-readme)
3. [Estrutura do repositório](#-estrutura-do-reposit%C3%B3rio)
4. [Pré-requisitos](#-pr%C3%A9-requisitos)
5. [Quick start — modo desenvolvimento](#-quick-start--modo-desenvolvimento)
6. [Galeria & demos (imagens, GIFs, vídeos)](#-galeria--demos-imagens-gifs-v%C3%ADdeos)
7. [Docker (template)](#-docker-template)
8. [.env / env.example](#-env--envexample)
9. [Testes manuais & debug de handshake SWF](#-testes-manuais--debug-de-handshake-swf)
10. [Produção: dependências e instalação](#-produ%C3%A7%C3%A3o-depend%C3%AAncias-e-instala%C3%A7%C3%A3o)
11. [Segurança, LGPD e retenção de dados](#-seguran%C3%A7a-lgpd-e-reten%C3%A7%C3%A3o-de-dados)
12. [Troubleshooting rápido](#-troubleshooting-r%C3%A1pido)
13. [Checklist de testes / validação](#-checklist-de-testes--valida%C3%A7%C3%A3o)
14. [Roadmap & próximos passos](#-roadmap--pr%C3%B3ximos-passos)
15. [Contribuição](#-contribui%C3%A7%C3%A3o)
16. [Créditos & licença](#-cr%C3%A9ditos--licen%C3%A7a)

---

## 🔎 Visão geral

F-rum (TFM) reúne três camadas principais:

* **Servidor do jogo (Python)** — gerencia conexões, parsing de pacotes, autenticação, salas e estado dos jogadores.
* **Fórum (Django)** — backend de fórum com APIs e painel administrativo.
* **Frontend (React)** — interface do fórum, pronta para rodar com `npm start`.

O repositório inclui *shims* (módulos substitutos) para facilitar o desenvolvimento local sem dependências nativas pesadas.

> Este README é seu mapa: do `python start_server.py` ao `docker-compose` e deploy.

---

## ✨ Destaques desta versão do README

* ✅ Organização clara por seções e listas de verificação.
* 🖼️ Nova seção **Galeria & Demos** com instruções para adicionar imagens, GIFs e thumbnails de vídeo.
* 🐳 Template `docker-compose.yml` comentado para desenvolvimento.
* 🔐 Seção de segurança com pontos específicos para LGPD e dados sensíveis.
* 🧪 Checklist de testes e comandos úteis para debugging.
* 🧩 Modelos: `.env.example`, `Dockerfile` hints e `CI` suggestions.

---

## 🗂 Estrutura principal do repositório (resumido)

```
MainServer.py                # Servidor do jogo (entrada principal)
modules/                     # Parsing, Tribulle, ByteArray, bindings Lua, etc.
utils/                       # Config, Utils, Priv, Captcha, wrappers
include/files/infoSWF.json   # Metadados do SWF (version, CKEY, authkey)
database/                    # DB files (Cafe.db, Cafe1.db) + scripts SQL
forum/                       # Django forum (backend) + frontend (forum/frontend)
start_server.py              # Script dev: injeta shims para facilitar imports
dev_db.py                    # Shim de cursor para desenvolvimento
requirements.txt             # Dependências Python mínimas
```

> **Nota:** shims como `lupa.py`, `Config.py`, `ByteArray.py` foram adicionados para facilitar execução sem bibliotecas nativas.

---

## 🧰 Pré-requisitos

* **Python** 3.11+
* **Node.js** 18+ e npm/yarn (para `forum/frontend`)
* **Docker & docker-compose** (recomendado para reproducibilidade)
* (Opcional) MySQL 8.0 / SQLite para testes locais

---

## ⚡ Quick start — modo desenvolvimento

### 1) Virtualenv e dependências

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 2) Rodar validação de import (shims)

```bash
python start_server.py
```

> `start_server.py` usa `dev_db.py` para criar um `CursorShim` e em seguida importa `MainServer.py` para validar importações e flows iniciais.

### 3) Rodar o frontend do fórum (opcional)

```bash
cd forum/frontend
npm install
npm start
```

---

## 🖼️ Galeria & demos (imagens, GIFs, vídeos)

### Como adicionar mídia ao README

1. **Imagem no repositório (melhor para screenshots):**

```markdown
![Forum preview](docs/assets/forum-screenshot.png)
```

2. **GIF animado (looping):**

```markdown
![Loading gif](docs/assets/loading.gif)
```

3. **Thumbnail linkando para vídeo (YouTube / Vimeo):**

```markdown
[![Demo video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)
```

> Observação: GitHub não reproduz vídeos no README. Use thumbnails que abrem no YouTube/Vimeo.

### Seção de exemplo (coloque no README ou em `docs/`):

```markdown
## 📷 Galeria & demos

![Banner](docs/assets/banner.gif)

### Demo: servidor iniciando
[![Servidor demo](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)
```

### Prompts prontos para geração de arte/mídia

* **Banner cyberpunk:** `A futuristic hacker lounge, neon lights, cinematic banner, ultra-detailed, 4k`
* **GIF loading:** `Looping animation 'SERVER LOADING...', neon green terminal aesthetic, glitch effect`
* **Vídeo trailer (8s):** `Cinematic cyberpunk city with holograms of code, dramatic neon rain, 8 second trailer`

> Dica: gere assets em 2048px largura para garantir boa qualidade em thumbnails.

---

## 🐳 Docker (template)

Abaixo um `docker-compose.yml` de referência — ajuste conforme suas `Dockerfile`s e variáveis de ambiente.

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: cafe
    volumes:
      - ./database:/docker-entrypoint-initdb.d
    ports:
      - "3306:3306"

  backend:
    build: .
    command: python start_server.py
    volumes:
      - ./:/app
    environment:
      - PYTHONUNBUFFERED=1
      - APP_ENV=development
    depends_on:
      - mysql

  forum-frontend:
    working_dir: ./forum/frontend
    build:
      context: ./forum/frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

> Use `docker-compose up --build` para iniciar o ambiente. Para produção, crie imagens específicas e não monte volumes com código em produção.

---

## 🧩 .env / env.example (exemplo)

Crie um arquivo `.env` com as variáveis mínimas:

```dotenv
APP_ENV=development
HOST=0.0.0.0
PORT=8000

DB_HOST=mysql
DB_PORT=3306
DB_USER=root
DB_PASS=rootpass
DB_NAME=cafe

S3_BUCKET=
S3_REGION=sa-east-1
LOG_LEVEL=DEBUG
```

> Nunca comite segredos. Use GitHub Secrets / Vault para CI e produção.

---

## 🧪 Testes manuais & debug de handshake SWF

* `include/files/infoSWF.json` contém as chaves `version` e `CKEY` que o SWF espera.
* Se ocorrer a mensagem **"Incorrect version, try to reload the game."**:

  1. Valide JSON de `infoSWF.json` (`jq . include/files/infoSWF.json`).
  2. Revise `parseSWF` / `Client.parseString` em `MainServer.py`.
  3. Ative prints/hexdump no início de `Client.parseString` para inspecionar payloads.

**Teste rápido:**

```bash
python start_server.py      # valida imports e shims
# rodar servidor completo após configurar DB e variáveis
```

---

## 📦 Produção: dependências e instalação

* `requirements.txt`: `discord-webhook`, `pymysql` (entre outros listados).
* `lupa` (bindings Lua/Python) possui requisitos nativos — use shim em dev.

Debian/Ubuntu example:

```bash
sudo apt-get update
sudo apt-get install -y liblua5.3-dev libssl-dev build-essential lua5.3
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install lupa pymysql
```

---

## 🔐 Segurança, LGPD e retenção de dados

> **Atenção:** projetos que manipulam identificadores, avatares e logs devem ser tratados com cuidado.

* Classifique dados sensíveis e faça **DPIA** (Data Protection Impact Assessment).
* Retenção mínima: por exemplo, imagens temporárias 30 dias, logs críticos 1 ano (ajustável por regra).
* Criptografia em repouso (SSE-KMS, volumes encriptados) e em trânsito (TLS 1.2+).
* Proteções: rate limiting, WAF, autenticação forte e pen-test regular.
* Documente consentimento do usuário (se aplicável) e publicação de política de privacidade.

---

## 🛠 Troubleshooting rápido

* `ImportError`: verifique virtualenv, `pip install -r requirements.txt` e use shims se necessário.
* Conexões fechando: veja `include/SErros.log` e aumente o nível de log.
* Handshake SWF: habilite hexdump em `Client.parseString`.
* Geo-IP: garantir acesso à internet ou desligar geolocalização para dev.

---

## ✅ Checklist de testes / validação

* [ ] `python start_server.py` importa `MainServer.py` sem erros.
* [ ] Handshake SWF validado ao conectar cliente local.
* [ ] Testes de DB com `CursorShim` e com DB real (MySQL/SQLite).
* [ ] Frontend (`forum/frontend`) roda e consome API Django.
* [ ] Varredura por secrets hardcoded e pen-test básico executados.

---

## 🛣 Roadmap & próximos passos

* [ ] `docker-compose.yml` completo (backend + mysql + forum + redis + worker).
* [ ] Scripts de seed / migrations para popular `database/` com dados de teste.
* [ ] Testes unitários (pytest) para parsing e handshake.
* [ ] CI (GitHub Actions): lint, tests, build images e deploy automát.
* [ ] Melhor UX para debug (hexdumps controláveis, modo verbose via env var).

---

## 🤝 Contribuição

Contribuições são bem-vindas:

1. Fork ▶️ criar branch `feature/xxx` ▶️ commit ▶️ PR.
2. Inclua testes mínimos para alterações críticas.
3. Atualize o README com detalhes da mudança.

> Para mudanças grandes, abra uma issue antes de começar.

---

## 🧾 Créditos & licença

Atualizado pela equipe de manutenção do repositório.

Licença: **MIT** (ajuste conforme o repositório original).

---

## 📬 Precisa de ajuda?

Posso gerar:

* `docker-compose.yml` pronto para desenvolvimento.
* Scripts de seed/migration (SQLite/MySQL).
* PoC: integração de upload (presigned S3) e app de teste.
* Assets: sugestões de prompts para gerar imagens/GIFs/vídeos.

Se quiser que eu já injete trechos (docker-compose completo, seed, ou seção de galeria com placeholders), diga qual você prefere e eu gero aqui.

Obrigado! 🚀
