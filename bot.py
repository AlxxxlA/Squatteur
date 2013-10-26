#!/usr/bin/python
# -*- coding: UTF-8 -*-
import irclib
import ircbot
from random import randrange
import urllib
import urllib2
import yaml

conf = yaml.load(file('conf.yaml'))
help = yaml.load(file('help.yaml'))

class Bot(ircbot.SingleServerIRCBot):

    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(conf['server']['host'], conf['server']['port'])], conf['server']['nick'], conf['server']['description'])
        
        self.caps_lock = ["Chuuut", "Hohé, hein, bon !", "Ouaich, cris pas !"]
        self.chambre = conf['roll']['chambre']
        
        
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
        users = self.channels[canal].users()
        msg = ev.arguments()[0]
        message = msg.lower()
        messages = message.split(' ')
        
        if msg.isupper() is True:
                say = randrange(0, len(self.caps_lock))
                serv.privmsg(canal, self.caps_lock[say])
        
        if 'lol' in message:
            serv.privmsg(canal, "On ne lol pas ici.")
# Roulette russe
        if message.lower() == conf['command']['roll']:
            
            random = randrange(0, self.chambre)
            clic = randrange(0, self.chambre)
            if random == clic:
                serv.privmsg(canal, "**BANG**")
                serv.kick(canal, auteur, "Touché")
                self.chambre = conf['roll']['chambre']
                serv.privmsg(canal, "À qui le tour ?")
            else:
                serv.privmsg(canal, "--CLIC--")
                self.chambre = self.chambre - 1

# Partager un lien sur shaarly                
        if messages[0] == conf['command']['shaarli']:
            if len(messages) > 1:
                url = messages[1]
                get_params = {'token_auth' : conf['shaarli']['token'], 'post' : url}
                if len(messages) == 3:
                    get_params["tags"] = messages[2].replace(',', ' ')
                if len (messages) == 4:
                    get_params["description"] = message[4]
                print urllib.urlopen(conf['shaarli']['host']+urllib.urlencode(get_params))


## Passer tous les participants en opérateur du chan
        if messages[0] == conf['command']['op']:
            print(users)
            print("+o"*len(users)+' '.join(users))
            serv.mode(canal, "+"+"o"*len(users)+' '+' '.join(users))
            print(message)

        if messages[0] == conf['command']['help']:
            if len(messages) > 1:
                command = messages[1]
                for command in help.keys():
                    if command == messages[1]:
                        serv.privmsg(canal, help[command].encode('utf-8'))
            else:
                serv.privmsg(canal, "Liste des commandes disponibles")
                serv.privmsg(canal, conf['command'].keys())
            print(messages)

            
if __name__ == "__main__":
    Bot().start()
