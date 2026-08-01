import asyncio
from typing import Dict, Any, List, Optional
from src.core.http_client import AsyncHttpClient
from src.config.settings import settings
from src.utils.logger import logger

class CortexClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.CORTEX_API_KEY}"
        }
        self.client = AsyncHttpClient(settings.CORTEX_URL, headers=self.headers, verify=False)

    async def list_analyzers(self) -> List[Dict[str, Any]]:
        """List all available analyzers in Cortex."""
        response = await self.client.get("/api/analyzer")
        return response

    async def run_analyzer(self, analyzer_id: str, data_type: str, data: str, tlp: int = 2) -> Dict[str, Any]:
        """Run a Cortex analyzer on an observable."""
        payload = {
            "data": data,
            "dataType": data_type,
            "tlp": tlp
        }
        response = await self.client.post(f"/api/analyzer/{analyzer_id}/run", json=payload)
        logger.info(f"Started analyzer {analyzer_id} for {data}")
        return response

    async def list_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List analyzer jobs in Cortex."""
        response = await self.client.get(f"/api/job?range=0-{limit}&sort=-createdAt")
        return response

    async def get_job_report(self, job_id: str) -> Dict[str, Any]:
        """Get report of a Cortex job."""
        response = await self.client.get(f"/api/job/{job_id}/report")
        return response

    async def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a Cortex analysis job."""
        response = await self.client.delete(f"/api/job/{job_id}")
        logger.info(f"Cancelled Cortex job {job_id}")
        return response

    async def list_responders() -> List[Dict[str, Any]]:
        """List available responders in Cortex."""
        response = await self.client.get("/api/responder")
        return response

    async def run_responder(self, responder_id: str, data_type: str, data: str) -> Dict[str, Any]:
        """Run a Cortex responder."""
        payload = {
            "data": data,
            "dataType": data_type
        }
        response = await self.client.post(f"/api/responder/{responder_id}/run", json=payload)
        logger.info(f"Started responder {responder_id}")
        return response
        
    async def wait_for_job(self, job_id: str, max_retries: int = 30, delay: int = 2) -> Dict[str, Any]:
        """Poll Cortex until job finishes."""
        for i in range(max_retries):
            job_info = await self.client.get(f"/api/job/{job_id}")
            status = job_info.get("status")
            if status == "Success":
                return await self.get_job_report(job_id)
            elif status == "Failure":
                logger.error(f"Cortex job {job_id} failed")
                return {"error": "Job failed", "details": job_info}
            await asyncio.sleep(delay)
        return {"error": "Timeout waiting for job completion"}

    async def close(self):
        await self.client.close()
