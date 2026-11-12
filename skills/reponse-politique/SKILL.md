---
name: reponse-politique
description: Méthode pour répondre aux questions générales sur les règles de la boutique (livraison, frais de port, paiement, garantie, remboursement, données personnelles) sans commande précise. À utiliser quand le client pose une question sur les conditions de vente et ne demande aucune action sur une commande.
metadata:
  version: "1.0"
  outils: chercher_politique
---

# Répondre à une question sur la politique de la boutique

## Procédure

1. **Reformuler la question en mots-clés** pour la recherche.
   Exemple : « c'est gratuit la livraison ? » → `chercher_politique("frais de livraison")`.
2. **Chercher** avec `chercher_politique`. Si les passages ne répondent pas,
   refais **une** recherche avec d'autres mots-clés (synonymes, nom de l'article).
3. **Répondre uniquement avec ce que disent les passages.**
   - Si l'information est trouvée → réponds en citant l'article.
   - Si elle n'est pas trouvée après deux recherches → dis-le clairement et
     oriente vers le service client. N'invente jamais.
4. **Montants et délais** : recopie-les exactement (ex. « 200 DT », « 2 à 4 jours
   ouvrables »), sans arrondir ni reformuler.

## Modèle de réponse

> [Réponse en une ou deux phrases.]
> *Source : politique de la boutique, Article [n] — [titre].*

## Erreurs à éviter

- Répondre de mémoire sans avoir appelé `chercher_politique`.
- Mélanger les règles de deux articles différents sans le signaler.
- Consulter une commande alors que le client pose une question générale.
