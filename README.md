# Benchmark Evaluation Platform

## Installation

To get started follow these steps,
* Create and activate a new python environment using the command.
```bash
python3 -m venv venv && source venv/bin/activate
```
* Clone this github repo.
```bash
git clone https://github.com/NLTM-IIITH/benchmark.git
```
* Install the requirements
```bash
cd benchmark && pip install -r requirements.txt
```
* Run the database migrations.
```bash
python manage.py makemigrations && python manage.py migrate
```
* Create a superuser for login
```bash
python manage.py createsuperuser
```
* Start the Django server
```bash
python manage.py runserver 0.0.0.0:8000
```
* Access the website at "[http://127.0.0.1:8000](http://127.0.0.1:8000)"

## Contact

Contact Krishna Tulsyan (krishna.tulsyan@research.iiit.ac.in) for any issues or queries.
