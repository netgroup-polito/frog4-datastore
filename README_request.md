# Request examples

## Nf_Configuration

  POST /nf_configuration/{user_id}/{configuration_id}
  ``` json
  {
    "yang_id": "nat",
    "configuration":{
        "ip_address": "10.0.0.1",
        "netmask": "255.255.255.0"
     }
  }
  ```
## User
  POST /user
  ``` json
  {
    "username": "admin",
    "password": "root"
  }
  ```
  
  POST /user/login
  ```json
  {
    "username": "admin",
    "password": "root"
  }
  ```
  ## VNF_Instance
  PUT /vnf/{instance_id}/bootconfiguration
  ```json
  {
    "configuration_id": "nat-config",
    "user_id": "admin"
  }
  ```
