from pythonosc import udp_client


def get_wekinator_input_client(ip="127.0.0.1", send_port=6448):
    return udp_client.SimpleUDPClient(ip, send_port)


def get_wekinator_output_client(ip="127.0.0.1", send_port=12000):
    return udp_client.SimpleUDPClient(ip, send_port)
