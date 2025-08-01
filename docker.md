# Create Dogtraining Server Docker image:

```sh
docker build -t dogtraining:test -f dogtraining.Dockerfile .
```

# Run Dogtraining Server: 

```sh
docker run -v C:\\dev\\dogtraining\\test.db:/home/test.db -it dogtraining:test python -m dogtraining.server --connection=sqlite+aiosqlite:///home/test.db
```