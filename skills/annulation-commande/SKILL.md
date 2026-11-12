---
name: annulation-commande
description: Procédure pour traiter une demande d'annulation de commande. À utiliser dès qu'un client veut annuler, stopper, supprimer une commande ou ne plus la recevoir.
metadata:
  version: "1.0"
  outils: consulter_commande, chercher_politique, annuler_commande
---

# Traitement d'une demande d'annulation

Ce skill décrit **comment** traiter une annulation. Les **règles** (statuts
autorisés, remboursement) ne sont pas écrites ici : elles se trouvent dans la
politique de la boutique et se lisent avec `chercher_politique`.

## Procédure (à suivre dans l'ordre)

1. **Identifier la commande.** Si le client ne donne pas de numéro, demande-le.
   Ne devine jamais un numéro.
2. **Consulter la commande** avec `consulter_commande(numero)`.
3. **Lire la règle** avec `chercher_politique("conditions d'annulation d'une commande")`.
   Ne cite jamais une règle de mémoire.
4. **Décider** selon le statut de la commande et la politique :

   | Statut            | Décision                                                    |
   |-------------------|-------------------------------------------------------------|
   | `en préparation`  | Annulation possible → étape 5                               |
   | `expédiée`        | Pas d'annulation : expliquer et proposer un retour après livraison |
   | `livrée`          | Pas d'annulation : orienter vers une demande de retour      |
   | `annulée`         | Déjà annulée : le confirmer, ne rien refaire                |

5. **Annuler** avec `annuler_commande(numero)`. Cette action est soumise à la
   validation d'un responsable avant d'être exécutée. Réponds ensuite selon le
   résultat de l'outil : commande annulée, ou action refusée par le responsable.

## Modèle de réponse

> Bonjour [client], votre commande [numéro] ([produit]) a le statut [statut].
> [Décision + règle de la politique en une phrase.]
> [Prochaine étape pour le client : aucune action / attendre la livraison puis
> demander un retour / contacter le service client.]

## Erreurs à éviter

- Appeler `annuler_commande` sans avoir consulté la commande.
- Annuler une commande expédiée ou livrée « pour faire plaisir » au client.
- Promettre un délai de remboursement qui ne figure pas dans la politique.
