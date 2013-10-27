Squatteur
=========

Un bot simpliste et amateur écrit en python avec irclib et ircbot.

Pour modifier la configuration du bot, éditer le fichier "conf.yaml" (server, nickname, channels).
Pour modifier la description des commandes d'aide, éditer le fichier "help.yaml"

Il sait :
  - partager des liens sur shaarly (shaarli un peu custom)
  - raccourcir des liens automatiquement et renvoyer le lien et le titre de l'url
  - faire des roulettes russes
  - rendre les utilisateurs opérateurs sur un canal

Il ne sait pas (encore) :
  - faire le café
  
TODO :
  
[shaarli]
  * Récupérer les [tags] et la "description" quel que soit la position
  * Génération du token avec TOTP
  * Suivre les redirections 301 / 302 pour récupération auto du titre / infos

[Yourls]
  * Lors de la publication d'un lien sur le chan, envoyer automatiquement à Yourls et retourner le titre de la page et le lien réduit

  
