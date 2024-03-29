import argparse

from gevent.pywsgi import WSGIServer

from fml.server.server import server_app
from fml.server.timer import MANAGER, Checker


def run():
    parser = argparse.ArgumentParser(description="Alarms Server")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
    )

    MANAGER.check()
    Checker(MANAGER).start()

    args = parser.parse_args()

    if args.debug:
        server_app.run(debug=True, port=8888)
    else:
        server = WSGIServer(("localhost", 8888), server_app)
        server.serve_forever()


if __name__ == "__main__":
    run()
