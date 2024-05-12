import json

class UnrecognizedFileTypeError(Exception):
    """
    Raised when handler does not recognize value in the 'file_type' field
    """
    pass

class MissingRequiredFieldError(Exception):
    """
    Raised when handler receives a JSON without a required field
    """
    def __init__(self, missing_field):
        self.message = f"JSON is missing required {} field".format(missing_field)
        super().__init__(self.message)


class MessageHandler:
    def __init__(self, string_to_func:dict, required_fields:list[str]) -> None:
        self.function_dictionary = string_to_func
        self.require_fields = required_fields

    def validate_json(self, message_json: dict) -> bool:
        """
        Checks JSON for presence of required fields, and confirms that files is
        a type that can be handled by the MessageHandler
        :param message_json: [dict]
        :return: None
        :except: Raises descriptive error if json is missing required fields or file type not recognized
        """
        for field in self.required_fields:
            if field not in message_json:
                raise MissingRequiredFieldError(field)
        if message_json['type'] not in self.function_dictionary:
            raise UnrecognizedFileTypeError

    def generate_reply(self, message:dict):
        """
        Takes a 'message' dict, validates it, then uses the function corresponding to 'type' from the handlers
        dictionary of functions to generate the payload for a reply dictionary object
        If the message is invalid or some error occurs with payload creation, an error dictionary will be returned instead
        :param message: JSON/dict with a 'type' and 'payload' field
        :return: JSON/dict with a 'status' and 'payload' field.
        """
        try:
            self.validate_json(message)
            payload = self.function_dictionary[message['type']](message['payload'])
            reply = {"status":"ok", "payload": payload}
        except Exception as error:
            reply = {"status":"error", error}

        return reply











