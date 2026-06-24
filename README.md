# CV Optimization Service

This service aims to optimize resumes for specific job descriptions. It uses ChromaDB and LangChain along with a LLM 
model to process the recruiting guidelines and the provided resume in order to generate a list of recommendations to 
improve the resume for an optional specific job description.

## Installation

Uses python 3.14

### Ollama

The project mainly uses Ollama for the LLM. There is untested code to use OpenAI, but that feature is untested.

### Using UV for local development

Use UV to sync dependencies

Run the project using uvicorn:

```uv run uvicorn app.main:app --host 0.0.0.0 --port 8000```

### Using Docker Compose

```docker compose up --build -d```

### Running with Docker

1. Build the Docker image:

```docker build -t cv-optimization:dev .```

2. Run the Docker container:

```
docker run --rm -p 8000:8000 \
  --add-host=host.docker.internal:host-gateway \
  -v $(pwd)/chroma:/data/chroma \
  -e LLM_PROVIDER=ollama \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e OLLAMA_LLM_MODEL=gemma4:e2b-mlx \
  -e OLLAMA_EMBEDDING_MODEL=nomic-embed-text \
  -e CHROMA_PATH=/data/chroma \
  cv-optimization:dev
```

## Generating vector database

Before running the service, you need to generate the vector database.
It processes all the resumes in the documents in the `knowledge` folder.

```python -m app.scripts.index_knowledge```

## Deploying with Kubernetes using Kind

This project was developed using Kind, the easiest way to deploy it is running:

1. Create cluster:

```kind create cluster --name cv-optimization```

2. Create namespace:

Note: Optional since there's a `namespace.yaml` file in the k8s folder.

```kubectl config use-context kind-cv-rag```

3. Grand docker hub access to the cluster:

```
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=****** \
  --docker-password=****** \
  --docker-email=******@gmail.com \
  -n cv-rag
```

4. Deploy the Kubernetes manifests:

```kubectl apply -f k8s/```

This assumes you have Kind and kubectl installed.
This also assumes Ollama is running locally, so it can communicate with it.

5. Verify the service is running:

- Check pods: ```kubectl get pods -n cv-rag```
- Check endpoints: ```kubectl get endpoints -n cv-rag```
- Check logs: ```kubectl logs deployment/cv-optimization -n cv-rag```

6. Expose the service:

```kubectl port-forward svc/cv-rag-service 8000:80 -n cv-rag```

## TODO

- [ ] Verify support for OpenAI
- [x] Add tests
- [x] Add CI/CD
- [ ] Add ingress (nginx vs traefik)
- [ ] Add traceability