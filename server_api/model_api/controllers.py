import base64
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .model_nn import text2table


@csrf_exempt
def audio_to_table(request: WSGIRequest) -> HttpResponse:
    try:
        if request.content_type in ["multipart/form-data", "application/x-www-form-urlencoded"]:
            encoding = request.POST.get("coded", "")
            # get file from request body coded by base64 and convert it to .wav file
            audio_bytes = dict(request.POST).get("wav", None)
            if audio_bytes is None:
                audio_bytes = dict(request.FILES).get("wav", None)
            if type(audio_bytes) is list:
                audio_bytes = audio_bytes[0]
            if audio_bytes is None:
                return HttpResponse("No audio file in request body", status=400)
            audio_bytes = audio_bytes.read()
            # save audio_bytes to file "tmp/input.wav"
            if encoding == "base64":
                audio_bytes = base64.b64decode(audio_bytes)
            if not os.path.exists("tmp"):
                os.makedirs("tmp")
            with open("tmp/input.wav", "wb") as file:
                file.write(audio_bytes)
            # convert audio file to table
            result_table = text2table.main("tmp/input.wav")
            # read file "test_ouput.csv" and put it to variable "result_table" encoded by base64
            with open("tests_input/test_output.csv", "rb") as file:
                file_str = bytes(file.read())
                result_table_as_bytes = file_str
                if encoding == "base64":
                    result_table_as_bytes = base64.b64encode(file_str)
                result_table = SimpleUploadedFile("result.csv", result_table_as_bytes, content_type="text/csv")
                # return status code 200 and response body .csv file
                return HttpResponse(result_table, content_type="text/csv")
        else:
            return HttpResponse("Bad request", status=400)
    except Exception as e:
        # Return unknown error
        raise e
        return HttpResponse(f"Unknown error. Exception: {str(e)}", status=500)
