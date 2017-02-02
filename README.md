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
	`-- views.py
|-- db_repository
|-- flask
 -- tmp

```

## How To Use

### GET features
To add node :

```bash
curl -i -H "Content-Type: application/json" -X POST -d '{
"id":"19",
"desc":"node bau",
"pos":"dimanaya"}' http://[server's IP address]/api/v01/post/node/add

```

To edit node :
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{
"id":"12",
"desc":"node bau diedit",
"pos":"dimanaya diedit"}' http://[server's IP address]/api/v01/post/node/edit

```

To delete node :
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{
"id":"19"}' http://[server's IP address]/api/v01/post/node/delete

```

To add data :
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{
"id":"19",
"timestamp":"yyyaaa",
"co2":"100",
"temp":"2020",
"hum":"3030",
"light":"4040"}' http://[server's IP address]/api/v01/post/data/add

```

### POST features
To view available node (output in JSON) :
```bash
http://[server's IP address]/api/v01/get/node

```

To view gathered data (output di JSON) :
```bash
http://[server's IP address]/api/v01/get/data

```

To view gathered data for specific node(output di JSON) :
```bash
http://[server's IP address]/api/v01/get/data/[node ID]

```

