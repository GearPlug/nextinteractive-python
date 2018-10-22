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

## Contributing
We are always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.
#### You can report any bug you find or suggest new functionality with a new [issue](https://github.com/GearPlug/nextinteractive-python/issues).
#### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/GearPlug/nextinteractive-python )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
