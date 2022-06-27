import os

from pydantic import BaseSettings

class Settings(BaseSettings):
   # OpenAPI
   TITLE = "Grow"
   
   # Redis
   REDIS_HOSTNAME: str
   
   # SQL
   DATABASE_USERNAME: str
   DATABASE_PASSWORD: str
   DATABASE_HOSTNAME = "localhost"
   DATABASE_DATABASE = "grow"
   DATABASE_INIT = False
   @property
   def DATABASE_URL(self):
      return self._get_base_database_url("pymysql")
   @property
   def DATABASE_URL_ASYNC(self):
      return self._get_base_database_url("aiomysql")

   def _get_base_database_url(self, driver: str):
      return f"mysql+{driver}://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOSTNAME}/{self.DATABASE_DATABASE}"

   class Config:
      env_file = os.path.abspath(".env")
      env_file_encoding = "utf-8"