from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # TheHive Settings
    THEHIVE_URL: str
    THEHIVE_API_KEY: str
    
    # Cortex Settings (Optional integration for analyzers and responders)
    CORTEX_URL: Optional[str] = "http://192.168.0.107:9001"
    CORTEX_API_KEY: Optional[str] = "w/G60UamrcGuLP33aA+Y36mrHmZp0c6h"
    
    # MISP Settings (Optional integration for CTI sync and event import/export)
    MISP_URL: Optional[str] = "https://192.168.0.107"
    MISP_API_KEY: Optional[str] = "RRuEFqrYDz4U44ZGGqDWyWfux5PmBfLC4YRfG83k"
    MISP_VERIFY_SSL: bool = False
    
    # App Settings
    LOG_LEVEL: str = "INFO"
    FAST_MCP_NAME: str = "TheHive-MCP-Server"
    FAST_MCP_PORT: int = 9000
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
