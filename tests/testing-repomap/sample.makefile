.PHONY: build test clean run lint docker-build docker-push

BINARY := bin/app
SRC := $(shell find . -name '*.go')

build: $(BINARY)

$(BINARY): $(SRC)
	go build -o $(BINARY) ./cmd/app

test:
	go test ./... -v -race -coverprofile=coverage.out

lint:
	golangci-lint run ./...

clean:
	rm -rf bin/ coverage.out

run: build
	./$(BINARY)

docker-build:
	docker build -t my-app:latest .

docker-push: docker-build
	docker push my-app:latest
