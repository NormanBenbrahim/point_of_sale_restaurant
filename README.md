# Point of Sale API for Restaurant Menu

Built with Python 3.9.0 + Docker 20.10.10 + Postgres 14.0

API tested on an Ubuntu 20.04 Desktop 

# Setup

First get the files

```
git clone https://github.com/NormanBenbrahim/point_of_sale_restaurant
cd point_of_sale_restaurant
```

Then make sure to go into the `.env-example` file and set the variables. Then `mv .env-example .env`

## Initializing container

Using the utility script (**Note** this script will delete any other containers, images & volumes you may have open. It also requires `docker-compose` of course)

```
./util/start-docker.sh
```

This builds everything from scratch

If you want to build from cache after the first time you run the above script, just add a command line argument (any argument string will work, I like to use `c`)

```
./util/start-docker.sh c
```

There is also a `cleanup.sh` script that you can use to clean your system of any dangling images that may slow down your system

# Calling the API

In Postman you can use the following routes, and each payload should be added in the raw field with JSON selected as input

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

**Note** I made the route so that PUT only works if the item exists. This way it won't create a new item if you input a new item id, so that the restaurant doesn't accidentally accept orders if they don't actually have enough stock

**Request**

Make the following request, let's update the royale with cheese
```
PUT 0.0.0.0:8000/menu/1
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

First add the following 3 items using the `POST /add-item` route:

```
{
    "item_id": "1",
    "description": "a royale with cheese",
    "price": "9.99",
    "quantity": "12"
}
```

```
{
    "item_id": "2",
    "description": "hamburger",
    "price": "7.99",
    "quantity": "20"
}
```

```
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
            "item_id": 1,
            "description": "a royale with cheese",
            "quantity": 12,
            "price": 9.99
        },
        {
            "item_id": 2,
            "description": "hamburger",
            "quantity": 20,
            "price": 7.99
        },
        {
            "item_id": 3,
            "description": "fries",
            "quantity": 45,
            "price": 4.99
        }
    ]
}
```

If you make the request while there are no items on the menu it will return
```
{
    "items": []
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

You will get a similar message if there is an overpayment in the request, or not enough quantity in the menu for the menu items

**Additionally** it wouldn't be a complete POS system if the item quantities didn't update too. After you add the order, if you do a GET to menu/1 for example, you will see that the quantities are also changed

```
{
    "item_id": 1,
    "price": 9.99,
    "quantity": 11, # used to be 12
    "description": "a royale with cheese"
}
```

### Return an order


**Request**

Make the following request after creating the above order
```
GET 0.0.0.0:8000/order/1
```

**Expected Response**
```
{
    "payment_amount": 45.93,
    "items": [
        {
            "item_id": 1,
            "quantity": 1,
            "order_id": 1
        },
        {
            "item_id": 2,
            "quantity": 2,
            "order_id": 1
        },
        {
            "item_id": 3,
            "quantity": 4,
            "order_id": 1
        }
    ],
    "order_id": 1,
    "order_note": "a bunch of food"
}
```

### Get all the orders

**Request**

Make the following request after creating orders
```
GET 0.0.0.0:8000/all-orders
```

**Expected Response**
```
{
    "orders": [
        {
            "payment_amount": 45.93,
            "order_note": "a bunch of food",
            "order_id": 1,
            "items": [
                {
                    "item_id": 1,
                    "order_id": 1,
                    "quantity": 1
                },
                {
                    "item_id": 2,
                    "order_id": 1,
                    "quantity": 2
                },
                {
                    "item_id": 3,
                    "order_id": 1,
                    "quantity": 4
                }
            ]
        }
    ]
}
```

### Deleting an order

**Request**

Make the following request after creating the above order
```
DELETE 0.0.0.0:8000/order/1
```

**Expected Response**
```
{
    "message": "Order with id '1' deleted"
}

```

I did not implement re-adding the item quantities after deleting the order, this was difficult and I wanted to hand something in within a reasonable time. The update route for orders also doesn't have this logic

However, given enough time I'm sure I could figure it out

# Logging

There is custom logging built-into the code, it will log to the console directly. I chose to do it this way because when launching containers to GCP on Kubernetes it records the logs for you on the web platform. In dev logs are simply output to the console

# Testing

This was my first time writing tests, in my current role QA handles that. We just try break the code and add the right exceptions. As such, I couldn't get POST tests with input data to work, so I only queried the endpoints

With the container running, in another tab run

```
./util/start-tests.sh
```

This will run tests, attempt to do test coverage, and do flake8 linting

# Notes on some design decisions

1. I chose to go with numerical IDs. There are benefits and drawdowns to this, but I kind of just wanted to get it working since it's easy to build an autoincrementing ID structure if it's just integers
2. Python 3.9 was released Oct 4 2021. When I download new packages (e.g. `flask`), I go into the release history and include the version that is released either on the same date (Oct 4 2021) or earlier. While this isn't bulletproof, it ensures you are working with compatible packages
3. When adding new "lego blocks" on top of flask, I chose to use an `extensions.py` file, with a method at the bottom of `api.py` which loads them all up. This way you can create custom error outputs and stuff and be able to edit everything in one place
4. I tried to make as many things as possible get called from `config/settings.py` (or `instance/settings.py` in prod) so that it is easy to update things
5. I had to use a custom `Nested` field for creating the orders table, see `app/schemas/orders.py` for more details. I believe this is still an outstanding issue for the marshmallow team, but maybe I am overthinking it

# Things I would do differently next time

### Authentication

I overcomplicated things by trying to get jwt authentication working from the beginning. I thought to myself "hey, I've done complex JWT auth stuff in Express, this should be easy"

Well, adding `jwt_required` to my routes broke the routes, and after 3 days spent debugging I just decided to scrap it

However, I kept the `user` files, and if you would like to see where the authentication was working on the minimal app you can browse the files in this commit: https://github.com/NormanBenbrahim/point_of_sale_restaurant/tree/be00081993bb62ab5c9999e18fb187164e036b02

### Production

I started by building out a CI/CD pipeline using GCP's cloudbuild (See `cloudbuild.yml` & `kubernetes-compose.yml`)

The idea was to use cloud build triggers on the main branch so that it would run automatically as a minimal yet pretty functional pipeline. However, with the authentication & whatnot I just got way too into building that and then realized I was 3 days in and didn't have any of the main functionality in the app yet!

The commit where this minimal app works in production is this one: https://github.com/NormanBenbrahim/point_of_sale_restaurant/tree/1d9d8a00a68a9674a2811304e4551ebb7aedba88

There are also the following utility scripts that can be used inside GCP's cloudshell to build the kubernetes cluster fast:

`util/build-image.sh`
`util/build-cluster.sh`

In general this is how I am used to working. Any new features need a feature branch, and that branch gets pulled into `development` branch, where a senior dev evaluates it, then pushes to `main` where we have auto-builders

# End

![meme](https://github.com/NormanBenbrahim/point_of_sale_restaurant/blob/add-testing/tmp/Untitled.png?raw=true)