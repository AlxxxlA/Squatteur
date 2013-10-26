#!/usr/bin/python
# -*- coding: UTF-8 -*-
import irclib
import ircbot
from random import randrange
import urllib
import urllib2
import yaml

conf = yaml.load(file('conf.yaml'))


class Bot(ircbot.SingleServerIRCBot):

    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(conf['server']['host'], conf['server']['port'])], conf['server']['nick'], conf['server']['description'])
        
        self.caps_lock = ["Chuuut", "Hohé, hein, bon !", "Ouaich, cris pas !"]
        
        
        
# Connexion aux chans
    def on_welcome(self, serv, ev):
        serv.privmsg("nickserv", "identify DRYTPC12")
        print("Identify")
        serv.join(conf['server']['channels'])

# Si on se fait kick, on revient
    def on_kick(self, serv, ev):
        serv.join(conf['server']['channels'])

# Quand une action se passe sur le salon
    def on_join(self, serv, ev):
        serv.privmsg(ev.target(), "Coucou ! Tu veux voir mon boulon ?")

    def on_pubmsg(self, serv, ev):
        """
        Réception des messages du chan
        """
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
	msg = ev.arguments()[0]
        message = msg.lower()
        messages = message.split(' ')
        
        if msg.isupper() is True:
                say = randrange(0, len(self.caps_lock))
                serv.privmsg(canal, self.caps_lock[say])
        
        if 'lol' in message:
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
        if messages[0] == "!share":
            if len(messages) > 1:
                    url = messages[1]
		    get_params = {'token_auth' : conf['shaarly']['token'], 'post' : url}
		    if len(messages) == 3:
			get_params["tags"] = messages[2]
                    print urllib.urlopen(conf['shaarly']['host']+urllib.urlencode(get_params))
		    

## Passer tous les participants en opérateur du chan
        if message.lower() == "!op":
            serv.mode(canal,"+o Grizby")
            print(message)

        if messages[0].lower() == "!help":
            if len(messages) > 1:
                if messages[1] == "roll":
                    serv.privmsg(canal, "!roll : Roulette russe de 6 chambes")
            print(messages)
            
if __name__ == "__main__":
    Bot().start()
