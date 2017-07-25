# Request examples

## Nf_Configuration

  POST /nf_configuration/{user_id}/{configuration_id}
  ```
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
  ```
  {
    "username": "admin",
    "password": "root"
   }
  ```
  
  POST /user/login
  ```
  {
    "username": "admin",
    "password": "root"
   }
  ```
  ## VNF_Instance
  PUT /vnf/{instance_id}/bootconfiguration
  ```
  {
    "configuration_id": "nat-config",
    "user_id": "admin"
   }
  ```
