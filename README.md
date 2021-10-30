# Point of Sale API for Restaurant Menu

Built with the most recent stable version of Python (3.9.0)


# Running the API

First make sure to go into the `.env-example` file and set the variables

Then you can use the utility scripts  in `util/` to run the api. I have only tested this on an Ubuntu 20.04 Desktop

The URL will be `0.0.0.0:8000`


## Without a container

Inside your python 3.9.0 virtual environment run

```
mv .env-example
.env
pip install -r requirements-dev.txt
./util/start-dev.sh
```

## With a container

Ensure you have `docker-compose` installed and please be advised that **this script will delete any other containers you may have open**

```
mv .env-example
.env
./util/start-docker.sh
```

This builds everything from scratch

If you want to build from cache after the first time you run the above script just add a command line argument (any argument string will work, I like to use `cache`)

```
./util/start-docker.sh cache
```

There is also a `cleanup.sh` script that you can use to clean your system of any dangling images that may slow down your system


# Calling the API

In Postman you can use the following routes:

### Make sure the API is up

**Request**
Make the following request
```
GET 0.0.0.0:8000/
```

No payload required

**Expected Response**
```
{
    "status": "up",
    "uptime": "2021-10-30 08:58:32"
}
```
