# LawRAG

![logo](./frontend/src/assets/lawrag.png)

## Description

This repository contains the code and data for the Data Battle 2025 organized by the IA Pau. The goal of this competition is to create an application to help student to study their exams about intellectual property laws.

This project use some AI models to help the students to study the laws. Be careful, this project is not a replacement for the study of the laws, it's just a tool to help the students to study. We try to make the most accurate AI models but we can't guarantee that the answers are correct.

Finally, it is recommended to have GPU to run this project locally. If you don't have GPU, the time to run the AI models can be very long.

## Installation with Docker

This is the way we recommend to install the project for a basic use. You need to have Docker and Docker Compose installed on your computer.

1. Clone the repository

```sh
git clone https://github.com/SOULIER-Patrice/ia-pau-data-battle-mars-2025.git
```

2. Go to the project folder

```sh
cd ia-pau-data-battle-mars-2025
```

3. Build the Docker image

```sh
docker compose build
```

4. Run the Docker container

```sh
docker compose up
```

5. Open your browser and go to the following URL: [http://localhost:5173](http://localhost:5173)

## Installation without Docker

This is the way we recommend to install the project for a development use. This project is tested with Python 3.13.2 and v23.2.0, we can't guarantee that it will work with other versions.

1. Clone the repository

```sh
git clone https://github.com/SOULIER-Patrice/ia-pau-data-battle-mars-2025.git
cd ia-pau-data-battle-mars-2025
```

### Ollama Server

This project use the Ollama server to run the AI models. You need to install it before running the project. You can find the installation instructions [here](https://github.com/ollama/ollama).

We recommend to use Docker to install it.

```sh
docker run -d --gpus=all --name ollama -p 11434:11434 ollama/ollama
```

Then you have to install the models you want to use. You can find the list of the models [here](https://ollama.com/models). We recommend to use the following models:

```sh
docker exec -it ollama ollama pull qwen2.5:7b
```

### Database

This project use PostgreSQL as database. You need to install it before running the project. You can find the installation instructions [here](https://www.postgresql.org/download/).

We recommend to use Docker to install it.

```sh
docker run --name postgres-data-battle -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=postgres -p 5432:5432 postgres:latest
```

### Backend

1. Go to the backend folder

```sh
cd backend
```
2. Create a virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
```

3. Install the requirements

```sh
pip install -r requirements.txt
```

4. Verify the `config/config.yml` file. You can change the database connection parameters if you choose different ones.

5. Create the tables in the database

```sh
python3 create_tables.py
```

6. Run the backend

```sh
fastapi dev
```

7. Open your browser and go to the following URL: [http://localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.

### Frontend

1. Go to the frontend folder

```sh
cd frontend
```

2. Install the requirements

```sh
npm install
```

3. Create `.env` file :

```sh
echo VITE_BASE_API_URL=http://localhost:8000 > .env
```

4. Run the frontend

```
npm run dev
```

5. Open your browser and go to the following URL: [http://localhost:5173](http://localhost:5173) to see the application.