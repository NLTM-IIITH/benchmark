import json
import time
from os.path import join
from tempfile import TemporaryDirectory

import requests
from google.cloud import texttospeech
from tqdm import tqdm


class TTSAPI:

	MOZHI_ACCESS_TOKEN = "eyJraWQiOiIyaHpiSDhzVGlRY3hlblNKNlRLY3J4cW5vKytMQ093dk5wc082VEp0QURNPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI1MDg0NjFmNS0wYmYxLTRhNGQtOTM1Ny1jZGE0MzQwZDQ0NTQiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtc291dGgtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aC0xX0JmVmo1WVFkZCIsInZlcnNpb24iOjIsImNsaWVudF9pZCI6IjRncHBwZ3Z0YW10dWpwaDAyYjcxaGU1MGNxIiwib3JpZ2luX2p0aSI6ImQzMTU1NGZiLTQyNzUtNDRmZi05MjkyLWMwMmI1MzczMzExZSIsImV2ZW50X2lkIjoiOTMxOThjZTYtZDYzNS00ZTBhLWE0ZWMtY2U0ZjY4ODQxZTI1IiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhd3MuY29nbml0by5zaWduaW4udXNlci5hZG1pbiBwaG9uZSBvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF1dGhfdGltZSI6MTY3NzQ4NjIyMCwiZXhwIjoxNjc3NTcyNjIwLCJpYXQiOjE2Nzc0ODYyMjAsImp0aSI6IjlmN2FmMjBhLWM1Y2UtNGM0ZS05YWQ2LTExYWVhOWU2MDViNiIsInVzZXJuYW1lIjoiNTA4NDYxZjUtMGJmMS00YTRkLTkzNTctY2RhNDM0MGQ0NDU0In0.nelwpy-mB-5nhcVuYV7RaqWgQBNxo0qMQoEj559TfF9BY237Ph-usOftMWsmwHHUjbJtqWgM5BcViUBeHS0n0EmRl_A20OVbdCdK_M7elqYpD8_9he1-4CbBFOkGSOYxanV0OCSz5MccxQMbSZMHx-ZqMZ3rpKqJqIMHE-coUvPWVN-4ZaNqI722jqkB77_n_jHxmjTIUrnB_Ktb5a2BRId5LBTAsQ_vVzna2pWXFl2Q-owKS_WXgPyyJyXPpXQb41IJT4uzScszyCcWianGNeeHnut_B_l8vVHEMrSOXOihh84qx6w1_45P5NE2_FSNJVoH5n92OCEIe9HLpTCkKg"

	def get_access_token():
		key = 'RTFMNGluUVRlc25WbHczMlp6SzB4em9LVVhzYTpXdGZubjhFV29nVlNlTXpHTllzMFBYYkI4dnNh'
		url = 'https://sts.choreo.dev/oauth2/token'
		headers = {
			'Authorization': f'Basic {key}'
		}
		data = {
			'grant_type': 'client_credentials'
		}
		r = requests.post(url, headers=headers, data=data, verify=False)
		print(r.text)
		return r.json()['access_token']

	def fire_mozhi(text, audio_path):
		print(text)
		url = "https://api.mozhi.me/v1/synthesize"
		payload = json.dumps({
			"text": text,
			"spkr": "FEMALE1_CUSTOM"
		})
		headers = {
			'authorization': TTSAPI.MOZHI_ACCESS_TOKEN,
			'Content-Type': 'application/json'
		}
		r = requests.post(url, headers=headers, data=payload)
		jobid = r.json()['jobid']
		count = 0
		while count<=10:
			print(f'Trying to access the status of the request for {count} times')
			url = "https://api.mozhi.me/v1/status"
			payload = json.dumps({
				"jobid": jobid
			})
			r = requests.get(url, headers=headers, data=payload)
			if r.json()['status'] == 'SUCCESS':
				out = r.json()['output']
				with open(audio_path, 'wb') as f:
					f.write(requests.get(out).content)
				return None
			count += 1
			print('waiting for 1 minute before trying again')
			time.sleep(60)
		print('failed to fetch the TTS output from the API')

	def fire_dev(text, lang, audio_path):
		print(text)
		text = text.strip().split('\n')
		print(len(text))
		tmp = TemporaryDirectory(prefix='tts_parts')
		folder = tmp.name
		folder = '/home/ocr_testing/test'
		token = TTSAPI.get_access_token()
		print(f'Performing TTS for {lang}')
		url = "https://11fc0468-644c-4cc6-be7d-46b5bffcd914-prod.e1-us-east-azure.choreoapis.dev/aqqz/iltts/1.0.0/IITM_TTS/API/tts.php"
		headers = {
			'Authorization': f'Bearer {token}',
			'Content-Type': 'application/json',
		}
		ret = []
		# for i in tqdm(text):
		for idx, i in enumerate(text):
			payload = json.dumps({
				'text': i,
				'gender': 'male',
				'lang': 'Hindi',
			})
			try:
				r = requests.post(url, headers=headers, data=payload)
				ret.append(r.json()['outspeech_filepath'][0])
				print(ret[-1])
				with open(join(folder, f'{idx}.wav'), 'wb') as f:
					f.write(requests.get(ret[-1]).content)
			except Exception as e:
				print(e)
				print(r.text)
		ret = [i.strip() for i in ret]
		print(ret)
		return '\n'.join(ret)

	@staticmethod
	def fire(text, language_code, outfile):
		client = texttospeech.TextToSpeechClient()
		synthesis_input = texttospeech.SynthesisInput(text=text)

		# Build the voice request, select the language code ("en-US") and the ssml
		# voice gender ("neutral")
		voice = texttospeech.VoiceSelectionParams(
			language_code=f'{language_code}-IN',
			ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
		)

		# Select the type of audio file you want returned
		audio_config = texttospeech.AudioConfig(
			audio_encoding=texttospeech.AudioEncoding.MP3
		)

		# Perform the text-to-speech request on the text input with the selected
		# voice parameters and audio file type
		response = client.synthesize_speech(
			input=synthesis_input, voice=voice, audio_config=audio_config
		)

		with open(outfile, 'wb') as out:
			out.write(response.audio_content)
