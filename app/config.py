from pydantic_settings import BaseSettings

# Example of creating environment variables using pydantic's BaseSettings class. This is a better way to manage environment variables in a FastAPI application, as it allows us to define the expected environment variables and their types, and also provides validation and default values.
class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"  # specify the name of the environment file, it will be read from the root directory of the project

settings = Settings()  # create an instance of the Settings class, it will read the environment variables and set the values of the attributes
