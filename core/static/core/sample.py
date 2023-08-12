import requests


def main():
	url = 'http://bhaasha.iiit.ac.in/leaderboard/submission/api/'
	r = requests.post(url, data={'name': 'Hindi Handwritten Submission', 'dataset_id':1})
	subid = r.json()['submission_id']
	while True:
		url = 'http://bhaasha.iiit.ac.in/leaderboard/submission/api/{}/get_image/'.format(subid)
		r = requests.get(url)
		res = r.json()['result_id']
		image = r.json()['image']
		if int(res) == -1 and image is None:
			break

		url = 'http://bhaasha.iiit.ac.in/ocr/handwritten/'
		r = requests.post(url, json={'image': image, 'language': 'hindi'})

		text = r.json()['text']

		print(f'result with id={res} has image with length: {len(image)} and text={text}')


		url = 'http://bhaasha.iiit.ac.in/leaderboard/result/api/{}/'.format(res)
		r = requests.post(url, data={'text': text})

	url = 'http://bhaasha.iiit.ac.in/leaderboard/submission/api/{}/close/'.format(subid)
	r = requests.post(url)
	print(r.json())


if __name__ == '__main__':
	main()
