#!/usr/bin/python
# -*- coding: UTF-8 -*-
import irclib
import ircbot
from random import randrange
import urllib
import urllib2
import yaml
import re
import simplejson

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
        users = self.channels[canal].users() # On récupère les utilisateurs sur le chan
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
                tags = re.findall('\[(.+)\]', message)
                tags = ''.join(tags)
                url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&#+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
                url = ''.join(url)
                description = ''.join(re.findall('\"(.+)\"', msg))
                get_params = {'token_auth' : conf['shaarli']['token'], 'post' : url, 'tags' : auteur}
                if tags:
                    get_params["tags"] = tags+" "+auteur
                if description:
                    get_params["description"] = description
                res = urllib.urlopen(conf['shaarli']['host']+urllib.urlencode(get_params))
                print(tags, url)
                print(conf['shaarli']['host']+urllib.urlencode(get_params))
                print(res.read())

## Passer tous les participants en opérateur du chan
        if messages[0] == conf['command']['op']:
            serv.mode(canal, "+"+"o"*len(users)+' '+' '.join(users))

        if messages[0] == conf['command']['help']:
            if len(messages) > 1:
                command = messages[1]
                for command in help.keys():
                    if command == messages[1]:
                        serv.privmsg(canal, help[command].encode('utf-8'))
            else:
                serv.privmsg(canal, "Liste des commandes disponibles")
                serv.privmsg(canal, conf['command'].keys())

# Transmet le lien à Yourls et renvoi le titre et le lien raccourcis
        if re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&#+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+').search(message):
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&#+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            print(urls)
            for url in urls:
                get_params = {'signature': conf['yourls']['token'], 'action': 'shorturl', 'format': 'json', 'url': url}
                res = simplejson.load(urllib.urlopen(conf['yourls']['host']+urllib.urlencode(get_params)))
                if res['statusCode'] == 200:
                    serv.privmsg(canal, res['title'].encode('utf-8')+" - "+res['shorturl'].encode('utf-8'))
                
                

            
if __name__ == "__main__":
    Bot().start()
