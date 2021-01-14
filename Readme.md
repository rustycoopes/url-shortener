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

### Datastore
This application uses a Mongo database (currently atlas) - connection string supplied in configuration files within the config folder.
File contents provide connection string, database name and collection name

### Logging
Logging is to **stdout**, and is using basic python logging.  For current deployment, this is reported to StackDriver

### Deployment
Build includes docker file **DockerFile**.
This project is currently built under Cloud Build and runs within google run.

### Dev Setup
To install, ensure **python 3.6** up, plus **pipenv**

To install
* [ ] `pipenv install`
* [ ] `pytest`

To Run
* [ ] Start the container, and the app will run  `docker run --rm -it  -p 8000:8000/tcp imagename`, or
* [ ] `gunicorn -b 0.0.0.0:8000 webserver:app`


