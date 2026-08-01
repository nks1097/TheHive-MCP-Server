from typing import Dict, Any, List, Optional
from src.tools.server import mcp
from src.integrations.thehive.client import TheHiveClient
from src.integrations.cortex.client import CortexClient
from src.integrations.misp.client import MISPClient

_hive_client: Optional[TheHiveClient] = None
_cortex_client: Optional[CortexClient] = None
_misp_client: Optional[MISPClient] = None

def get_thehive() -> TheHiveClient:
    global _hive_client
    if _hive_client is None:
        _hive_client = TheHiveClient()
    return _hive_client

def get_cortex() -> CortexClient:
    global _cortex_client
    if _cortex_client is None:
        _cortex_client = CortexClient()
    return _cortex_client

def get_misp() -> MISPClient:
    global _misp_client
    if _misp_client is None:
        _misp_client = MISPClient()
    return _misp_client


# ==========================================
# 1. FERRAMENTAS DE CASOS (THEHIVE CASES)
# ==========================================

@mcp.tool()
async def criar_caso_thehive(title: str, description: str, severity: int = 2, tags: List[str] = None, tlp: int = 2, pap: int = 2) -> Dict[str, Any]:
    """Cria um novo caso de incidente de segurança no TheHive."""
    client = get_thehive()
    return await client.create_case(title=title, description=description, severity=severity, tags=tags, tlp=tlp, pap=pap)

@mcp.tool()
async def listar_casos_thehive(limit: int = 10) -> List[Dict[str, Any]]:
    """Lista os casos de incidentes mais recentes no TheHive."""
    client = get_thehive()
    return await client.list_cases(limit=limit)

@mcp.tool()
async def obter_caso_thehive(case_id: str) -> Dict[str, Any]:
    """Obtém detalhes completos de um caso de incidente no TheHive pelo ID."""
    client = get_thehive()
    return await client.get_case(case_id=case_id)

@mcp.tool()
async def atualizar_caso_thehive(case_id: str, description: str = None, severity: int = None, status: str = None, resolution_status: str = None, owner: str = None) -> Dict[str, Any]:
    """Atualiza propriedades (descrição, severidade, status, resolução, responsável) de um caso no TheHive."""
    client = get_thehive()
    kwargs = {}
    if description is not None:
        kwargs["description"] = description
    if severity is not None:
        kwargs["severity"] = severity
    if status is not None:
        kwargs["status"] = status
    if resolution_status is not None:
        kwargs["resolutionStatus"] = resolution_status
    if owner is not None:
        kwargs["owner"] = owner
    return await client.update_case(case_id=case_id, **kwargs)

@mcp.tool()
async def deletar_caso_thehive(case_id: str) -> Dict[str, Any]:
    """Exclui um caso de incidente do TheHive."""
    client = get_thehive()
    return await client.delete_case(case_id=case_id)

@mcp.tool()
async def fechar_caso_thehive(case_id: str, resolution_status: str = "TruePositive") -> Dict[str, Any]:
    """Fecha um caso com resolução (TruePositive, FalsePositive, Indeterminate)."""
    client = get_thehive()
    return await client.update_case_status(case_id, status="Resolved", resolution_status=resolution_status)

@mcp.tool()
async def reabrir_caso_thehive(case_id: str) -> Dict[str, Any]:
    """Reabre um caso encerrado no TheHive."""
    client = get_thehive()
    return await client.update_case_status(case_id, status="Open")

@mcp.tool()
async def atribuir_caso_thehive(case_id: str, owner: str) -> Dict[str, Any]:
    """Atribui um responsável (usuário) a um caso no TheHive."""
    client = get_thehive()
    return await client.assign_case(case_id=case_id, owner=owner)

@mcp.tool()
async def adicionar_tag_caso_thehive(case_id: str, tags: List[str]) -> Dict[str, Any]:
    """Adiciona tags a um caso no TheHive."""
    client = get_thehive()
    return await client.add_case_tag(case_id=case_id, tags=tags)

@mcp.tool()
async def remover_tag_caso_thehive(case_id: str, tags: List[str]) -> Dict[str, Any]:
    """Remove tags de um caso no TheHive."""
    client = get_thehive()
    return await client.remove_case_tag(case_id=case_id, tags=tags)

@mcp.tool()
async def obter_timeline_caso_thehive(case_id: str) -> List[Dict[str, Any]]:
    """Recupera o histórico/linha do tempo completa de eventos de um caso no TheHive."""
    client = get_thehive()
    return await client.get_case_timeline(case_id=case_id)

@mcp.tool()
async def listar_logs_caso_thehive(case_id: str) -> List[Dict[str, Any]]:
    """Lista logs de auditoria e atividades registradas em um caso no TheHive."""
    client = get_thehive()
    return await client.list_case_logs(case_id=case_id)

@mcp.tool()
async def buscar_casos_thehive(query: str = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Pesquisa casos por qualquer termo (título, descrição, status, severidade, tag)."""
    client = get_thehive()
    return await client.search_cases(query=query, limit=limit)

@mcp.tool()
async def adicionar_comentario_caso_thehive(case_id: str, message: str) -> Dict[str, Any]:
    """Adiciona um comentário técnico na aba de investigação de um caso no TheHive."""
    client = get_thehive()
    return await client.add_case_comment(case_id=case_id, message=message)

@mcp.tool()
async def buscar_casos_duplicados_thehive(title: str, rule_id: str = None, hours_window: int = 24) -> Optional[Dict[str, Any]]:
    """Verifica se existe um caso idêntico ou relacionado criado/atualizado nas últimas N horas."""
    client = get_thehive()
    return await client.find_duplicate_case(title=title, rule_id=rule_id, hours_window=hours_window)


# ==========================================
# 2. FERRAMENTAS DE TAREFAS (THEHIVE TASKS)
# ==========================================

@mcp.tool()
async def obter_tarefas_thehive(task_id: str = None, case_id: str = None, limit: int = 10) -> Any:
    """Busca tarefas do TheHive. Se task_id for informado, retorna a tarefa. Se case_id for informado, retorna as tarefas daquele caso. Caso contrário, lista as tarefas recentes."""
    client = get_thehive()
    if task_id:
        return await client.get_task(task_id)
    elif case_id:
        return await client.get_case_tasks(case_id)
    return await client.list_tasks(limit=limit)

@mcp.tool()
async def criar_tarefa_thehive(case_id: str, title: str, description: str = "", status: str = "Waiting") -> Dict[str, Any]:
    """Cria uma nova tarefa dentro de um caso do TheHive."""
    client = get_thehive()
    return await client.create_task(case_id=case_id, title=title, description=description, status=status)

@mcp.tool()
async def atualizar_tarefa_thehive(task_id: str, title: str = None, description: str = None, status: str = None, owner: str = None) -> Dict[str, Any]:
    """Atualiza título, descrição, status ou responsável de uma tarefa."""
    client = get_thehive()
    kwargs = {}
    if title: kwargs["title"] = title
    if description: kwargs["description"] = description
    if status: kwargs["status"] = status
    if owner: kwargs["owner"] = owner
    return await client.update_task(task_id, **kwargs)

@mcp.tool()
async def concluir_tarefa_thehive(task_id: str) -> Dict[str, Any]:
    """Marca uma tarefa de investigação no TheHive como concluída."""
    client = get_thehive()
    return await client.complete_task(task_id)

@mcp.tool()
async def atribuir_tarefa_thehive(task_id: str, owner: str) -> Dict[str, Any]:
    """Define o responsável por uma tarefa no TheHive."""
    client = get_thehive()
    return await client.assign_task(task_id, owner=owner)

@mcp.tool()
async def remover_tarefa_thehive(task_id: str) -> Dict[str, Any]:
    """Exclui uma tarefa do TheHive."""
    client = get_thehive()
    return await client.delete_task(task_id)

@mcp.tool()
async def criar_tasklog_thehive(task_id: str, message: str) -> Dict[str, Any]:
    """Cria um registro detalhado de log em uma tarefa do TheHive."""
    client = get_thehive()
    return await client.add_task_log(task_id=task_id, message=message)

@mcp.tool()
async def adicionar_log_tarefa_thehive(task_id: str, message: str) -> Dict[str, Any]:
    """Adiciona uma entrada de log a uma tarefa do TheHive."""
    client = get_thehive()
    return await client.add_task_log(task_id=task_id, message=message)


# ==========================================
# 3. FERRAMENTAS DE OBSERVÁVEIS (IOCs)
# ==========================================

@mcp.tool()
async def adicionar_observavel_thehive(case_id: str, data_type: str, data: str, tags: List[str] = None, tlp: int = 2, pap: int = 2, ioc: bool = True) -> Dict[str, Any]:
    """Adiciona um observável (IOC: IP, Hash, Domínio, URL) a um caso no TheHive."""
    client = get_thehive()
    return await client.add_observable(case_id=case_id, data_type=data_type, data=data, tags=tags, tlp=tlp, pap=pap, ioc=ioc)

@mcp.tool()
async def obter_observaveis_thehive(case_id: str) -> List[Dict[str, Any]]:
    """Obtém todos os observáveis e evidências anexadas a um caso no TheHive."""
    client = get_thehive()
    return await client.get_observables(case_id=case_id)

@mcp.tool()
async def criar_observavel_arquivo_thehive(case_id: str, file_path_or_name: str, data_type: str = "file") -> Dict[str, Any]:
    """Cria um observável do tipo arquivo em um caso."""
    client = get_thehive()
    return await client.add_observable(case_id=case_id, data_type=data_type, data=file_path_or_name)

@mcp.tool()
async def atualizar_observavel_thehive(obs_id: str, tags: List[str] = None, tlp: int = None, pap: int = None, ioc: bool = None) -> Dict[str, Any]:
    """Atualiza IOC, tags, TLP, PAP ou flags de um observável."""
    client = get_thehive()
    kwargs = {}
    if tags is not None: kwargs["tags"] = tags
    if tlp is not None: kwargs["tlp"] = tlp
    if pap is not None: kwargs["pap"] = pap
    if ioc is not None: kwargs["ioc"] = ioc
    return await client.update_observable(obs_id, **kwargs)

@mcp.tool()
async def deletar_observavel_thehive(obs_id: str) -> Dict[str, Any]:
    """Remove um observável do TheHive."""
    client = get_thehive()
    return await client.delete_observable(obs_id)

@mcp.tool()
async def marcar_observavel_ioc_thehive(obs_id: str, is_ioc: bool = True) -> Dict[str, Any]:
    """Marca ou desmarca um observável como IOC relevante."""
    client = get_thehive()
    return await client.toggle_observable_ioc(obs_id, is_ioc=is_ioc)

@mcp.tool()
async def marcar_observavel_sighted_thehive(obs_id: str, sighted: bool = True) -> Dict[str, Any]:
    """Marca um observável como visto (Sighted) na infraestrutura."""
    client = get_thehive()
    return await client.mark_observable_sighted(obs_id, sighted=sighted)


# ==========================================
# 4. FERRAMENTAS DE ALERTAS (THEHIVE ALERTS)
# ==========================================

@mcp.tool()
async def obter_alertas_thehive(alert_id: str = None, limit: int = 10) -> Any:
    """Busca alertas do TheHive. Se alert_id for informado, retorna detalhes do alerta específico, caso contrário lista os mais recentes."""
    client = get_thehive()
    if alert_id:
        return await client.get_alert(alert_id)
    return await client.list_alerts(limit=limit)

@mcp.tool()
async def criar_alerta_thehive(title: str, description: str, type: str = "security_alert", source: str = "mcp", sourceRef: str = "1", severity: int = 2, tags: List[str] = None) -> Dict[str, Any]:
    """Cria um novo alerta de segurança no TheHive."""
    client = get_thehive()
    return await client.create_alert(title=title, description=description, type=type, source=source, sourceRef=sourceRef, severity=severity, tags=tags)

@mcp.tool()
async def obter_alerta_thehive(alert_id: str) -> Dict[str, Any]:
    """Obtém detalhes completos de um alerta específico no TheHive pelo ID."""
    client = get_thehive()
    return await client.get_alert(alert_id)

@mcp.tool()
async def atualizar_alerta_thehive(alert_id: str, title: str = None, description: str = None, status: str = None, tags: List[str] = None) -> Dict[str, Any]:
    """Atualiza título, descrição, tags ou status de um alerta no TheHive."""
    client = get_thehive()
    kwargs = {}
    if title: kwargs["title"] = title
    if description: kwargs["description"] = description
    if status: kwargs["status"] = status
    if tags: kwargs["tags"] = tags
    return await client.update_alert(alert_id, **kwargs)

@mcp.tool()
async def deletar_alerta_thehive(alert_id: str) -> Dict[str, Any]:
    """Remove um alerta do TheHive pelo ID."""
    client = get_thehive()
    return await client.delete_alert(alert_id)

@mcp.tool()
async def promover_alerta_para_caso_thehive(alert_id: str, case_template: str = None) -> Dict[str, Any]:
    """Converte/Promove um alerta do TheHive em um caso de incidente."""
    client = get_thehive()
    return await client.promote_alert_to_case(alert_id, case_template=case_template)

@mcp.tool()
async def mesclar_alertas_thehive(case_id: str, alert_ids: List[str]) -> Dict[str, Any]:
    """Mescla alertas relacionados dentro de um caso existente no TheHive."""
    client = get_thehive()
    return await client.merge_alerts(case_id, alert_ids)

@mcp.tool()
async def buscar_alertas_thehive(query: str = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Pesquisa alertas no TheHive por filtros ou termos."""
    client = get_thehive()
    return await client.search_alerts(query=query, limit=limit)

@mcp.tool()
async def excluir_alertas_duplicados_thehive(batch_size: int = 50) -> Dict[str, Any]:
    """Identifica e exclui automaticamente todos os alertas duplicados no TheHive em alta velocidade."""
    client = get_thehive()
    return await client.deduplicate_alerts(batch_size=batch_size)


# ==========================================
# 5. FERRAMENTAS CORTEX (ANALYZERS & RESPONDERS)
# ==========================================

@mcp.tool()
async def listar_analyzers_cortex() -> List[Dict[str, Any]]:
    """Lista todos os analisadores (VirusTotal, Shodan, etc.) disponíveis no Cortex."""
    client = get_cortex()
    return await client.list_analyzers()

@mcp.tool()
async def listar_analisadores_cortex() -> List[Dict[str, Any]]:
    """Lista todos os motores de análise disponíveis no Cortex."""
    client = get_cortex()
    return await client.list_analyzers()

@mcp.tool()
async def executar_analyzer_cortex(analyzer_id: str, data_type: str, data: str) -> Dict[str, Any]:
    """Executa um analisador do Cortex em um observável e aguarda o resultado."""
    client = get_cortex()
    job = await client.run_analyzer(analyzer_id, data_type, data)
    job_id = job.get("id")
    if job_id:
        return await client.wait_for_job(job_id)
    return job

@mcp.tool()
async def executar_analise_cortex(analyzer_id: str, data_type: str, data: str) -> Dict[str, Any]:
    """Executa um analisador do Cortex em um observável."""
    return await executar_analyzer_cortex(analyzer_id, data_type, data)

@mcp.tool()
async def listar_jobs_analyzer(limit: int = 20) -> List[Dict[str, Any]]:
    """Lista os jobs de análise em andamento ou concluídos no Cortex."""
    client = get_cortex()
    return await client.list_jobs(limit=limit)

@mcp.tool()
async def listar_jobs_cortex(limit: int = 20) -> List[Dict[str, Any]]:
    """Lista os jobs de análise no Cortex."""
    client = get_cortex()
    return await client.list_jobs(limit=limit)

@mcp.tool()
async def obter_resultado_analyzer(job_id: str) -> Dict[str, Any]:
    """Obtém o relatório/resultado final de um job de análise do Cortex."""
    client = get_cortex()
    return await client.get_job_report(job_id)

@mcp.tool()
async def cancelar_job_cortex(job_id: str) -> Dict[str, Any]:
    """Cancela um job de análise em execução no Cortex."""
    client = get_cortex()
    return await client.cancel_job(job_id)

@mcp.tool()
async def listar_responders_cortex() -> List[Dict[str, Any]]:
    """Lista os responders atômicos de resposta ativa disponíveis no Cortex."""
    client = get_cortex()
    return await client.list_responders()

@mcp.tool()
async def executar_responder_cortex(responder_id: str, data_type: str, data: str) -> Dict[str, Any]:
    """Executa uma ação de resposta ativa (responder) no Cortex."""
    client = get_cortex()
    return await client.run_responder(responder_id, data_type, data)


# ==========================================
# 6. FERRAMENTAS MISP (CTI & SYNCHRONIZATION)
# ==========================================

@mcp.tool()
async def buscar_evento_misp(value: str) -> List[Dict[str, Any]]:
    """Pesquisa eventos e indicadores de comprometimento (IOCs) na base CTI do MISP."""
    client = get_misp()
    return await client.search_events(value)

@mcp.tool()
async def buscar_misp(value: str) -> List[Dict[str, Any]]:
    """Consulta um IOC na inteligência de ameaças do MISP."""
    client = get_misp()
    return await client.search_events(value)

@mcp.tool()
async def importar_evento_misp(event_id: str) -> Dict[str, Any]:
    """Importa os detalhes de um evento do MISP para o ambiente de investigação."""
    client = get_misp()
    return await client.get_event(event_id)

@mcp.tool()
async def exportar_caso_misp(info: str) -> Dict[str, Any]:
    """Exporta e cria um evento de ameaça no MISP com base nos dados do caso."""
    client = get_misp()
    return await client.add_event(info=info)

@mcp.tool()
async def publicar_evento_misp(info: str) -> Dict[str, Any]:
    """Publica um evento no MISP."""
    client = get_misp()
    return await client.add_event(info=info)

@mcp.tool()
async def sincronizar_iocs_misp(case_id: str) -> Dict[str, Any]:
    """Sincroniza os observáveis de um caso do TheHive com a base de inteligência do MISP."""
    hive = get_thehive()
    misp = get_misp()
    observables = await hive.get_observables(case_id)
    synced = []
    for obs in observables:
        res = await misp.search_events(obs.get("data", ""))
        synced.append({"observable": obs.get("data"), "misp_hits": len(res)})
    return {"status": "success", "case_id": case_id, "synced_iocs": synced}


# ==========================================
# 7. TEMPLATES, ORGANIZAÇÕES, TAGS & CAMPOS
# ==========================================

@mcp.tool()
async def listar_case_templates_thehive() -> List[Dict[str, Any]]:
    """Lista todos os modelos/templates de casos cadastrados no TheHive."""
    client = get_thehive()
    return await client.list_case_templates()

@mcp.tool()
async def criar_caso_template_thehive(title: str, template_name: str, description: str = "") -> Dict[str, Any]:
    """Cria um novo caso de incidente baseado em um template pré-definido."""
    client = get_thehive()
    return await client.create_case_from_template(title=title, template_name=template_name, description=description)

@mcp.tool()
async def listar_organizacoes_thehive() -> List[Dict[str, Any]]:
    """Lista as organizações cadastradas na instância do TheHive."""
    client = get_thehive()
    return await client.list_organisations()

@mcp.tool()
async def listar_usuarios_thehive() -> List[Dict[str, Any]]:
    """Lista todos os usuários registrados no TheHive."""
    client = get_thehive()
    return await client.list_users()

@mcp.tool()
async def listar_tags_thehive() -> List[str]:
    """Lista todas as tags existentes usadas em casos e alertas."""
    client = get_thehive()
    return await client.list_tags()

@mcp.tool()
async def listar_taxonomias_thehive() -> List[Dict[str, Any]]:
    """Lista as taxonomias disponíveis no TheHive."""
    client = get_thehive()
    return await client.list_taxonomies()

@mcp.tool()
async def adicionar_taxonomia_caso_thehive(case_id: str, taxonomy: str, value: str) -> Dict[str, Any]:
    """Adiciona uma taxonomia (ex: veredito, categoria) a um caso no TheHive."""
    client = get_thehive()
    return await client.add_case_taxonomy(case_id=case_id, taxonomy=taxonomy, value=value)

@mcp.tool()
async def listar_custom_fields_thehive() -> List[Dict[str, Any]]:
    """Lista os campos personalizados (Custom Fields) definidos no TheHive."""
    client = get_thehive()
    return await client.list_custom_fields()

@mcp.tool()
async def atualizar_custom_field_thehive(case_id: str, field_name: str, value: Any) -> Dict[str, Any]:
    """Atualiza o valor de um campo personalizado (Custom Field) em um caso."""
    client = get_thehive()
    return await client.update_custom_field(case_id=case_id, field_name=field_name, value=value)

@mcp.tool()
async def buscar_similares_thehive(case_id: str) -> List[Dict[str, Any]]:
    """Busca casos semelhantes que compartilham dos mesmos observáveis/IOCs."""
    client = get_thehive()
    return await client.find_similar_cases(case_id)


# ==========================================
# 8. ESTATÍSTICAS, EXPORTAÇÃO E SISTEMA
# ==========================================

@mcp.tool()
async def exportar_caso_thehive(case_id: str) -> Dict[str, Any]:
    """Exporta um caso completo com observáveis e tarefas em formato JSON."""
    client = get_thehive()
    return await client.export_case(case_id)

@mcp.tool()
async def importar_caso_thehive(case_data: Dict[str, Any]) -> Dict[str, Any]:
    """Importa um caso a partir de uma estrutura JSON."""
    client = get_thehive()
    return await client.import_case(case_data)

@mcp.tool()
async def estatisticas_thehive() -> Dict[str, Any]:
    """Exibe estatísticas gerais da plataforma (casos abertos, fechados, severidades)."""
    client = get_thehive()
    return await client.get_case_statistics()

@mcp.tool()
async def healthcheck_thehive() -> Dict[str, Any]:
    """Verifica o status da conexão e saúde da API do TheHive."""
    client = get_thehive()
    return await client.healthcheck()

@mcp.tool()
async def versao_thehive() -> Dict[str, Any]:
    """Retorna as informações de versão do servidor TheHive."""
    client = get_thehive()
    return await client.get_version()
