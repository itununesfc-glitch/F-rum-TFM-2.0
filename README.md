
# F-rum (TFM) — Repositório do servidor e fórum

Uma cópia do projeto "F-rum" (Transformice private server + fórum integrado). Este repositório contém o servidor do jogo em Python, módulos auxiliares, um backend de fórum em Django e a interface frontend (React) do fórum.

Este README foi atualizado para facilitar o uso em ambiente de desenvolvimento, descrever a estrutura do repositório, dependências e os passos recomendados para subir o servidor localmente.

🎯 Objetivo deste README
- Documentar o conteúdo do repositório de forma clara e navegável.
- Instruções rápidas de como executar em modo de desenvolvimento (shims inclusos).
- Notas de debug e próximos passos para um deploy completo.

## Estrutura principal do repositório

Top-level (resumido):

- `MainServer.py` — Código principal do servidor do jogo (parte mais importante). Trata conexões, parsing de pacotes, autenticação, gerenciamento de salas e estados dos jogadores.
- `modules/` — Módulos do servidor (ParsePackets, ParseCommands, Tribulle, Lua bindings, ByteArray, etc.).
- `utils/` — Utilitários e wrappers (Config, Utils, Priv, Captcha, etc.).
- `include/files/infoSWF.json` — Arquivo com metadados do SWF (versão, CKEY, chaves de pacotes, authkey). O servidor usa esse arquivo para validar handshake com o cliente SWF.
- `database/` — Arquivos de banco (ex.: `Cafe.db`, `Cafe1.db`) e scripts SQL; aqui ficam os dados persistidos.
- `forum/` — Aplicação Django do fórum (backend + frontend em `forum/frontend` com React).
- `start_server.py` — Script de desenvolvimento que injeta shims (cursores) para testar importações sem precisar de DB real.
- `dev_db.py` — Shim de cursor para desenvolvimento (retorna valores vazios seguros para evitar crashes durante import).
- `requirements.txt` — Dependências Python mínimas (discord-webhook, pymysql). Instale em um virtualenv antes de rodar.

Arquivos recém-adicionados/alterados (nota):
- Foram adicionados shims (`ByteArray.py`, `Identifiers.py`, `Config.py`, `Priv.py`, `Utils.py`, `lupa.py`) para permitir testes locais rápidos sem dependências nativas.
- `MainServer.py` recebeu correções de comportamento em `data_received` (evitar fechar conexões imediatamente) e fallback de geolocalização.

## Como rodar em modo desenvolvimento (rápido)

1. Crie e ative um virtualenv (recomendado Python 3.11+):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Rodar o modo dev (shim):

```bash
python start_server.py
```

`start_server.py` usa `dev_db.py` para criar um `CursorShim` e em seguida tenta importar `MainServer.py` e instanciar componentes mínimos. Ele NÃO sobe o servidor de rede por padrão — serve para validar import e handshake mínimo. Para testar mais, veja a seção "Testes manuais".

## Testes manuais e debug de handshake SWF

- O arquivo `include/files/infoSWF.json` contém a `version` e `key` (CKEY) esperadas pelo servidor. Se o cliente SWF apresentar "Incorrect version, try to reload the game.", verifique:
	1. `infoSWF.json` está bem formado (JSON válido)
 2. `MainServer.py` carrega esse arquivo corretamente (procurar no código por parseSWF)
 3. Ative logs no método `Client.parseString` — eu já adicionei um print debug que mostra os valores do cliente vs servidor.

Teste rápido do handshake (local):

1. Rode `python start_server.py` para validar import.
2. Se quiser testar handshake real, você precisa rodar o servidor completo (ver próximos passos) e conectar o SWF de cliente apontando para o host/porta.

## Dependências e notas de instalação

- Python packages (em `requirements.txt`): `discord-webhook`, `pymysql`.
- Dependências nativas possivelmente necessárias para recursos Lua: `lupa` (binding Lua/Python). No repositório incluí um shim `lupa.py` para testes, mas em produção prefira instalar `lupa` via pip e preparar Lua no sistema.

Instalação sugerida para produção (exemplo):

```bash
# No Debian/Ubuntu
sudo apt-get install -y liblua5.3-dev libssl-dev build-essential lua5.3
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install lupa pymysql
```

## Principais pontos de atenção / troubleshooting

- Banco de dados: O servidor espera cursores/ligação com um MySQL/SQLite conforme a configuração. Em dev use os shims ou configure `Cursor`/`CursorCafe` para apontar para os bancos em `database/`.
- Geo-IP: O servidor consulta um serviço externo para geolocalização; adicione um timeout ou rode em um ambiente com acesso à internet.
- Mensagens de erro: Erros são registrados em `include/SErros.log` — verifique esse arquivo se o servidor fechar conexões inesperadamente.
- Handshake: Se o cliente SWF continuar a reclamar de versão incorreta, ative o hexdump no início de `Client.parseString` (já adicionei prints) para ver exatamente o payload que o SWF envia.

## Estrutura do fórum (resumida)

- `forum/backend/` — Django app (servidor do fórum). Contém `manage.py`, app `forum`, e configurações Django.
- `forum/frontend/` — frontend em React (package.json presente). Use `npm install` e `npm start` para rodar o frontend localmente.

## Próximos passos recomendados

1. Se quiser que eu suba o servidor aqui, confirme se posso instalar dependências (pip, pacotes de sistema) no container/dev. Posso tentar instalar `lupa`, configurar um banco SQLite temporário e iniciar o servidor para testes end-to-end.
2. Preparar scripts de migração/seed para popular o banco (usuários de teste) para validar logins.
3. Escrever testes unitários minimalistas para `Client.parseString` e parsing de `infoSWF.json`.

## Créditos e notas finais

Este README foi gerado/atualizado pelo time de manutenção do repositório para facilitar a retomada do projeto. Se quiser, eu posso:

- Gerar um `docker-compose.yml` que sobe MySQL + servidor + frontend para testes.
- Implementar testes automatizados (pytest) para as funções críticas.
- Fazer um walkthrough interativo para subir o servidor em produção.

Obrigado! 🚀
