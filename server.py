import tornado.ioloop
import tornado.web
import tornado.locks

import random
import os

class Dice(object):
    """
    Dice: class that represents our server side dice.
    """
    def __init__(self):
        #the dice number
        self.number = 0
        #a tornado condition.  Serves as a 'gate' that requests
        #can wait to open.  We'll use it for long polling
        self.cond = tornado.locks.Condition() 
        self.roll()
        
    def roll(self):
        self.number = random.randint(1,6)
        #notify all waiting coroutines that the dice has been rolled
        self.cond.notify_all()

class MainHandler(tornado.web.RequestHandler):
    """
    MainHandler: request handler to serve up HTML for the dice.
    """
    def get(self):
        self.render("templates/index.html")

class DiceHandler(tornado.web.RequestHandler):
    """
    DiceHandler: request handler to get the dice status and roll the dice.
    """
    async def get(self):
        """
        get(): get the status of the dice and update client if necessary
        """
        #first, get the number the client has
        client_number = self.get_query_argument("number",0)
        #set a variable if the client side and server side number are the same
        same = int(client_number) == DICE.number
        #if they are the same, then wait for an update.  otherwise, skip waiting
        #and write the number, thus updating the client
        while same:
            #set a variable for the dice condition
            wait_future = DICE.cond.wait()
            try:
                #wait until condition is triggered
                await wait_future
            except asyncio.CancelledError:
                return
            #if roll was the same, no need to send update to client, and start
            #the process over
            same = int(client_number) == DICE.number
            
        if self.request.connection.stream.closed():
            return
        #after we have a different server and client side number, write the update
        #back to the client
        self.write({"number":DICE.number})
        
    def post(self):
        """
        post(): roll the dice
        """
        DICE.roll()
        print("Dice was rolled: " + str(DICE.number))

DICE = Dice()

if __name__ == "__main__":
    #create the tornado application, and specify URL routes
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/dice", DiceHandler),
        ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    #start server
    app.listen(8888)
    #start IO loop
    tornado.ioloop.IOLoop.current().start()
