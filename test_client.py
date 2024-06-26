import zmq
import base64
import json

class TestClient:
    def __init__(self, address: str = "localhost", port: int = 5555):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(address, port))

    def mainloop(self):
        """
        # Test image conversion
        with open("longcat.jpg", "rb") as image_file:
            encoded_message = base64.b64encode(image_file.read()).decode('utf-8')
        message = {"type": "img", "payload": encoded_message}
        self.socket.send_json(message)

        reply: dict = self.socket.recv_json()
        print(json.dumps(reply, indent=2))

        with open("longcat.pdf", "wb+") as pdf_file:
            decoded_file = base64.b64decode(reply['payload'])
            pdf_file.write(decoded_file)
        print("Image PDF received")
        """

        # Test text conversion
        with open("lorem_ipsum.txt", "rb") as text_file:
            encoded_message = base64.b64encode(text_file.read()).decode('utf-8')
        message = {"type": "text", "payload": encoded_message, "font": "Arial", "size": "15"}
        print("Sending message to PDFMaker Server...")
        print(json.dumps(message,indent=2))
        self.socket.send_json(message)

        print("")

        reply: dict = self.socket.recv_json()
        print("Receiving reply from server...")
        print(json.dumps(reply, indent=2))
        print("")


        with open("lorem_ipsum.pdf", "wb+") as pdf_file:
            decoded_file = base64.b64decode(reply['payload'])
            pdf_file.write(decoded_file)
        print("Text PDF received: lorem_ipsum.pdf")


if __name__ == "__main__":
    client = TestClient("localhost", 5555)
    client.mainloop()
