---
name: suivi-commande
description: Procédure pour informer un client sur l'état ou la livraison de sa commande. À utiliser quand un client demande où en est sa commande, quand il sera livré, si sa commande est partie ou pourquoi il ne l'a pas encore reçue.
metadata:
  version: "1.0"
  outils: consulter_commande, chercher_politique
---

# Suivi d'une commande

Ce skill est en **lecture seule** : il n'appelle jamais d'outil qui modifie la base.

## Procédure (à suivre dans l'ordre)

1. **Identifier la commande.** Si le client ne donne pas de numéro, demande-le.
2. **Consulter la commande** avec `consulter_commande(numero)`.
3. **Expliquer le statut** en langage simple :

   | Statut            | Ce que tu dis au client                                     | Règle à lire avec `chercher_politique` |
   |-------------------|-------------------------------------------------------------|----------------------------------------|
   | `en préparation`  | La commande est en cours de préparation, pas encore partie  | « délais de livraison »                |
   | `expédiée`        | La commande est en route                                    | « délais de livraison et suivi »       |
   | `livrée`          | La commande a été livrée il y a N jours                     | aucune (sauf si le client le demande)  |
   | `annulée`         | La commande a été annulée                                   | aucune                                 |
   | `retour demandé`  | Une demande de retour est en cours                          | « remboursement après retour »         |

4. **Donner le délai** uniquement s'il figure dans la politique. Ne calcule
   jamais une date de livraison précise : donne la fourchette de la politique.

## Modèle de réponse

> Votre commande [numéro] ([produit]) est [statut expliqué].
> [Délai ou prochaine étape selon la politique.]

## Erreurs à éviter

- Inventer une date de livraison ou un numéro de suivi.
- Proposer spontanément une annulation ou un retour : réponds seulement à la question posée.
