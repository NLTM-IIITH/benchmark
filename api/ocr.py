import json

import requests


class OCRAPI:

	@staticmethod
	def fire(
		dataset,
		model
	) -> list[dict[str, str]]:
		"""
		input is the path to the Dataset.file in json in the format
		[{
			"image": "<base64 image content>",
			"gt": "<groundtruth of the image>",
		}]

		output of the function is in the format
		[{
			"gt": "<groundtruth of the image>",
			"ocr": "<corresponding ocr value of the image>"
		}]
		"""
		url = 'https://ilocr.iiit.ac.in/ocr/infer'
		with open(dataset.file.path, 'r', encoding='utf-8') as f:
			dataset = json.loads(f.read())
		images = [i['image'] for i in dataset]
		ocr_request = {
			'imageContent': images,
			'modality': model.modality.name,
			'version': model.version.name,
			'language': model.language.code,
		}
		headers = {
			'Content-Type': 'application/json'
		}
		response = requests.post(
			url,
			headers=headers,
			data=json.dumps(ocr_request),
		)
		if response.ok:
			response = response.json()
			response = [i['text'] for i in response]
			assert len(response) == len(dataset), (
				'# of images in the OCR response doesnt match the request'
			)
			ret = []
			for d, ocr in zip(dataset, response):
				ret.append({
					'gt': d['gt'],
					'ocr': ocr.strip()
				})
			return ret
		else:
			raise ValueError(response.text)
