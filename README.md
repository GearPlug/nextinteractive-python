# nextinteractive-python
Python wrapper for NextInteractive API
## Installing
```
git+git://github.com/GearPlug/nextinteractive-python.git
```

## Usage

- Instantiate client
```
from client import Client
client=Client(user=USER, passwd=PASSWORD)
```
- The use of the client is quite simple, just call each method with its respective arguments
(if required) to obtain the corresponding response from the endpoint in the API:
`client.method(args)`
e.g. `client.create_template(template_name, custom_fields)`

