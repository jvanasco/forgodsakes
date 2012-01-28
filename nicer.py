# coding=utf-8
r"""


    1. made this a little more oop nd to run off of 'main' (keep_on_with_the_force_dont_stop) , so that it...
        - if you run on commandline, it needs the configparser
        - if you don't, you could import this off another modules (i.e. its reusable )
        - the setup of the search patterns and responses are in main too
        - you could wrap this all in eventlet and just run as a daemon that polls twitter regularly, and does the other processing async

    2. it should save stuff to sqlite , keep a local db of what you've repsonded to ( and what you said ). 
    
    
config file= nicer.cfg
    
config format= 

[tokens]
consumer_key = 123
consumer_secret = 123
access_token_key = 123
access_token_secret = 123

[sqlite]
dbfile= nicer.sqlite



"""
import ConfigParser
import time
import twitter
import sqlite3


def keep_on_with_the_force_dont_stop():
    config = ConfigParser.ConfigParser()
    config.read('nicer.cfg')
    
    api = twitter.Api( consumer_key=config.get('tokens','consumer_key'),
                  consumer_secret=config.get('tokens','consumer_secret'),
                  access_token_key=config.get('tokens','access_token_key'),
                  access_token_secret=config.get('tokens','access_token_secret')
            )
    try:
        print "attempting to connect with the api..."
        print api.VerifyCredentials() 
        print "enabling our sqlite storage..."
        connection = sqlite3.connect(config.get('sqlite','dbfile'))
        cursor= connection.cursor()
    except twitter.TwitterError :
        raise
    except:
        raise
    
    twitticisms= [ Sarcasm( account='wormmouth', search_string='baited breath" -"RT" -cheese -mouse -mousetrap -mousetraps -bated -fish' , response_template=u'@%(screen_name)s I think you meant to say “bated breath” ... Have a nice day!') ]

    heartbreakEnemyDespise= SearchAndRespond(api)
    heartbreakEnemyDespise.dont_stop_til_you_get_enough(twitticisms)
    
    
class Sarcasm(object):
    def __init__(self,account=None,search_string=None,response_template=None):
        self.account= account
        self.search_string= search_string
        self.response_template= response_template
        self.tweets_in= {}
        self.tweets_responded= {}
        self.screen_names_responded= {}
        self.recent_replies= []
    
    def search(self,api):
        try:
            statuses = api.GetSearch(self.search_string)
            for i in statuses:
               self.tweets_in[i.id]= i
        except:
            raise

    def api_refresh_already_replied(self,api):
        """this should really save to the db, instead of an object"""
        try:
            my_timeline = api.GetUserTimeline(self.account)
            for t in my_timeline:
                if t.id in self.tweets_in:
                    del self.tweets_in[t.id]
                if t.id not in self.tweets_responded:
                    self.tweets_responded[t.id]= {\
                        'id':t.id,
                        'in_reply_to_status_id':t.in_reply_to_status_id,
                        'in_reply_to_user_id':t.in_reply_to_user_id,
                        'in_reply_to_screen_name':t.in_reply_to_screen_name,
                    }
                if t.in_reply_to_screen_name not in self.screen_names_responded:
                    self.screen_names_responded[t.in_reply_to_screen_name]= True
        except:
            raise

    def reply(self,api):
        try:
            print "----"
            print "----"
            print "----"
            print "Not really reploying.  note the 'if 0'"
            print "----"
            for id in self.tweets_in:
                t= self.tweets_in[id]
                # lets just only respond to a screen id once
                if 1 and ( t.in_reply_to_screen_name in self.screen_names_responded ):
                    continue

                status= self.response_template % { 'screen_name' : t.user.screen_name }
                print status
                if 0:
                    posted_status = api.PostUpdate( status, in_reply_to_status_id=t.id )
                    self.recent_replies.append(posted_status)
        except:
            raise
          
    
def update_homepage(twitticism):
    pass


class SearchAndRespond(object):
    api= None
    
    def __init__(self,api):
        self.api= api
        
    def dont_stop_til_you_get_enough(self,twitticisms):
        print ""
        print """Lovely Is The Feeling Now I Won't Be Complanin' (Ooh Ooh)"""
        print """The Force Is Love Power"""
        print ""
        for twitticism in twitticisms:
            print """Keep On With The Force Don't Stop"""
            print """Don't Stop 'Til You Get Enough"""
            try:
                twitticism.search(self.api)
                twitticism.api_refresh_already_replied(self.api)
                twitticism.reply(self.api)
                update_homepage(twitticism)
            except:
                raise


        
    

    

if __name__ == '__main__':
    keep_on_with_the_force_dont_stop()