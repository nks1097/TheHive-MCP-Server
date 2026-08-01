from typing import Dict, Any, List, Optional
from src.core.http_client import AsyncHttpClient
from src.config.settings import settings
from src.utils.logger import logger

class TheHiveClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.THEHIVE_API_KEY}",
            "Content-Type": "application/json"
        }
        self.client = AsyncHttpClient(settings.THEHIVE_URL, headers=self.headers, verify=False)

    # --- CASES ---

    async def list_cases(self, limit: int = 10, full_details: bool = False) -> List[Dict[str, Any]]:
        """List cases from TheHive ordered by creation date."""
        response = await self.client.get(f"/api/case?sort=-createdAt&limit={limit}")
        logger.info(f"Fetched {len(response)} cases from TheHive")
        if full_details or not isinstance(response, list):
            return response

        clean_list = []
        for c in response:
            clean_case = {
                "_id": c.get("_id"),
                "caseId": c.get("caseId"),
                "title": c.get("title"),
                "severity": c.get("severity"),
                "status": c.get("status"),
                "stage": c.get("stage"),
                "owner": c.get("owner"),
                "createdAt": c.get("createdAt"),
                "tags": c.get("tags", []),
                "summary": c.get("summary") or (c.get("description", "")[:120] + "..." if c.get("description") else "")
            }
            clean_list.append(clean_case)
        return clean_list

    async def create_case(self, title: str, description: str, severity: int = 2, tags: List[str] = None, tlp: int = 2, pap: int = 2) -> Dict[str, Any]:
        """Create a new security incident case in TheHive."""
        payload = {
            "title": title,
            "description": description,
            "severity": severity,
            "tags": tags or [],
            "tlp": tlp,
            "pap": pap
        }
        response = await self.client.post("/api/case", json=payload)
        logger.info(f"Created TheHive case: {response.get('caseId')}")
        return response

    async def get_case(self, case_id: str) -> Dict[str, Any]:
        """Get details of a specific case in TheHive."""
        response = await self.client.get(f"/api/case/{case_id}")
        return response

    async def update_case_status(self, case_id: str, status: str, resolution_status: Optional[str] = None) -> Dict[str, Any]:
        """Update case status (e.g., 'Resolved', 'Open') and optionally resolution status."""
        payload = {"status": status}
        if resolution_status:
            payload["resolutionStatus"] = resolution_status
            
        response = await self.client.patch(f"/api/case/{case_id}", json=payload)
        logger.info(f"Updated case {case_id} status to {status}")
        return response

    async def update_case(self, case_id: str, **kwargs) -> Dict[str, Any]:
        """Update case properties (e.g., description, title, severity, tags, status, owner)."""
        response = await self.client.patch(f"/api/case/{case_id}", json=kwargs)
        logger.info(f"Updated case {case_id} with keys: {list(kwargs.keys())}")
        return response

    async def delete_case(self, case_id: str) -> Dict[str, Any]:
        """Delete a case from TheHive."""
        response = await self.client.delete(f"/api/case/{case_id}")
        logger.info(f"Deleted case {case_id} from TheHive")
        return response

    async def search_cases(self, query: str = None, status: str = None, severity: int = None, tag: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Search cases by query filters."""
        query_body = {"query": [{"_name": "listCase"}]}
        if query:
            query_body = {"query": [{"_name": "listCase"}, {"_name": "filter", "_expr": {"_contains": {"_field": "title", "_value": query}}}]}
        try:
            res = await self.client.post("/api/v1/query", json=query_body)
            return res[:limit] if isinstance(res, list) else []
        except Exception:
            return await self.list_cases(limit=limit)

    async def assign_case(self, case_id: str, owner: str) -> Dict[str, Any]:
        """Assign an owner to a case."""
        return await self.update_case(case_id, owner=owner)

    async def add_case_tag(self, case_id: str, tags: List[str]) -> Dict[str, Any]:
        """Add tags to a case."""
        case = await self.get_case(case_id)
        current_tags = case.get("tags", [])
        new_tags = list(set(current_tags + tags))
        return await self.update_case(case_id, tags=new_tags)

    async def remove_case_tag(self, case_id: str, tags: List[str]) -> Dict[str, Any]:
        """Remove tags from a case."""
        case = await self.get_case(case_id)
        current_tags = case.get("tags", [])
        new_tags = [t for t in current_tags if t not in tags]
        return await self.update_case(case_id, tags=new_tags)

    async def get_case_timeline(self, case_id: str) -> List[Dict[str, Any]]:
        """Get timeline / history stream of a case."""
        query_body = {
            "query": [
                {"_name": "getCase", "idOrName": case_id},
                {"_name": "timeline"}
            ]
        }
        try:
            return await self.client.post("/api/v1/query", json=query_body)
        except Exception:
            return await self.client.get(f"/api/case/{case_id}/timeline")

    async def list_case_logs(self, case_id: str) -> List[Dict[str, Any]]:
        """List logs and audit entries of a case."""
        return await self.get_case_timeline(case_id)

    async def find_similar_cases(self, case_id: str) -> List[Dict[str, Any]]:
        """Search for similar cases based on observables."""
        response = await self.client.get(f"/api/case/{case_id}/similar")
        return response

    async def export_case(self, case_id: str) -> Dict[str, Any]:
        """Export case data in JSON summary format."""
        case = await self.get_case(case_id)
        observables = await self.get_observables(case_id)
        tasks = await self.get_case_tasks(case_id)
        return {
            "case": case,
            "observables": observables,
            "tasks": tasks
        }

    async def import_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Import a case from JSON data."""
        title = case_data.get("title", "Imported Case")
        description = case_data.get("description", "Imported via MCP")
        severity = case_data.get("severity", 2)
        tags = case_data.get("tags", [])
        return await self.create_case(title, description, severity, tags)

    async def get_case_statistics(self) -> Dict[str, Any]:
        """Get general statistics on cases (open, closed, severity counts)."""
        cases = await self.list_cases(limit=100)
        open_cases = [c for c in cases if c.get("status") in ["Open", "New", "InProgress"]]
        closed_cases = [c for c in cases if c.get("status") in ["Resolved", "Closed"]]
        severities = {}
        for c in cases:
            s = c.get("severity", 0)
            severities[s] = severities.get(s, 0) + 1
        return {
            "total_casos_analisados": len(cases),
            "casos_abertos": len(open_cases),
            "casos_fechados": len(closed_cases),
            "distribuicao_severidade": severities
        }

    # --- ALERTS ---

    async def list_alerts(self, limit: int = 10, full_details: bool = False) -> List[Dict[str, Any]]:
        """List alerts from TheHive."""
        response = await self.client.get(f"/api/alert?sort=-createdAt&limit={limit}")
        logger.info(f"Fetched {len(response)} alerts from TheHive")
        if full_details or not isinstance(response, list):
            return response

        clean_list = []
        for a in response:
            clean_alert = {
                "_id": a.get("_id"),
                "title": a.get("title"),
                "type": a.get("type"),
                "source": a.get("source"),
                "sourceRef": a.get("sourceRef"),
                "severity": a.get("severity"),
                "status": a.get("status"),
                "stage": a.get("stage"),
                "createdAt": a.get("createdAt"),
                "tags": a.get("tags", []),
                "description_snippet": (a.get("description", "")[:120] + "..." if a.get("description") else "")
            }
            clean_list.append(clean_alert)
        return clean_list

    async def get_alert(self, alert_id: str) -> Dict[str, Any]:
        """Get a specific alert from TheHive by ID."""
        response = await self.client.get(f"/api/alert/{alert_id}")
        return response

    async def create_alert(self, title: str, description: str, type: str, source: str, sourceRef: str, severity: int = 2, tags: List[str] = None) -> Dict[str, Any]:
        """Create a new alert in TheHive."""
        payload = {
            "title": title,
            "description": description,
            "type": type,
            "source": source,
            "sourceRef": sourceRef,
            "severity": severity,
            "tags": tags or [],
            "tlp": 2,
            "pap": 2
        }
        response = await self.client.post("/api/alert", json=payload)
        logger.info(f"Created alert: {title}")
        return response

    async def update_alert(self, alert_id: str, **kwargs) -> Dict[str, Any]:
        """Update properties of an alert (title, description, tags, status, etc.)."""
        response = await self.client.patch(f"/api/alert/{alert_id}", json=kwargs)
        logger.info(f"Updated alert {alert_id}")
        return response

    async def delete_alert(self, alert_id: str) -> Dict[str, Any]:
        """Delete an alert from TheHive."""
        response = await self.client.delete(f"/api/alert/{alert_id}")
        logger.info(f"Deleted alert {alert_id}")
        return response

    async def promote_alert_to_case(self, alert_id: str, case_template: Optional[str] = None) -> Dict[str, Any]:
        """Promote an alert into a new case."""
        payload = {}
        if case_template:
            payload["caseTemplate"] = case_template
        response = await self.client.post(f"/api/alert/{alert_id}/createCase", json=payload)
        logger.info(f"Promoted alert {alert_id} to case")
        return response

    async def merge_alerts(self, case_id: str, alert_ids: List[str]) -> Dict[str, Any]:
        """Merge related alerts into an existing case."""
        payload = {"alertIds": alert_ids}
        response = await self.client.post(f"/api/case/{case_id}/alert/merge", json=payload)
        logger.info(f"Merged alerts {alert_ids} into case {case_id}")
        return response

    async def search_alerts(self, query: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Search alerts with filters."""
        alerts = await self.list_alerts(limit=limit)
        if query:
            q = query.lower()
            return [a for a in alerts if q in a.get("title", "").lower() or q in a.get("description", "").lower()]
        return alerts

    async def deduplicate_alerts(self, batch_size: int = 50) -> Dict[str, Any]:
        """Automatically find and delete all duplicate alerts in TheHive at high speed."""
        import asyncio
        try:
            alerts = await self.client.get("/api/alert?range=0-10000&sort=-createdAt")
            if not isinstance(alerts, list):
                alerts = []
        except Exception:
            alerts = await self.list_alerts(limit=100)

        seen = set()
        to_delete = []
        to_keep = []

        for alert in alerts:
            alert_id = alert.get("_id") or alert.get("id")
            title = alert.get("title", "")
            source = alert.get("source", "")
            key = (title, source)

            if key in seen:
                to_delete.append(alert_id)
            else:
                seen.add(key)
                to_keep.append(alert_id)

        deleted_count = 0
        for i in range(0, len(to_delete), batch_size):
            chunk = to_delete[i:i + batch_size]
            tasks = [self.delete_alert(aid) for aid in chunk]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            deleted_count += sum(1 for r in results if not isinstance(r, Exception))

        return {
            "status": "success",
            "total_alertas_analisados": len(alerts),
            "alertas_unicos_mantidos": len(to_keep),
            "alertas_duplicados_excluidos": deleted_count
        }

    # --- TASKS ---

    async def list_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent tasks from TheHive."""
        response = await self.client.get(f"/api/case/task?sort=-createdAt&limit={limit}")
        logger.info(f"Fetched {len(response)} tasks from TheHive")
        return response

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get a specific task from TheHive by ID."""
        response = await self.client.get(f"/api/case/task/{task_id}")
        return response

    async def get_case_tasks(self, case_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a specific case."""
        query_body = {
            "query": [
                {"_name": "getCase", "idOrName": case_id},
                {"_name": "tasks"}
            ]
        }
        response = await self.client.post("/api/v1/query", json=query_body)
        logger.info(f"Fetched tasks for case {case_id} using query API")
        return response

    async def create_task(self, case_id: str, title: str, description: str = "", status: str = "Waiting") -> Dict[str, Any]:
        """Create a task in a case."""
        payload = {
            "title": title,
            "description": description,
            "status": status,
            "flag": False
        }
        response = await self.client.post(f"/api/case/{case_id}/task", json=payload)
        logger.info(f"Created task '{title}' in case {case_id}")
        return response

    async def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Update task status, owner, description, or dates."""
        response = await self.client.patch(f"/api/case/task/{task_id}", json=kwargs)
        logger.info(f"Updated task {task_id}")
        return response

    async def complete_task(self, task_id: str) -> Dict[str, Any]:
        """Mark a task as completed."""
        return await self.update_task(task_id, status="Completed")

    async def assign_task(self, task_id: str, owner: str) -> Dict[str, Any]:
        """Assign owner to a task."""
        return await self.update_task(task_id, owner=owner)

    async def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete/remove a task."""
        response = await self.client.delete(f"/api/case/task/{task_id}")
        logger.info(f"Deleted task {task_id}")
        return response

    async def add_task_log(self, task_id: str, message: str) -> Dict[str, Any]:
        """Add a log entry to a task."""
        payload = {"message": message}
        response = await self.client.post(f"/api/case/task/{task_id}/log", json=payload)
        logger.info(f"Added log to task {task_id}")
        return response

    # --- OBSERVABLES ---

    async def add_observable(self, case_id: str, data_type: str, data: str, tags: List[str] = None, tlp: int = 2, pap: int = 2, ioc: bool = True) -> Dict[str, Any]:
        """Add an observable (IOC: IP, Hash, Domain, URL) to a case in TheHive."""
        payload = {
            "dataType": data_type,
            "data": data,
            "tags": tags or [],
            "tlp": tlp,
            "pap": pap,
            "ioc": ioc
        }
        response = await self.client.post(f"/api/case/{case_id}/artifact", json=payload)
        logger.info(f"Added observable to case {case_id}: {data}")
        return response

    async def get_observables(self, case_id: str) -> List[Dict[str, Any]]:
        """Get all observables attached to a case in TheHive."""
        response = await self.client.get(f"/api/case/{case_id}/artifact")
        return response

    async def update_observable(self, obs_id: str, **kwargs) -> Dict[str, Any]:
        """Update an observable's tags, TLP, PAP, IOC flag, etc."""
        response = await self.client.patch(f"/api/case/artifact/{obs_id}", json=kwargs)
        logger.info(f"Updated observable {obs_id}")
        return response

    async def delete_observable(self, obs_id: str) -> Dict[str, Any]:
        """Delete an observable."""
        response = await self.client.delete(f"/api/case/artifact/{obs_id}")
        logger.info(f"Deleted observable {obs_id}")
        return response

    async def toggle_observable_ioc(self, obs_id: str, is_ioc: bool) -> Dict[str, Any]:
        """Toggle IOC status on an observable."""
        return await self.update_observable(obs_id, ioc=is_ioc)

    async def mark_observable_sighted(self, obs_id: str, sighted: bool = True) -> Dict[str, Any]:
        """Mark observable as Sighted."""
        return await self.update_observable(obs_id, sighted=sighted)

    # --- TEMPLATES, TAXONOMIES, SYSTEM & METADATA ---

    async def list_case_templates(self) -> List[Dict[str, Any]]:
        """List case templates in TheHive."""
        try:
            return await self.client.get("/api/case/template")
        except Exception:
            return []

    async def create_case_from_template(self, title: str, template_name: str, description: str = "") -> Dict[str, Any]:
        """Create a case based on a case template."""
        payload = {
            "title": title,
            "template": template_name,
            "description": description
        }
        response = await self.client.post("/api/case", json=payload)
        return response

    async def list_organisations(self) -> List[Dict[str, Any]]:
        """List organisations in TheHive."""
        try:
            return await self.client.get("/api/organisation")
        except Exception:
            return []

    async def list_users(self) -> List[Dict[str, Any]]:
        """List users in TheHive."""
        try:
            return await self.client.get("/api/user")
        except Exception:
            return []

    async def list_tags(self) -> List[str]:
        """List existing tags."""
        try:
            res = await self.client.get("/api/case/tag")
            return res if isinstance(res, list) else []
        except Exception:
            return []

    async def list_taxonomies(self) -> List[Dict[str, Any]]:
        """List available taxonomies."""
        try:
            return await self.client.get("/api/taxonomy")
        except Exception:
            return []

    async def add_case_taxonomy(self, case_id: str, taxonomy: str, value: str) -> Dict[str, Any]:
        """Add a taxonomy tag to a case."""
        return await self.add_case_tag(case_id, [f"{taxonomy}:{value}"])

    async def list_custom_fields(self) -> List[Dict[str, Any]]:
        """List custom fields definitions."""
        try:
            return await self.client.get("/api/customField")
        except Exception:
            return []

    async def update_custom_field(self, case_id: str, field_name: str, value: Any) -> Dict[str, Any]:
        """Update a custom field on a case."""
        payload = {"customFields": {field_name: {"order": 0, "value": value}}}
        return await self.update_case(case_id, **payload)

    async def add_case_comment(self, case_id: str, message: str) -> Dict[str, Any]:
        """Add a comment to a case."""
        payload = {"message": message}
        response = await self.client.post(f"/api/v1/case/{case_id}/comment", json=payload)
        logger.info(f"Added comment to case {case_id}")
        return response

    async def find_duplicate_case(self, title: str, rule_id: str = None, hours_window: int = 24) -> Optional[Dict[str, Any]]:
        """Find if an identical case was created/updated within the last N hours."""
        try:
            import time
            now_ms = int(time.time() * 1000)
            window_ms = hours_window * 3600 * 1000
            min_time = now_ms - window_ms

            cases = await self.client.get("/api/case?range=0-100&sort=-createdAt")
            for case in cases:
                case_title = case.get("title", "")
                last_time = max(case.get("updatedAt", 0), case.get("createdAt", 0))
                if last_time >= min_time:
                    if case_title == title or (rule_id and f"Regra {rule_id}:" in case_title):
                        logger.info(f"Duplicate case found in TheHive: {case.get('_id')} ({case_title})")
                        return case
            return None
        except Exception as e:
            logger.warning(f"Error checking duplicate cases in TheHive: {e}")
            return None

    async def healthcheck(self) -> Dict[str, Any]:
        """Check connection health with TheHive server."""
        try:
            res = await self.client.get("/api/status")
            return {"status": "ok", "server_info": res}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_version(self) -> Dict[str, Any]:
        """Get TheHive server version."""
        try:
            return await self.client.get("/api/status")
        except Exception as e:
            return {"version": "TheHive 5", "error": str(e)}

    async def close(self):
        await self.client.close()
