from sanic import Sanic

app = Sanic(__name__)

from app.controller import __init__
