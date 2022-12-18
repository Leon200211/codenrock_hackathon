import base64
from unittest import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import subprocess
import json
import os
import ffmpeg

# Create your tests here.
class Test(TestCase):
    def test_audio_to_table(self):
        # read file "test.wav" and put it to variable "encoded_file" encoded by base64
        audio_file = None
        with open("tests_input/test.wav", "rb") as file:
            original_result_table = bytes(file.read())
            encoded_file = base64.b64encode(original_result_table)
            audio_file = SimpleUploadedFile("test.wav", encoded_file, content_type="audio/wav")
        self.assertIsNotNone(audio_file)
        post = self.client.post("/audio-to-table/", data={"wav": audio_file, "coded": "base64"})
        self.assertEqual(post.status_code, 200)
        self.assertEqual(post.headers.get('Content-Type', ''), "text/csv")
        # read file "test_ouput.csv" and compare it with post body. File from response body should be decoded by base64
        # before comparing
        with open("tests_input/test_output.csv", "rb") as file:
            original_result_table = bytes(file.read())
            result_table_as_bytes = post.content
            result_table = base64.b64decode(result_table_as_bytes)
            self.assertEqual(original_result_table, result_table)

    def test_audio_to_table2(self):
        # read file "test.wav" and put it to variable "encoded_file" encoded by base64
        audio_file = None
        with open("tests_input/test.wav", "rb") as file:
            original_input_audio = bytes(file.read())
            audio_file = SimpleUploadedFile("test.wav", original_input_audio, content_type="audio/wav")
        self.assertIsNotNone(audio_file)
        post = self.client.post("/audio-to-table/", data={"wav": audio_file})
        self.assertEqual(post.status_code, 200)
        self.assertEqual(post.headers.get('Content-Type', ''), "text/csv")
        # read file "test_ouput.csv" and compare it with post body. File from response body should be decoded by base64
        # before comparing
        with open("tests_input/test_output.csv", "rb") as file:
            original_result_table = bytes(file.read())
            result_table_as_bytes = post.content
            result_table = result_table_as_bytes
            self.assertEqual(original_result_table, result_table)
