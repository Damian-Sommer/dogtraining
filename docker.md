# Create Dogtraining Server Docker image:

```sh
docker build -t dogtraining:test -f dogtraining.Dockerfile .
```

# Run Dogtraining Server: 

```sh
docker run -v C:\\dev\\dogtraining\\test.db:/home/test.db -p 5555:50 -it dogtraining:test python -m dogtraining.server --connection=sqlite+aiosqlite:///home/test.db --frontend_host_url=http://localhost:8888 --port=50 --host=0.0.0.0
```

Dont add any slash at the end of the frontend_host_url parameter, if you do, the CORS header only applies this special url and not any other url part that has an addition at the end of the url. 

# Client: 

```sh
docker --debug build -t client:test -f client.Dockerfile .
```

```sh
docker run -p 8888:80 -it client:test
```
