# How makefiles work: https://opensource.com/article/18/8/what-how-makefile
# You have to use a makefile to build your and run your docker image. So, other
# person does not need to run this commands by hand

IMAGE_NAME ?= "fake-social-media"
IMAGE_TAG ?= "latest"
APP_PORT ?= 8000

build:
	@docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

run:
	@docker run --rm -p $(APP_PORT):$(APP_PORT) -e APP_PORT=$(APP_PORT) $(IMAGE_NAME):$(IMAGE_TAG)
