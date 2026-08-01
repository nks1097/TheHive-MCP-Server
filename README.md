# 🐝 TheHive MCP Server

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-2025--11--25-green.svg)](https://modelcontextprotocol.io/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-yellow.svg)](LICENSE)

**TheHive MCP Server** é um servidor **MCP (Model Context Protocol)** dedicado à gestão de incidentes, triagem forense, resposta a incidentes, análise automatizada via **Cortex** e sincronização de inteligência de ameaças via **MISP**, construído sobre a API do **TheHive 5**.

---

## 🛠️ Catálogo Completo de Ferramentas MCP (70 Tools)

### 📁 1. Gestão de Casos e Investigações (15 Tools)

| Nº | Ferramenta MCP | Descrição Operacional |
| :---: | :--- | :--- |
| **01** | `criar_caso_thehive` | Cria um novo caso de incidente de segurança no TheHive. |
| **02** | `listar_casos_thehive` | Lista os casos de incidentes mais recentes no TheHive. |
| **03** | `obter_caso_thehive` | Obtém detalhes completos de um caso de incidente pelo ID. |
| **04** | `atualizar_caso_thehive` | Atualiza descrição, severidade, status, resolução ou responsável. |
| **05** | `deletar_caso_thehive` | Exclui um caso de incidente do TheHive. |
| **06** | `fechar_caso_thehive` | Fecha um caso com veredito (TruePositive, FalsePositive, Indeterminate). |
| **07** | `reabrir_caso_thehive` | Reabre um caso encerrado no TheHive. |
| **08** | `atribuir_caso_thehive` | Atribui um responsável (usuário) a um caso no TheHive. |
| **09** | `adicionar_tag_caso_thehive` | Adiciona tags de identificação a um caso. |
| **10** | `remover_tag_caso_thehive` | Remove tags de um caso no TheHive. |
| **11** | `obter_timeline_caso_thehive` | Recupera a linha do tempo completa de eventos do caso. |
| **12** | `listar_logs_caso_thehive` | Lista logs de auditoria e atividades registradas em um caso. |
| **13** | `buscar_casos_thehive` | Pesquisa casos por qualquer termo (título, descrição, status, tag). |
| **14** | `adicionar_comentario_caso_thehive` | Adiciona um comentário técnico na aba de investigação. |
| **15** | `buscar_casos_duplicados_thehive` | Verifica se existe caso idêntico criado recentemente. |

---

### 📋 2. Tarefas e Logs de Atividades (8 Tools)

| Nº | Ferramenta MCP | Descrição Operacional |
| :---: | :--- | :--- |
| **16** | `obter_tarefas_thehive` | Busca tarefas (específica por ID, por caso ou gerais). |
| **17** | `criar_tarefa_thehive` | Cria uma nova tarefa dentro de um caso do TheHive. |
| **18** | `atualizar_tarefa_thehive` | Atualiza título, descrição, status ou responsável da tarefa. |
| **19** | `concluir_tarefa_thehive` | Marca uma tarefa de investigação como concluída. |
| **20** | `atribuir_tarefa_thehive` | Define o responsável por uma tarefa no TheHive. |
| **21** | `remover_tarefa_thehive` | Exclui uma tarefa do TheHive. |
| **22** | `criar_tasklog_thehive` | Cria um registro detalhado de log em uma tarefa. |
| **23** | `adicionar_log_tarefa_thehive` | Adiciona uma entrada de log a uma tarefa. |

---

### 🔍 3. Observáveis e Evidências IOC (7 Tools)

| Nº | Ferramenta MCP | Descrição Operacional |
| :---: | :--- | :--- |
| **24** | `adicionar_observavel_thehive` | Registra um IOC (IP, Hash, Domínio, URL) em um caso. |
| **25** | `obter_observaveis_thehive` | Lista todas as evidências e IOCs anexados a um caso. |
| **26** | `criar_observavel_arquivo_thehive` | Faz upload ou registra um observável do tipo arquivo. |
| **27** | `atualizar_observavel_thehive` | Atualiza IOC, tags, TLP, PAP ou flags de um observável. |
| **28** | `deletar_observavel_thehive` | Remove um observável do TheHive. |
| **29** | `marcar_observavel_ioc_thehive` | Marca ou desmarca um observável como IOC relevante. |
| **30** | `marcar_observavel_sighted_thehive` | Marca um observável como visto (Sighted) na infraestrutura. |

---

### 🚨 4. Alertas de Segurança (9 Tools)

| Nº | Ferramenta MCP | Descrição Operacional |
| :---: | :--- | :--- |
| **31** | `obter_alertas_thehive` | Lista ou obtém detalhes de alertas no TheHive. |
| **32** | `criar_alerta_thehive` | Cria um novo alerta de segurança no TheHive. |
| **33** | `obter_alerta_thehive` | Obtém detalhes completos de um alerta específico pelo ID. |
| **34** | `atualizar_alerta_thehive` | Atualiza título, descrição, tags ou status de um alerta. |
| **35** | `deletar_alerta_thehive` | Remove um alerta do TheHive pelo ID. |
| **36** | `promover_alerta_para_caso_thehive` | Converte/Promove um alerta do TheHive em um caso de incidente. |
| **37** | `mesclar_alertas_thehive` | Mescla alertas relacionados dentro de um caso existente. |
| **38** | `buscar_alertas_thehive` | Pesquisa alertas no TheHive por filtros ou termos. |
| **39** | `excluir_alertas_duplicados_thehive` | Identifica e exclui automaticamente todos os alertas duplicados em alta velocidade. |

---

### ⚡ 5. Analisadores e Responders do Cortex (10 Tools)

| Nº | Ferramenta MCP | Descrição Operacional |
| :---: | :--- | :--- |
| **40** | `listar_analyzers_cortex` | Lista analisadores disponíveis (VirusTotal, Shodan, etc.). |
| **41** | `listar_analisadores_cortex` | Alias para listagem de motores de análise disponíveis. |
| **42** | `executar_analyzer_cortex` | Executa um analisador do Cortex em um observável e aguarda relatório. |
| **43** | `executar_analise_cortex` | Submete observável para análise automatizada no Cortex. |
| **44** | `listar_jobs_analyzer` | Lista jobs de análise em andamento ou concluídos no Cortex. |
| **45** | `listar_jobs_cortex` | Lista histórico de execuções de jobs no Cortex. |
| **46** | `obter_resultado_analyzer` | Obtém o relatório/resultado final de um job de análise. |
| **47** | `cancelar_job_cortex` | Cancela um job de análise em execução no Cortex. |
| **48** | `listar_responders_cortex` | Lista os responders de resposta ativa disponíveis. |
| **49** | `executar_responder_cortex` | Executa uma ação de resposta ativa no Cortex. |

---

### 🛡️ 6. Sincronização CTI com MISP (6 Tools)

| Nº | Ferramenta MCP | Descrição Operacional |
| :---: | :--- | :--- |
| **50** | `buscar_evento_misp` | Pesquisa eventos e IOCs na inteligência de ameaças do MISP. |
| **51** | `buscar_misp` | Consulta genérica de IOC no MISP. |
| **52** | `importar_evento_misp` | Importa os detalhes de um evento do MISP para investigação. |
| **53** | `exportar_caso_misp` | Exporta e cria um evento de ameaça no MISP com base no caso. |
| **54** | `publicar_evento_misp` | Publica um novo evento no MISP. |
| **55** | `sincronizar_iocs_misp` | Sincroniza observáveis do caso com a base CTI do MISP. |

---

### 🏛️ 7. Templates, Organizações, Usuários, Taxonomias e Campos (10 Tools)

| Nº | Ferramenta MCP | Descrição Operacional |
| :---: | :--- | :--- |
| **56** | `listar_case_templates_thehive` | Lista os modelos/templates de casos cadastrados no TheHive. |
| **57** | `criar_caso_template_thehive` | Cria um caso baseado em um template pré-definido. |
| **58** | `listar_organizacoes_thehive` | Lista as organizações cadastradas na instância do TheHive. |
| **59** | `listar_usuarios_thehive` | Lista os usuários registrados no TheHive. |
| **60** | `listar_tags_thehive` | Lista todas as tags existentes usadas em casos e alertas. |
| **61** | `listar_taxonomias_thehive` | Lista as taxonomias disponíveis no TheHive. |
| **62** | `adicionar_taxonomia_caso_thehive` | Adiciona uma taxonomia (ex: veredito, categoria) a um caso. |
| **63** | `listar_custom_fields_thehive` | Lista os campos personalizados (Custom Fields) definidos. |
| **64** | `atualizar_custom_field_thehive` | Atualiza o valor de um campo personalizado em um caso. |
| **65** | `buscar_similares_thehive` | Busca casos semelhantes que compartilham dos mesmos IOCs. |

---

### 📊 8. Estatísticas, Exportação, Importação e Diagnóstico (5 Tools)

| Nº | Ferramenta MCP | Descrição Operacional |
| :---: | :--- | :--- |
| **66** | `exportar_caso_thehive` | Exporta um caso completo com observáveis e tarefas em JSON. |
| **67** | `importar_caso_thehive` | Importa um caso a partir de uma estrutura JSON. |
| **68** | `estatisticas_thehive` | Exibe estatísticas (casos abertos, fechados, severidades). |
| **69** | `healthcheck_thehive` | Verifica a saúde e conectividade com a API do TheHive. |
| **70** | `versao_thehive` | Retorna as informações de versão do servidor TheHive. |

---

## 📦 Instalação e Configuração

```bash
git clone https://github.com/nks1097/TheHive-MCP-Server.git
cd TheHive-MCP-Server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python start_mcp.py
```
### Configurar as variaveis de ambiente

Edite o arquivo .env com os dados da sua infraestrutura:

```env
# TheHive Credenciais
THEHIVE_URL=ALTERE_SUA_URL
THEHIVE_API_KEY=ALTERE_SUA_API_KEY

# Cortex Credenciais (se no caso vc precisar usar)
CORTEX_URL=ALTERE_SUA_URL
CORTEX_API_KEY=ALTERE_SUA_API_KEY

# MISP Credentials (se no caso vc precisar usar)
MISP_URL=ALTERE_SUA_URL
MISP_API_KEY=ALTERE_SUA_API_KEY
MISP_VERIFY_SSL=false

# SSH para o Docker Host (for TheHive, Cortex, MISP) (se no caso vc precisar usar)
DOCKER_HOST_SSH_IP=ALTERE_SUA_URL
DOCKER_HOST_SSH_PORT=22
DOCKER_HOST_SSH_USER=ALTERE_SEU_USUARIO
DOCKER_HOST_SSH_PASS=ALTERE_SUA_SENHA

# App Settings
LOG_LEVEL=INFO
FAST_MCP_NAME=TheHive-MCP-Server
FAST_MCP_PORT=9000
```
* Exemplo das configuraçoes do arquivo .env

   ![.env](docs/imagens/1.png)
  
---

## 🔌 Antigravity IDE (`mcp_config.json`)

Adicione ao arquivo `C:\Users\<SeuUsuario>\.gemini\config\mcp_config.json`:

```json
{
  "mcpServers": {
    "soc-mcp-server": {
      "command": "C:\\Caminho\\Para\\TheHive-MCP-Server\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Caminho\\Para\\TheHive-MCP-Server\\start_mcp.py"
      ],
      "env": {
        "FASTMCP_LOG_LEVEL": "CRITICAL",
        "FASTMCP_SHOW_SERVER_BANNER": "false",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

   * imagem de Exemplo de configuração mcp_config.json para o Antigravity IDE

   ![Configuração mcp_config.json na Antigravity IDE](docs/imagens/config_antigravity_json.png)

### LM Studio / Claude Desktop

```json
{
  "mcpServers": {
    "soc-mcp-server": {
      "command": "C:\\Caminho\\Para\\TheHive-MCP-Server\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Caminho\\Para\\TheHive-MCP-Server\\start_mcp.py"
      ]
    }
  }
}
```

* imagem de Exemplo de configuração mcp_config.json para o LM Studio
   
   ![Configuração mcpServers no LM Studio](docs/imagens/2.png)

### ChatGPT Codex

Adicione ao arquivo `C:\Users\<SeuUsuario>\.codex\config.toml`:

```json
[mcp_servers.soc-ai]
command = "C:\\Caminho\\Para\\TheHive-MCP-Server\\.venv\\Scripts\\python.exe"
args = [
  "C:\\Caminho\\Para\\TheHive-MCP-Server\\start_mcp.py",
]

```

* imagem de Exemplo de configuração mcp_config.json para o codex
   
   ![Configuração config.toml no ChatGPT Codex](docs/imagens/3.png)

---
### VIDEO DE CONFIGURAÇÃO DE FORMA SIMPLIFICADA USANDO GRATUITAMENTE LLM LOCAL COM LM STUDIO

 ▶️ **[Clique aqui para assistir ao vídeo completo no Google Drive Assiste em Full Hd (1080P)](https://drive.google.com/file/d/1oq8Xt84Gb8irlTWp1CeNMNZEGyv1a59w/view?usp=drive_link)**

---

## 📜 Licença

Distribuído sob a licença **Apache 2.0**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📂 Estrutura do Projeto

```text
TheHive-MCP-Server/
├── src/
│   ├── config/
│   │   └── settings.py          # Configurações globais e variáveis de ambiente
│   ├── core/
│   │   └── http_client.py       # Cliente HTTP assíncrono (httpx) com tratamento de erros
│   ├── integrations/
│   │   ├── cortex/
│   │   │   └── client.py        # Cliente de integração com Cortex (Analyzers/Responders/Jobs)
│   │   ├── misp/
│   │   │   └── client.py        # Cliente de integração com MISP CTI
│   │   └── thehive/
│   │       └── client.py        # Cliente completo da API REST do TheHive 5
│   ├── tools/
│   │   ├── server.py            # Instanciação da aplicação FastMCP (TheHive-MCP-Server)
│   │   └── thehive_tools.py     # Registro decorado de todas as 70 ferramentas MCP
│   ├── utils/
│   │   └── logger.py            # Logger estruturado Loguru
│   └── main.py                  # Ponto de entrada do servidor FastMCP
├── logs/                        # Logs de execução da aplicação
├── .env.example                 # Modelo de variáveis de ambiente com dados sanitizados
├── .gitignore                   # Regras de exclusão do Git
├── LICENSE                      # Licença de uso Apache 2.0
├── README.md                    # Documentação técnica oficial e catálogo de ferramentas
├── pyproject.toml               # Metadados do projeto Python
├── requirements.txt             # Dependências diretas do projeto
└── start_mcp.py                 # Script de inicialização stdio para clientes MCP
```
