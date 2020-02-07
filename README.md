# random.webteam.space
This is the repo for the [website](random.webteam.space).

## run it locally

After [installing Docker](https://docs.docker.com/install/):

``` bash
./run
```

And browse to http://127.0.0.1:8080.

## Play with it

The pages should be able to serve JSON if the `Content-Type: application/json` is requested in the headers.

``` bash
curl -s -H 'Content-Type: application/json' "http://localhost:8080"
```
