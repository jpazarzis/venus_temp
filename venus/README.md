###health_checker - A library to allow for automatic health checks.


####Features

Exposes a function called make_health_checker which receives a description of
the applicable tests which can be passed as yaml or json files or as a python
dictionary.  This function returns a function object which can be called using
the () notation to run all the health checks and return the applicable status
as a python dictionary.

Examples of health check descriptions:

yaml sample: health_check.yaml

```
health_checks:
  check_redis_connection:
      callable: health_checks.check_redis
      parameters:
        server: localhost
        passwd: $PASSWORD
```

json sample: health_check.json
```
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

python dict sample:

```
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
```
def check_redis(server, passwd):
    # Apply your checks and return a dict
```
You can now use this library using any of the supported formats (yaml - json - 
dict) to build a checker and call it using the returned function object:

```
checker = make_health_checker('health_check.yaml')
health_check = checker()
``` 

####Exception handling

This library is expected to raise only this exception: 

```
    HealthCheckerError
``` 
who's message explains the specific reason of failure.