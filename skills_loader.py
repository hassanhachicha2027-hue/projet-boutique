"""Chargement des skills (format Agent Skills : un dossier par skill avec un SKILL.md).

    skills/
      traitement-retour/
        SKILL.md      <- en-tête YAML (name, description) + instructions en Markdown

Principe de la « divulgation progressive » :
  1. au démarrage, seuls le NOM et la DESCRIPTION de chaque skill vont dans le prompt
     (RESUME_SKILLS) ;
  2. quand une demande correspond, l'agent appelle charger_skill(nom) et lit
     les instructions complètes, et seulement à ce moment-là.
"""
from pathlib import Path

import yaml
from langchain_core.tools import tool

# Lecture de tous les skills au démarrage : {nom: {"description": ..., "instructions": ...}}
CATALOGUE = {}
for fichier in sorted((Path(__file__).parent / "skills").glob("*/SKILL.md")):
    _, entete, corps = fichier.read_text(encoding="utf-8").split("---", 2)  # YAML | Markdown
    meta = yaml.safe_load(entete)
    CATALOGUE[meta["name"]] = {"description": meta["description"], "instructions": corps.strip()}

# Texte ajouté au prompt système : uniquement nom + description de chaque skill
RESUME_SKILLS = (
    "Skills disponibles (appelle charger_skill avec le nom exact AVANT d'agir "
    "si la demande correspond) :\n"
    + "\n".join(f"- {nom} : {s['description']}" for nom, s in CATALOGUE.items())
)


@tool
def charger_skill(nom: str) -> str:
    """Charge les instructions détaillées d'un skill (procédure à suivre pas à pas)."""
    skill = CATALOGUE.get(nom)
    if skill is None:
        return f"Skill inconnu : {nom}. Skills disponibles : {', '.join(CATALOGUE)}."
    return skill["instructions"]
