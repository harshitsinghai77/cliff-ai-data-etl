install:
	poetry install

export_requirments.txt:
	poetry export -f requirements.txt --output requirements.txt

runserver:
	uvicorn main:app --reload --port 5000

docker_image:
	docker build -t cliff-app .

start_docker_container:
	docker run -d --name cliff-app -p 5000:5000 cliff-app

restore_sample_data:
	docker exec -i cliff-postgres pg_restore -U cliff -v -d cliff < dev/dump/sample.dump

dump_sample_data:
	pg_dump -O -f dev/dump/sample.sql postgres://cliff:password@localhost:5432/cliff

format:
	bash scripts/format.sh

test:
	pytest --cov=app 