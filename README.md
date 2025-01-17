Le bot du serveur discord de CommentCoder.

## Quickstart

1. Clônez le code
2. Créez un fichier `.env` à partir de `.env.example` et complétez le
3. Récupérez un token sur le discord developer portal
4. Récupérez les différents ID de canaux sur votre serveur
5. Installez les modules avec `pip install -r requirements.txt`
6. Lancez le bot avec `python main.py`

## Comment contribuer ?

1. Rejoindre le discord : https://discord.gg/2AubRA4eBQ
2. Lire le sujet sur le forum : https://discord.com/channels/1115999077776240682/1321674294182543373


## Fonctionnalités : 
Le code du bot fonctionne avec des Cogs. Voici de quoi chaque Cog est composé :
### Leveling
- Commande `/levels`
- Commande `/rank <MEMBRE>`
- Event `on_message` : attribue de l'XP (seulement une fois par minute pour éviter le flood)
### Welcome
- Event `on_member_join` : 
  - Nouveau message de bienvenue dans #💬┃général 
  - Inviter un membre donne de l'XP
### Database
- Commande pour initialiser la DB
- Commande pour donner de l'XP
- Commande pour retirer de l'XP
### Social
- Commandes pour les différents liens (!youtube, !udemy, !github, !tiktok, !instagram, !linkedin)

## Configuration Discord Developer Portal
### Intents
- Presence Intent
- Server Members Intent
- Message Content Intent
### Permissions
- Change Nickname
- Embed Links
- Manage Channels
- Manage Events
- Manage Messages
- Manage Events
- Manage Messages
- Manage Nicknames
- Manage Roles
- Send Messages
- Manage Nicknames
- Manage Roles
- Send Messages
- View Audit Log
- View Channels
- View Server Insights
- View Server Subscription Insights


