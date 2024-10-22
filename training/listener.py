# listener.py

from pythonosc import osc_server, dispatcher


# Function to handle incoming OSC messages
def handle_sentiment_input(address, *args):
    print(f"Received message at {address}: {args}")


# OSC Server Function
def start_osc_server(port):
    disp = dispatcher.Dispatcher()
    disp.map("/wek/outputs", handle_sentiment_input)

    server = osc_server.BlockingOSCUDPServer(("127.0.0.1", port), disp)
    print(f"Listening for OSC messages on port {port}...")
    server.serve_forever()


if __name__ == "__main__":
    listen_port = 12000
    start_osc_server(listen_port)
