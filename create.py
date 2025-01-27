from database import engine
from models import Base  # Importer les modèles

# Créer toutes les tables
Base.metadata.create_all(bind=engine)
