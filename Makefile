PROJECT_ID = paparman
REPOSITORY = paparmane
IMAGE_NAME = paparmane
TAG = latest
GCR_URL = northamerica-northeast1-docker.pkg.dev

.PHONY: build
build:
	docker build -t $(GCR_URL)/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(TAG) .

.PHONY: push
push: build
	gcloud config set project paparman && docker push $(GCR_URL)/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(TAG)

.PHONY: cluster-auth
cluster-auth:
	gcloud container clusters get-credentials $(PROJECT_ID) --zone northamerica-northeast1 --project $(PROJECT_ID)

.PHONY: cluster-deploy
cluster-deploy:
	cd charts && helm package $(REPOSITORY) $(REPOSITORY) && helm upgrade $(REPOSITORY) $(REPOSITORY)

.PHONY: install-nats
install-nats:
	helm repo add nats https://nats-io.github.io/k8s/helm/charts/ && helm install nats nats/nats --namespace nats --create-namespace

.PHONY: install-nginx
install-nginx:
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx && helm install nginx-ingress ingress-nginx/ingress-nginx --namespace nginx --create-namespace