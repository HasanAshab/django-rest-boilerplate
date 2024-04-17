from http.client import responses
from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, data=None, *args, **kwargs):
        self.wrap = kwargs.pop("wrap", True)
        data = self._format_response_data(data)
        super().__init__(data, *args, **kwargs)

    def is_successful(self):
        return 199 < self.status_code < 400

    def standard_message(self):
        return responses[self.status_code]

    def get_wrapper_key(self):
        if not self.wrap:
            return None
        if self.wrap == True:
            return "data"
        return self.wrap

    def _format_response_data(self, data):
        data_type = type(data)

        if data == None:
            return data
        if not self.wrap and data_type in [list, tuple]:
            return data

        if data_type == str:
            data = {"message": data}
        elif data_type != dict:
            data = {self.get_wrapper_key(): data}
        data["success"] = self.is_successful()
        data["message"] = data.get("message", self.standard_message())
        return data
