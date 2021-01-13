# src/app/validation.py

from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

# https://pythonhosted.org/Flask-Inputs/#module-flask_inputs
# https://json-schema.org/understanding-json-schema/
# we want an object containing a required greetee  string value
shortener_schema = {
   'type': 'object',
    'oneOf':[ 
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
}


class ShortenerInputs(Inputs):
   json = [JsonSchema(schema=shortener_schema)]


def validate_shortener_request(request):
   inputs = ShortenerInputs(request)
   if inputs.validate():
       return None
   else:
       return inputs.errors