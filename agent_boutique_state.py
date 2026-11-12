"""Agent service client : LangChain create_agent + RAG (Chroma) + SQL + skills + validation humaine.

La validation humaine est confiée au middleware HumanInTheLoopMiddleware : il met
l'agent en pause avant chaque outil sensible.
Les skills (skills/*/SKILL.md) sont des procédures que l'agent charge à la demande
avec l'outil charger_skill (voir skills_loader.py).

    uv run indexer.py                            # une fois, pour indexer la politique
    uv run streamlit run app_streamlit_state.py
"""
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from indexer import connecter_chroma
from outils_base import OUTILS_SQL
from skills_loader import RESUME_SKILLS, charger_skill

load_dotenv()

# ---------- Outils, prompt et modèle ----------
vector_store = connecter_chroma()


@tool
def chercher_politique(question: str) -> str:
    """Cherche dans les règles de la boutique : livraison, retour, annulation, paiement."""
    docs = vector_store.similarity_search(question, k=2)
    return "\n".join(d.page_content for d in docs)


OUTILS = [chercher_politique, charger_skill, *OUTILS_SQL]  # charger_skill : lecture, pas de validation
SENSIBLES = {"annuler_commande", "creer_retour"}  # exigent une validation humaine

PROMPT = (
    "Tu es l'assistant du service client d'une boutique en ligne tunisienne. "
    "Réponds en français, brièvement et poliment. N'invente jamais d'information. "
    "Pour une question sur les règles de la boutique, utilise chercher_politique. "
    "Avant toute annulation ou tout retour : consulte la commande, vérifie la règle, "
    "puis agis seulement si la règle est respectée ; sinon explique pourquoi.\n\n"
    "Commence toujours par charger le skill qui correspond à la demande, puis suis sa procédure.\n"
    + RESUME_SKILLS  # seulement nom + description de chaque skill (divulgation progressive)
)

llm = ChatGoogleGenerativeAI(model=os.getenv("MODELE", "gemini-2.5-flash"), temperature=0)

# ---------- Agent ----------
app = create_agent(
    llm,
    tools=OUTILS,
    system_prompt=PROMPT,
    middleware=[HumanInTheLoopMiddleware(interrupt_on={nom: True for nom in SENSIBLES})],  # PAUSE
    checkpointer=InMemorySaver(),  # mémoire de la conversation (obligatoire pour la pause)
)
