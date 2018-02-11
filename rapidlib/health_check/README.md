### health_checker - A library to allow for automatic health checks.


#### Features

Exposes a function called check_health which receives a description of
the applicable tests which can be passed as yaml or json files or as a python
dictionary.  This function returns a description of the health of the system 
as a python dictionary.

#### Examples of health check descriptions:

###### yaml sample

```yaml
health_checks:
  check_redis_connection:
      callable: health_checks.check_redis
      parameters:
        server: localhost
        passwd: $PASSWORD
```

###### json sample
```json
{
   "health_checks":{
      "check_redis_connection":{
         "callable":"health_checks.check_redis",
         "parameters":{
            "host":"localhost",
            "passwd":"$PASSWORD"
         }
      }
}
```

###### python dict:

```python
health_checks = {
   "health_checks":{
      "check_redis_connection":{
         "callable":"health_checks.check_redis",
         "parameters":{
            "host":"localhost",
            "passwd":"$PASSWORD"
         }
      }
}
```

Example of a health check callable:
```python
def check_redis(server, passwd):
    """Applies a specific check.
    
    :parameter:  server
    :parameter:  passwd
    
    Specified in the health check description (yaml, json or dict) using the 
    parameters key.
    
    :returns: A python dictionary.
    """
```
You can now use this library using any of the supported formats (yaml - json - 
dict) to build a checker and call it using the returned function object:

```python
from rapidlib.health_check import check_health
from rapidlib.health_check import HealthCheckerError

try:
    health = check_health('health_check.yaml')
except HealthCheckerError as ex:
    print(ex)
```
 
 
```python
def verify_file_access(): 
    return "OK"

instructions = {
    'health_checks':
    {
        'file_access': 
        {
            'callable': 'verify_file_access'
        },
    }
}

from rapidlib.health_check import check_health

check_health(instructions)
```

```
Out[13]: 
{'status': False,
 'checks': {'file_access': {'status': False,
   'exception': 'HealthCheckerError ',
   'desc': ''}}}

```

#### Exception handling

This library is expected to raise only this exception: 

```
    HealthCheckerError
``` 
who's message explains the specific reason of failure.