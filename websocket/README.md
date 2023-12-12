# Websocket Application

Une application Django avec WebSockets pour fournir une communication en temps réel entre le serveur et le client. Voici un aperçu détaillé:

### Bibliothèques utilisés
  - channels: Extension de Django pour gérer les WebSockets et autres protocoles de communication en temps réel.
  - channels-redis: "Channel layer" utilisant Redis comme backend pour gérer les communications entre différentes instances de Django.
  - daphne: Serveur ASGI pour traiter les requêtes HTTP et WebSocket.



###  Fonctionnement:
  - Initialisation: Lorsqu'un client souhaite établir une connexion WebSocket, il envoie une requête d'initialisation à l'application Django.

  - Authentification: Dans le code que vous avez partagé, l'authentification se fait en extrayant un jeton JWT (JSON Web Token) de la chaîne de requête lors de l'établissement de la connexion WebSocket. Si le jeton est valide, l'utilisateur est authentifié.