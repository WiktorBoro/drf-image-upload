# Image upload based on django

# API capabilities
- Create Account Tier with the given parameters 
- Create Users with given account tier
- Get users list
- Get account tiers list
- Upload image for the user
- Get a list of photos and sizes (available for the account level) for, a given user
- Generate expiring binary image (if your account level allows it)

#Heroku deploy

Soon

# Quickstart

## Clone repository
`git clone https://github.com/WiktorBoro/rock-paper-scissors.git`

## Install the libraries
`pip install -r requirements.txt`

## Create superuser to access the database 
`python manage.py createsuperuser`

fill in the required fields

## Go to manage.py location
Run

`python manage.py runserver`

### Start celery worker 

for windows

`celery -A image_upload worker -l info --pool=solo`

and for macs

`celery -A image_upload worker -l info`

## Go to your local host 
http://127.0.0.1:8000/

## Admin site
http://127.0.0.1:8000/admin

# Endpoints

## 1. Users

Url: `/users`

### Method: GET

Obtains a list of all existing users.

Return a list of dictionary with all users with their account levels

Return example: 
```
[
    {
        "user_name":"<str: user name>", 
        "account_tier": "<str: account tier name>"
    }, 
....
]`
```
### Method: POST

Create new user

Body: 
```
{
    "user_name": "<str: user name>", 
    "account_tier": "<str: account tier name>"
}
```
Return dictionary with user_name and account tier key

Return example:
```
{
    "user_name": "Test", 
    "account_tier": "Basic"
}
```

### Method: GET
Get a list of photos and sizes (available for the account level) for, a given user

Url: `/users/<str: user-name>`

Return dictionary of dictionaries with the size of the images and a links to them

Return example: 
```
[
    {
        "image_name": "<str: image name>",
        "width": <int: original image width>,
        "height": <int: original image height>,
        "link": <str: link to original image OPTIONAL if the account permissions are appropriate>,
        "resize_images_list": [
            {
                "width": <int: resize image width>,,
                "height": <int: resize image height>,
                "resize_image": "<str: resize image link>"
            },
            ....
        ]
    },
    ....
]
```

## 2. Account tiers

Url: `/account-tiers`

### Method: GET

Obtains a list of all existing account tiers with permissions and available image sizes.

Return a list of dictionary with all account tiers with permissions and available image

Return example: 
```
[
    {
        "account_tier_name": "<str: account tier name>",
        "link_to_the_originally_uploaded_file": <boolean>,
        "ability_to_generate_expiring_links": <boolean>,
        "image_height": "<str: list in string with available image sizes>"
    },
    ....
]
```

### Method: GET

Url: `/account-tiers/<str: accoun tier name>`

Returns the data of one level of the account

Return example: 
```
{
        "account_tier_name": "<str: account tier name>",
        "link_to_the_originally_uploaded_file": <boolean>,
        "ability_to_generate_expiring_links": <boolean>,
        "image_height": "<str: list in string with available image sizes>"
    }
```

## 3. Image upload

Url: `/image-upload`

### Method: POST
Send a photo and give it a name for the chosen user

Body: 
```
{
    "user": "<str: user name>", 
    "image_name": "<str: name the image>", 
    "image": <object: image file>
}
```

Return example: 
```
{
    "image_name": "<str: image name>",
    "link": <str: link to original image OPTIONAL if the account permissions are appropriate>,
    "resize_images_list": [
            {
                "width": <int: resize image width>,,
                "height": <int: resize image height>,
                "resize_image": "<str: resize image link>"
            },
            ....
    ]
}
```

## 3. Generate expiring binary image

Url: `/expires-image`

### Method: POST

Specify the username, image name, and the expiration time, if you have sufficient account tier, the graphic will be generated which will expire after the specified time.

!Note the graphic must belong to the specified user

Body: 
```
{   
    "user": "<str: user name>", 
    "original_image": "<str: original image name>", 
    "image": <object: image file>
}
```

Return example: 
```
{
    "expiring_time": <int: expiring time>,
    "resize_image": "<str: link>"
}
```