import sys
from pathlib import Path

# Ajoute le chemin absolu vers le dossier app
sys.path.insert(0, str(Path(__file__).resolve().parent / "app"))

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


