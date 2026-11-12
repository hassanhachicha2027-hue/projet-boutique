---
name: reclamation-client
description: Conduite à tenir face à un client mécontent, en colère ou qui fait une réclamation (retard, produit abîmé, mauvaise expérience, menace d'avis négatif). À utiliser dès que le message exprime une insatisfaction, avant de traiter la demande elle-même.
metadata:
  version: "1.0"
  outils: consulter_commande, chercher_politique, charger_skill
---

# Gérer une réclamation

Ce skill règle le **ton** et l'**orientation**. Pour l'action elle-même
(retour, annulation, suivi), il renvoie vers le skill adapté.

## Procédure

1. **Accuser réception de l'émotion** en une phrase, sans se justifier.
   Exemple : « Je comprends votre agacement, je regarde votre commande tout de suite. »
2. **Identifier la commande** et la consulter avec `consulter_commande(numero)`.
3. **Identifier le vrai besoin** et charger le skill correspondant :

   | Le client veut…                          | Skill à charger         |
   |------------------------------------------|-------------------------|
   | savoir où est sa commande (retard)       | `suivi-commande`        |
   | renvoyer ou échanger un produit          | `traitement-retour`     |
   | ne plus recevoir sa commande             | `annulation-commande`   |
   | une règle (garantie, remboursement…)     | `reponse-politique`     |
   | autre chose (litige, geste commercial)   | aucun : étape 4         |

4. **Hors procédure** : si la demande ne correspond à aucun skill, lis les
   modalités de réclamation avec `chercher_politique("réclamation service client")`
   et transmets-les au client.

## Ton

- Phrases courtes, vouvoiement, pas de jargon (« statut », « ID »…).
- Une seule excuse, au début. Pas d'excuses répétées.
- Pas de promesse hors politique : ni geste commercial, ni remboursement, ni délai inventé.

## Erreurs à éviter

- Répondre à la colère par la règle brute (« La politique interdit… ») sans phrase d'empathie.
- Accorder une exception pour calmer le client.
