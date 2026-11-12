---
name: traitement-retour
description: Procédure pour traiter une demande de retour de produit (produit qui ne plaît pas, défectueux, abîmé ou non conforme). À utiliser dès qu'un client veut retourner, renvoyer, échanger ou se faire rembourser un produit d'une commande.
metadata:
  version: "1.0"
  outils: consulter_commande, chercher_politique, creer_retour
---

# Traitement d'une demande de retour

Ce skill décrit **comment** traiter un retour. Les **règles** (délais, conditions)
ne sont pas écrites ici : elles se trouvent dans la politique de la boutique et
se lisent avec `chercher_politique`.

## Procédure (à suivre dans l'ordre)

1. **Identifier la commande.** Si le client ne donne pas de numéro, demande-le.
   Ne devine jamais un numéro.
2. **Consulter la commande** avec `consulter_commande(numero)`.
3. **Vérifier le statut.**
   - `livrée` → continuer.
   - `en préparation` → pas de retour : proposer plutôt une annulation.
   - `expédiée` → pas encore de retour : attendre la livraison.
   - `retour demandé` → un retour existe déjà : ne pas en créer un second.
4. **Lire la règle** avec `chercher_politique("délai et conditions de retour")`.
   Ne cite jamais une règle de mémoire.
5. **Décider** en comparant « livrée il y a N jours » au délai de la politique :

   | Situation                                  | Décision                                     |
   |--------------------------------------------|----------------------------------------------|
   | Dans le délai                              | Retour possible → étape 6                    |
   | Hors délai, produit défectueux             | Pas de retour : orienter vers la garantie    |
   | Hors délai, produit qui ne plaît pas       | Refus poli, expliqué avec la règle           |

6. **Obtenir le motif.** S'il n'est pas clair, demande-le au client.
7. **Créer le retour** avec `creer_retour(numero, motif)`. Cette action est
   soumise à la validation d'un responsable avant d'être exécutée. Réponds
   ensuite selon le résultat de l'outil : retour enregistré, ou action refusée
   par le responsable.

## Modèle de réponse

> Bonjour [client], votre commande [numéro] ([produit]) a été livrée il y a
> [N] jours. [Décision + règle de la politique en une phrase.]
> [Prochaine étape pour le client : renvoyer le produit dans son emballage
> d'origine / contacter le service garantie / aucune action.]

## Erreurs à éviter

- Appeler `creer_retour` sans avoir consulté la commande et lu la politique.
- Promettre un remboursement ou une date : seule la politique fait foi.
- Créer un retour hors délai « pour faire plaisir » au client.
