from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://timurisakov@localhost/to_do", echo=True, pool_pre_ping=True)
