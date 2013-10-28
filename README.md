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
  - dire des trucs inutiles

Il ne sait pas (encore) :
  - faire le café
  
TODO :
  
[shaarli]
  * Génération du token avec TOTP

Installation :

Pré-requis :
  * python-irclib
  * python-simplejson
  * urllib

Aucune installation nécesaire, éditer le fichier 'conf.yaml'.
