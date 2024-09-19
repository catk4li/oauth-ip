# Discord OAuth

## Description

Ce projet est un bot Discord utilisant OAuth pour vérifier les membres et récupérer leurs adresses IP pendant le processus de vérification. Le bot envoie un lien de vérification aux utilisateurs, qui, lorsqu'ils cliquent dessus, obtiennent un rôle spécifique sur le serveur Discord. Les informations sur l'adresse IP et les détails de l'utilisateur sont collectées et envoyées à un webhook Discord.

## Fonctionnalités

- Envoi d'un lien de vérification avec un bouton dans un message privé.
- Attribution automatique de rôles aux utilisateurs sur Discord après vérification.
- Récupération et envoi des adresses IP des utilisateurs et des détails associés à un webhook Discord.

## Prérequis

- Python 3.8+
- Flask
- Requests
- User Agents
- Nextcord

## Installation

1. **Clonez le repository :**

    ```bash
    git clone https://github.com/catk4li/oauth-ip
    cd oauth-ip
    ```

2. **Installez les dépendances :**

    ```bash
    pip install flask requests user-agents nextcord
    ```

3. **Configurez les variables d'environnement :**

    Remplacez les placeholders suivants dans les fichiers `serveur.py` et `main.py` :

    - `WEBHOOK_URL` : URL du webhook Discord pour les notifications.
    - `DISCORD_API_URL` : URL de l'API Discord.
    - `BOT_TOKEN` : Token du bot Discord.
    - `GUILD_ID` : ID du serveur Discord.
    - `ROLE_ID` : ID du rôle à attribuer.

## Démarrage du serveur Flask

1. **Lancez le serveur Flask :**

    ```bash
    python serveur.py
    ```

   Le serveur Flask sera disponible à l'adresse `http://localhost:5000`.

## Démarrage du Bot Discord

1. **Lancez le bot Discord :**

    ```bash
    python main.py
    ```

   Assurez-vous que le bot est correctement configuré et connecté à votre serveur Discord.

## Utilisation

1. **Obtenez le rôle :**

    Utilisez la commande `!grole` sur votre serveur Discord. Le bot enverra un message privé avec un lien de vérification.

2. **Vérification :**

    Cliquez sur le bouton de vérification dans le message privé. Vous recevrez une confirmation et le rôle sera attribué si la vérification est réussie.
