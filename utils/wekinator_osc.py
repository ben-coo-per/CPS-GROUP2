from pythonosc import udp_client, osc_server, dispatcher


def get_wekinator_input_client(ip="127.0.0.1", port=6448):
    return udp_client.SimpleUDPClient(ip, port)


def get_wekinator_osc_server(disp_function, ip="127.0.0.1", port=12000):
    disp = dispatcher.Dispatcher()
    disp.map("/wek/outputs", disp_function)

    server = osc_server.BlockingOSCUDPServer(("127.0.0.1", port), disp)
    print(f"Listening for OSC messages on port {port}...")
    server.serve_forever()
