from tornado.options import define

# Defines an option in the global namespace.
define("appname", default="app", type=str)
define("env", default="local", type=str)
define("port", default="8080", type=int)