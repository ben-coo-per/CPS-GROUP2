from utils.wekinator_osc import get_wekinator_osc_server


def handle_sentiment_input(address, *args):
    print(f"Received message at {address}: {args}")


if __name__ == "__main__":
    get_wekinator_osc_server(handle_sentiment_input)
