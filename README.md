# co2-webservice
Webservice for WSN-CO2 Research


## How To Run
1. Set connection to database at 'config.py'
2. Run webservice by excuting 'run.py'

## Structure

```bash
.
|-- app
	|-- static
	|-- templates
	|-- __init__.py
	|-- forms.py
	|-- models.py
	|-- views.py
|-- db_repository
|-- flask
|-- tmp

```

## How To Use

### POST features
To add node :

```bash
curl -i -H "Content-Type: application/json" -X POST -d '{
"id":"(node ID-integer)",
"desc":"(node's description-string)",
"pos":"(node's position-string)"}' http://(server's IP address)/api/v01/post/node/add

```

To edit node :
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{
"id":"(insert node's ID that want to be edited-integer)",
"desc":"(new description-string)",
"pos":"(new position-string)"}' http://(server's IP address)/api/v01/post/node/edit

```

To delete node :
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{
"id":"(node's ID that want to be deleted-integer)"}' http://(server's IP address)/api/v01/post/node/delete

```
To modify node status :
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{
"id":"(node ID / 9999(to modify all nodes-integer) )",
"status":(desired status(0/1)-integer)}' http://(server's IP address)/api/v01/post/node/statchange

```

To add data :
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{
"id":"(node ID of data source)",
"timestamp":"(data timestamp)",
"co2":"(co2 data)",
"temp":"(temperature data)",
"hum":"(humidity data)",
"light":"(light intensity data)"}' http://(server's IP address)/api/v01/post/data/add

```

### GET features
To view available node in JSON :
```bash
http://(server's IP address)/api/v01/get/node

```

To view gathered data in JSON :
```bash
http://(server's IP address)/api/v01/get/data

```

To view gathered data for specific node in JSON :
```bash
http://(server's IP address)/api/v01/get/data/[node ID]

```

To download gathered data in CSV :
```bash
http://(server's IP address)/	

```