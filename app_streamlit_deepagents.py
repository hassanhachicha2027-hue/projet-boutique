"""Interface Streamlit de l'agent service client — version deepagents.

Streamlit ne garde pas de copie de la conversation : l'historique et les actions
en attente sont lus directement dans l'état de l'agent (app.get_state).
L'agent (agent_boutique_deepagents.py) lit ses skills avec l'outil read_file.

    uv run streamlit run app_streamlit_deepagents.py
"""
import uuid
from pathlib import Path

import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from agent_boutique_deepagents import app
from outils_base import creer_base

st.set_page_config(page_title="Service client boutique", page_icon="🛒")

DOSSIER = Path(__file__).parent
# standard Agent Skills : le nom d'un skill est le nom de son dossier
NOMS_SKILLS = sorted(f.parent.name for f in (DOSSIER / "skills").glob("*/SKILL.md"))

# ---------- Initialisation ----------
st.cache_resource(creer_base)()  # une seule fois au démarrage du serveur
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())  # seule information gardée par Streamlit

config = {"configurable": {"thread_id": st.session_state.thread_id}}
snapshot = app.get_state(config)                   # photo de l'état de l'agent
messages = snapshot.values.get("messages", [])     # historique de la conversation
pause = snapshot.interrupts[0].value if snapshot.interrupts else None  # agent en pause ?
# le middleware décrit chaque appel d'outil à valider dans pause["action_requests"]
actions = [f"{a['name']} {a['args']}" for a in pause["action_requests"]] if pause else None
# skills lus par l'agent : appels read_file sur « /<nom-du-skill>/SKILL.md »
skills_lus = {a["args"].get("file_path", "").strip("/").split("/")[0] for m in messages if m.type == "ai"
              for a in m.tool_calls if a["name"] == "read_file"}

# ---------- Barre latérale ----------
with st.sidebar:
    st.header("🛒 Boutique")
    st.caption("Agent deepagents : skills + RAG + SQL + validation humaine")
    if st.button("Nouvelle conversation", use_container_width=True):
        creer_base()              # remet les commandes dans leur état initial
        st.session_state.clear()  # nouveau thread_id = nouvelle conversation
        st.rerun()

    with st.expander("Graphe de l'agent"):  # schéma des nœuds et des arêtes
        st.image(str(DOSSIER / "graphe_agent_deepagents.png"))

    st.subheader("Skills")
    st.markdown("\n".join(f"- {'✅' if nom in skills_lus else '▫️'} `{nom}`" for nom in NOMS_SKILLS))
    st.caption("✅ = skill lu par l'agent (read_file) dans cette conversation")

    st.subheader("Questions à essayer")
    st.markdown(
        "- Quels sont les délais de livraison ?\n"
        "- Où en est la commande 1002 ?\n"
        "- Annule ma commande 1001\n"
        "- J'ai reçu la commande 1003 mais la souris ne marche pas, "
        "je peux la retourner ?\n"
        "- Je veux retourner la commande 1004, le casque ne me plaît plus."
    )

# ---------- Conversation (lue dans l'état) ----------
st.title("Service client")

for m in messages:
    if m.type == "human":
        st.chat_message("user").markdown(m.text)
    elif m.type == "ai" and m.text:  # on ignore les messages qui ne font qu'appeler des outils
        st.chat_message("assistant").markdown(m.text)

envoi_au_graphe = None  # question du client ou décision du responsable (None : rien à envoyer)

# Validation humaine : l'agent est en pause
if actions:
    st.markdown("**Validation requise :**\n\n" + "\n".join(f"- `{a}`" for a in actions))
    col1, col2 = st.columns(2)
    # une décision par action, dans le même ordre (format attendu par HumanInTheLoopMiddleware)
    if col1.button("✅ Valider", use_container_width=True):
        envoi_au_graphe = Command(resume={"decisions": [{"type": "approve"}] * len(actions)})
    if col2.button("❌ Refuser", use_container_width=True):
        refus = {"type": "reject", "message": "Action refusée par le responsable."}
        envoi_au_graphe = Command(resume={"decisions": [refus] * len(actions)})

question = st.chat_input("Votre question...", disabled=bool(actions))
if question:
    st.chat_message("user").markdown(question)
    envoi_au_graphe = {"messages": [HumanMessage(question)]}

# ---------- Exécution de l'agent ----------
if envoi_au_graphe is not None:
    with st.spinner("Thought..."):
        app.invoke(envoi_au_graphe, config)  # le résultat est enregistré dans l'état
    st.rerun()                               # réaffichage à partir du nouvel état
