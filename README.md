# Point of Sale API for Restaurant Menu

Built with the most recent stable version of Python (3.9.0)


# Running the API

First make sure to go into the `.env-example` file and set the variables

Then you can use the utility script `util/start-docker.sh` to run the api. I have only tested this on an Ubuntu 20.04 Desktop

The URL will be `0.0.0.0:8000`

## Initializing container

Using the utility script (**Note** this script will delete any other containers, images & volumes you may have open. It also requires `docker-compose`, of course)

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

# First request: make sure the API is up

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

# Menu Routes

### Add a menu item

**Request**
Make the following request
```
POST 0.0.0.0:8000/add-item
```

Example raw payload:

```
{
    "item_id": "1",
    "description": "A royale with cheese",
    "price": "9.99",
    "quantity": "12"
}
```

Then if you try to add it again, you should get:

```
{
    "message": "Item with id '1' already exists"
}
```

**Expected Response**
```
{
    "added": {
        "item_id": 1,
        "price": 9.99,
        "quantity": 12,
        "description": "A royale with cheese"
    }
}
```

### Return a menu item

**Request**
Make the following request after creating the above item
```
GET 0.0.0.0:8000/menu/1
```

**Expected Response**
```
{
    "quantity": 12,
    "price": 9.99,
    "description": "A royale with cheese",
    "item_id": 1
}
```

### Update a menu item

**Note** I made the route so that PUT only works if the item exists. This way it won't create a new item if you input a new item id. This can easily be changed in the route though

**Request**
Make the following request, let's update the royale with cheese
```
PUT 0.0.0.0:8000/add-item
```

Example raw payload, note you must supply the entire payload including any fields you don't update

```
{
    "item_id": "1",
    "description": "NEW DESCRIPTION",
    "price": "19.99",
    "quantity": "42"
}
```

**Expected Response**
```
{
    "updated": {
        "price": 19.99,
        "quantity": 12,
        "description": "NEW DESCRIPTION",
        "item_id": 1
    }
}
```

Then if you do a GET to 0.0.0.0:8000/menu/1, you should see

```
{
    "price": 19.99,
    "quantity": 12,
    "description": "NEW DESCRIPTION",
    "item_id": 1
}
```

### Delete a menu item

**Request**
Make the following request, let's delete the royale with cheese

```
DELETE 0.0.0.0:8000/menu/1
```

**Expected Response**
```
{
    "message": "Item with id '1' deleted"
}
```

Then if you do a GET to 0.0.0.0:8000/menu/1, it should respond with

```
{
    "message": "Item '1' not found"
}
```

### List all items in the menu
**Request**

First add the following items using the `add-item` POST route:

```
{
    "item_id": "1",
    "description": "a royale with cheese",
    "price": "9.99",
    "quantity": "12"
}

{
    "item_id": "2",
    "description": "hamburger",
    "price": "7.99",
    "quantity": "20"
}

{
    "item_id": "3",
    "description": "fries",
    "price": "4.99",
    "quantity": "45"
}
```
Then make the following request

```
GET 0.0.0.0:8000/all-items
```

**Expected Response**

```
{
    "items": [
        {
            "quantity": 18,
            "description": "hamburger",
            "price": 7.99,
            "item_id": 2
        },
        {
            "quantity": 41,
            "description": "fries",
            "price": 4.99,
            "item_id": 3
        },
        {
            "quantity": 12,
            "description": "a royale with cheese",
            "price": 9.99,
            "item_id": 1
        }
    ]
}
```

# Order routes

### Add a new order

**Request**
Let's assume you still have the above 3 items in the menu. If you make a request to

```
POST 0.0.0.0:8000/add-order
```

With the following payload

```
{
    "payment_amount": "34.99",
    "order_note": "a bunch of food",
    "order_id": "1",
    "items": [
        {"item_id": "1", "quantity": "1", "order_id": "1"},
        {"item_id": "2", "quantity": "2", "order_id": "1"},
        {"item_id": "3", "quantity": "4", "order_id": "1"}
        ]
}
```

You will get the following output:

```
{
    "mesage": "Payment insufficient. Total due: $45.93, payment amount: $34.99,     remaining amount due: $10.939999999999998"
}
```

If you then change your payment amount to the correct amount, you should get:

```
{
    "added. order id": 1
}
```

**Additionally** it wouldn't be a complete POS system if the item quantities didn't update too. If you do a GET to menu/1 for example, you will see that the quantities are also changed

```
{
    "item_id": 1,
    "price": 9.99,
    "quantity": 11, # used to be 12
    "description": "a royale with cheese"
}
```

# Logging

There is custom logging built-into the code, it will log to the console directly. I chose to do it this way because when launching containers to GCP on Kubernetes it records the logs for you on the web platform. In dev logs are simply output to the console

# Testing

This was my first time writing tests, as usually in my current role QA handles that, we just try break the code and add the right exceptions. As such, I couldn't get POST tests with input data to work, so I only queried the endpoints

With the container running, in another tab run

```
./util/start-tests.sh
```

This will run tests, attempt to do test coverage, and do flake8 linting

# Notes on some design decisions

1. I chose to go with numerical IDs. There are benefits and drawdowns to this, but I kind of just wanted to get it working since it's easy to build an autoincrementing ID structure if it's just integers
2. 

# Things I would do differently next time

### Authentication

I overcomplicated things by trying to get jwt authentication working from the beginning. I thought to myself "hey, I've done complex JWT auth stuff in Express, this should be easy"

Well, adding `jwt_required` to my routes broke the routes, and after 3 days spent debugging I just decided to scrap it. 

However, I kept the `user` files, and if you would like to see where the authentication was working on the minimal app you can browse the files in this commit: 

### Production

I started by building out a CI/CD pipeline using GCP's cloudbuild (See `cloudbuild.yml` & `kubernetes-compose.yml`)

The idea was to use cloud build triggers on the main branch so that it would run automatically as a minimal yet pretty functional pipeline. However, with the authentication & whatnot I just got way too into building that and then realized I was 3 days in and didn't have any of the main functionality in the app yet!

The commit where this minimal app works in production is this one: 

There are also the following utility scripts that can be used inside GCP's cloudshell to build the kubernetes cluster fast:

`util/build-image.sh`
`util/build-cluster.sh`
