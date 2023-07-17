build:
	docker build --build-arg GITHUB_TOKEN=$(GITHUB_TOKEN) -t $(CONTAINER_REGISTRY)/$(GCP_PROJECT)/$(REPO_NAME):latest .

run:
	docker run -it --rm $(REPO_NAME):latest

push:
	@docker push $(CONTAINER_REGISTRY)/$(GCP_PROJECT)/$(REPO_NAME):latest
