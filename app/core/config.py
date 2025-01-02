from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatbot"
    database_url_normal: str = "postgresql://postgres:postgres@localhost:5432/chatbot?sslmode=disable"
    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openai_api_key: str
    langchain_api_key: str
    langchain_tracing_v2: bool
    langchain_endpoint: str
    langchain_project: str
    tavily_api_key: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()