build:
	docker build --build-arg GITHUB_TOKEN=$(GITHUB_TOKEN) -t githuber .

run:
	docker run -it --rm githuber

docker_push:
	@docker push $(CONTAINER_REGISTRY)/$(GCP_PROJECT)/$(REPO_NAME):latest

docker_deploy:
	@gcloud config set project $(GCP_PROJECT)
	@gcloud run deploy tiniworld --image $(CONTAINER_REGISTRY)/$(GCP_PROJECT)/$(REPO_NAME):latest --platform managed --region $(REGION) --allow-unauthenticated
