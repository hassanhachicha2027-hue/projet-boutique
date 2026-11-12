# Agent service client — boutique en ligne

Agent LangChain qui combine :
- **RAG** : recherche dans la politique de la boutique (PDF indexé dans ChromaDB, embeddings Gemini) ;
- **SQL** : consultation, annulation et retour de commandes (SQLite) ;
- **skills** : procédures `SKILL.md` (standard Agent Skills) chargées à la demande ;
- **validation humaine** : pause de l'agent (`HumanInTheLoopMiddleware`) avant toute annulation ou tout retour.

Le projet existe en deux versions, qui partagent les mêmes skills, outils et données.

## Fichiers communs

| Fichier | Rôle |
|---|---|
| `indexer.py` | Charge le PDF, le découpe et l'indexe dans Chroma (`connecter_chroma`) |
| `outils_base.py` | Base SQLite et outils SQL |
| `skills/*/SKILL.md` | Procédures (skills) lues à la demande par l'agent |
| `politique_boutique.pdf` | Règles de la boutique |
| `pyproject.toml` / `uv.lock` | Dépendances gérées avec uv |

## Version 1 — `create_agent` + chargeur de skills écrit à la main

| Fichier | Rôle |
|---|---|
| `skills_loader.py` | Lit les skills et fournit l'outil `charger_skill` |
| `agent_boutique_state.py` | Agent `create_agent` + middleware de validation humaine |
| `app_streamlit_state.py` | Interface Streamlit |
| `graphe_agent.png` | Schéma du graphe |

## Version 2 — `create_deep_agent` (deepagents) + `SkillsMiddleware`

| Fichier | Rôle |
|---|---|
| `agent_boutique_deepagents.py` | Agent `create_deep_agent` : skills lus avec `read_file`, accès en lecture seule au dossier `skills/` |
| `app_streamlit_deepagents.py` | Interface Streamlit |
| `graphe_agent_deepagents.png` | Schéma du graphe |

## Installation (uv)

```bash
uv sync                  # crée .venv et installe les dépendances du uv.lock
# puis créer le fichier .env avec GOOGLE_API_KEY (voir le tutoriel, étape 2)
```

## Lancement

```bash
uv run indexer.py                                 # une fois : indexation de la politique
uv run streamlit run app_streamlit_state.py       # version 1
uv run streamlit run app_streamlit_deepagents.py  # version 2
```

Ajouter une dépendance : `uv add <paquet>`.
