# chatBot

all to all chat

## Quick start


Build image :
```shell
docker build -t mychat .
```

Deploy container :
```shell
docker run -d --env-file .env --name mycontainer -p 8000:80 mychat
```

app_url : http:localhost:8000

print running logs :
```shell
 docker logs -f mycontainer
```


stop and remove container :
```shell
docker stop mycontainer
docker rm mycontainer
```

