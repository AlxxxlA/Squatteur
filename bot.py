#!/usr/bin/python
# -*- coding: UTF-8 -*-
import irclib
import ircbot
from random import randrange
import urllib
import urllib2

class Bot(ircbot.SingleServerIRCBot):

    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.freenode.net", 6667)], "Squatteur", "Un bot sachant squatter sur un chan est un bon squatteur")
        
        self.caps_lock = ["Chuuut", "Hohé, hein, bon !", "Ouaich, cris pas !"]
        self.chambre = 6
        self.base = "http://shaarly.bhz.im/addlink.php?token_auth=token&post="
        
# Connexion aux chans
    def on_welcome(self, serv, ev):
        serv.privmsg("nickserv", "identify DRYTPC12")
        print("Identify")
        serv.join("#lesquat")

# Si on se fait kick, on revient
    def on_kick(self, serv, ev):
        serv.join("#lesquat")

# Quand une action se passe sur le salon
    def on_join(self, serv, ev):
        serv.privmsg(ev.target(), "Coucou ! Tu veux voir mon boulon ?")

    def on_pubmsg(self, serv, ev):
        """
        Réception des messages du chan
        """
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]
        messages = message.split(' ')
        
        if message.isupper() is True:
                say = randrange(0, len(self.caps_lock))
                serv.privmsg(canal, self.caps_lock[say])
        
        if 'lol' in message.lower():
            serv.privmsg(canal, "On ne lol pas ici.")
# Roulette russe
        if message.lower() == "!roll":
            
            random = randrange(0, self.chambre)
            clic = randrange(0, self.chambre)
            if random == clic:
                serv.privmsg(canal, "**BANG**")
                serv.kick(canal, auteur, "Touché")
                self.chambre = 6
                serv.privmsg(canal, "À qui le tour ?")
            else:
                serv.privmsg(canal, "--CLIC--")
                self.chambre = self.chambre - 1

# Partager un lien sur shaarly                
        if messages[0].lower() == "!share":
            if len(messages) > 1:
                    url = messages[1].lower()
                    urllib.urlopen(self.base+url)

## Passer tous les participants en opérateur du chan
        if message.lower() == "!op":
            serv.mode(canal,"+o Grizby")
            print(message)

        if messages[0].lower() == "!help":
            if len(messages) > 1:
                if messages[1] == "roll":
                    serv.privmsg("#lesquat", "!roll : Roulette russe de 6 chambes")
            print(messages)
            
if __name__ == "__main__":
    Bot().start()
