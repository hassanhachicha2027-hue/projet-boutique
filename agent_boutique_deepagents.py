"""Agent service client — version deepagents : create_deep_agent + skills (standard Agent Skills)
+ RAG (Chroma) + SQL + validation humaine.

Les skills (skills/*/SKILL.md) sont gérés par le SkillsMiddleware de deepagents :
  1. le nom et la description de chaque skill sont injectés dans le prompt système ;
  2. l'agent lit le SKILL.md complet avec l'outil read_file quand la demande correspond.

    uv run indexer.py                                 # une fois, pour indexer la politique
    uv run streamlit run app_streamlit_deepagents.py
"""
import os
from pathlib import Path

from deepagents import (GeneralPurposeSubagentProfile, HarnessProfile, create_deep_agent,
                        register_harness_profile)
from deepagents.backends.filesystem import FilesystemBackend
from deepagents.middleware.filesystem import FilesystemMiddleware
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from indexer import connecter_chroma
from outils_base import OUTILS_SQL

load_dotenv()

# ---------- Outils, prompt et modèle ----------
vector_store = connecter_chroma()


@tool
def chercher_politique(question: str) -> str:
    """Cherche dans les règles de la boutique : livraison, retour, annulation, paiement."""
    docs = vector_store.similarity_search(question, k=2)
    return "\n".join(d.page_content for d in docs)


OUTILS = [chercher_politique, *OUTILS_SQL]
SENSIBLES = {"annuler_commande", "creer_retour"}  # exigent une validation humaine

PROMPT = (
    "Tu es l'assistant du service client d'une boutique en ligne tunisienne. "
    "Réponds en français, brièvement et poliment. N'invente jamais d'information. "
    "Pour une question sur les règles de la boutique, utilise chercher_politique. "
    "Avant toute annulation ou tout retour : consulte la commande, vérifie la règle, "
    "puis agis seulement si la règle est respectée ; sinon explique pourquoi.\n\n"
    "Commence toujours par lire (read_file) le skill qui correspond à la demande, puis suis sa procédure."
)

llm = ChatGoogleGenerativeAI(model=os.getenv("MODELE", "gemini-2.5-flash"), temperature=0)

# ---------- Skills : accès en LECTURE SEULE au dossier skills/ ----------
# La racine du backend est skills/ : l'agent ne peut rien lire d'autre (ni .env, ni le code).
backend = FilesystemBackend(root_dir=Path(__file__).parent / "skills", virtual_mode=True)

# Pour les modèles Google : pas d'outil « task » ni de sous-agent généraliste.
register_harness_profile("google_genai", HarnessProfile(
    excluded_tools=frozenset({"task"}),
    general_purpose_subagent=GeneralPurposeSubagentProfile(enabled=False),
))

# ---------- Agent ----------
app = create_deep_agent(
    model=llm,
    tools=OUTILS,
    system_prompt=PROMPT,
    backend=backend,
    skills=["/"],  # les skills sont à la racine du backend (= dossier skills/)
    middleware=[FilesystemMiddleware(backend=backend, tools=["read_file"])],  # seul outil de fichiers : read_file
    interrupt_on={nom: True for nom in SENSIBLES},  # PAUSE avant chaque outil sensible
    checkpointer=InMemorySaver(),  # mémoire de la conversation (obligatoire pour la pause)
)
