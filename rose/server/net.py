import json
import logging

from twisted.internet import protocol
from twisted.protocols import basic
from twisted.web import http, resource, xmlrpc

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol

from rose.common import error, message

log = logging.getLogger("net")


class Hub(object):
    def __init__(self, game):
        game.hub = self
        self.game = game
        self.clients = set()

    # PlayerProtocol hub interface

    def add_player(self, player):
        # First add player, will raise if there are too many players or this
        # name is already taken.
        self.game.add_player(player.name)
        self.clients.add(player)

    def remove_player(self, player):
        if player in self.clients:
            self.clients.remove(player)
            self.game.remove_player(player.name)

    def drive_player(self, player, info):
        self.game.drive_player(player.name, info)

    # WatcherProtocol hub interface

    def add_watcher(self, watcher):
        self.clients.add(watcher)
        msg = message.Message("update", self.game.state())
        watcher.send_message(str(msg))

    def remove_watcher(self, watcher):
        self.clients.discard(watcher)

    # Game hub interface

    def broadcast(self, msg):
        data = str(msg)
        for client in self.clients:
            client.send_message(data)


class PlayerProtocol(basic.LineReceiver):
    def __init__(self, hub):
        self.hub = hub
        self.name = None

    # LineReceiver interface

    def connectionLost(self, reason):
        self.hub.remove_player(self)

    def lineReceived(self, line):
        try:
            msg = message.parse(line)
            self.dispatch(msg)
        except error.Error as e:
            log.warning("Error handling message: %s", e)
            msg = message.Message("error", {"message": str(e)})
            self.sendLine(str(msg).encode("utf-8"))
            self.transport.loseConnection()

    # Hub client interface

    def send_message(self, data):
        self.sendLine(data.encode("utf-8"))

    # Disaptching messages

    def dispatch(self, msg):
        if self.name is None:
            # New player
            if msg.action != "join":
                raise error.ActionForbidden(msg.action)
            if "name" not in msg.payload:
                raise error.InvalidMessage("name required")
            self.name = msg.payload["name"]
            self.hub.add_player(self)
        else:
            # Registered player
            if msg.action == "drive":
                self.hub.drive_player(self, msg.payload)
            else:
                raise error.ActionForbidden(msg.action)


class PlayerFactory(protocol.ServerFactory):
    def __init__(self, hub):
        self.hub = hub

    def buildProtocol(self, addr):
        p = PlayerProtocol(self.hub)
        p.factory = self
        return p


class WatcherProtocol(WebSocketServerProtocol):
    def __init__(self, hub):
        self.hub = hub
        WebSocketServerProtocol.__init__(self)

    # WebSocketServerProtocol interface

    def onConnect(self, request):
        log.info("watcher connected from %s", request)

    def onOpen(self):
        self.hub.add_watcher(self)

    def onClose(self, wasClean, code, reason):
        log.info(
            "watcher closed (wasClean=%s, code=%s, reason=%s)", wasClean, code, reason
        )
        self.hub.remove_watcher(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = json.loads(payload.decode('utf8'))
            action = message.get("action")

            if action == "set_seed":
                seed = message.get("seed")
                if seed:
                    self.hub.game.set_seed(seed)
                    self.send_message(json.dumps({"status": "Seed set successfully"}).encode('utf8'))
                else:
                    self.send_message(json.dumps({"error": "No seed provided"}).encode('utf8'))

            elif action == "get_seed":
                if self.hub.game.seed:
                    self.send_message(json.dumps({"seed": self.hub.game.seed}).encode('utf8'))
                else:
                    self.send_message(json.dumps({"error": "No seed set"}).encode('utf8'))

            else:
                self.send_message(json.dumps({"error": "Unknown action"}).encode('utf8'))
    # Hub client interface

    def send_message(self, data):
        self.sendMessage(data.encode("utf-8"), False)


class WatcherFactory(WebSocketServerFactory):
    def __init__(self, url, hub):
        self.hub = hub
        WebSocketServerFactory.__init__(self, url)

    def buildProtocol(self, addr):
        p = WatcherProtocol(self.hub)
        p.factory = self
        return p


class CliAdmin(xmlrpc.XMLRPC):
    def __init__(self, game):
        self.game = game
        xmlrpc.XMLRPC.__init__(self, allowNone=True)

    def xmlrpc_start(self):
        try:
            self.game.start()
        except error.GameAlreadyStarted as e:
            raise xmlrpc.Fault(1, str(e))

    def xmlrpc_stop(self):
        try:
            self.game.stop()
        except error.GameNotStarted as e:
            raise xmlrpc.Fault(1, str(e))

    def xmlrpc_set_rate(self, rate):
        self.game.rate = rate


class WebAdmin(resource.Resource):
    def __init__(self, game):
        self.game = game
        resource.Resource.__init__(self)

    def render_POST(self, request):
        if b"running" in request.args:
            value = request.args[b"running"][0]
            if value == b"1":
                self.game.start()
            elif value == b"0":
                if self.game.started:
                    self.game.stop()
            else:
                request.setResponseCode(http.BAD_REQUEST)
                return b"Invalid running value %r, expected (1, 0)" % value
        if b"rate" in request.args:
            value = request.args[b"rate"][0]
            try:
                self.game.rate = float(value)
            except ValueError:
                request.setResponseCode(http.BAD_REQUEST)
                return b"Invalid rate value %r, expected number" % value
        return b""

    def render_GET(self, request):
        print(request)
        if request.uri.decode('utf-8').endswith('/seed'):
            # Check if the seed is set
            if self.game.seed is not None:
                # Prepare the response object
                response = {
                    "seed": self.game.seed,
                    "status": "Seed retrieved successfully"
                }
                # Convert the response object to JSON
                response_json = json.dumps(response)
                # Set the content type to JSON
                request.setHeader('Content-Type', 'application/json')
                return response_json.encode('utf-8')
            else:
                request.setResponseCode(400)
                return b"No seed set"
        else:
            request.setResponseCode(404)
            return b"Not Found"


