# Url Shortener
Project is to provide a simple url shortener service which associates slugs with urls.

## Components

### Website
Main access point to view mappings and add newones via an API.  This also supports Json rest inefaces
The server runs as a flask application, which is deployed into the container to run  under  gunicorn

### Interface
```python
Calls to get or post are in the following format
   'type': 'object',
    'anyOf':[ 
       {'required': ['slug']},
       {'required': ['url']} 
    ],
   'properties': {
       'slug': {
           'type': 'string',
       },
       'url': {
           'type': 'string',
       }
   },
```

* Flask service which runs under gunicorn.
* Using bootstrap for styling

### Backend
Mongo database - connection string supplied in .....


### Deployment
Build includes docker file.
Built to run as a google run service

### Dev Setup
To install, ensure **python 3.6** up, plus **pipenv**

To install
* [ ] `pipenv install`
* [ ] `pytest`

To Run
* [ ] Start the container, and the app will run, or
* [ ] gunicorn -b 0.0.0.0:8000 webserver:app


