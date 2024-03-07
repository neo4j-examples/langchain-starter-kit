import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

print(f'Credentials loaded: oak:{OPENAI_API_KEY} n4j_uri:{NEO4J_URI} n4j_database:{NEO4J_DATABASE} n4j_username:{NEO4J_USERNAME} n4j_pass:{NEO4J_PASSWORD}')