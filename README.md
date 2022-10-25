## Hello!

This is a Python/Flask API that lets you manage your files and directories. You can use this to query, create, edit, or delete a file or directory. 

### How to Run 

The guide below assumes you have Docker installed on your machine.

First, clone this github repo. 

From within the repo, run: 
```commandline
docker-compose up -d
docker exec -it directory-app bash
```
This will open a bash session within the container. In this session, you can launch the API using: 
```commandline
/bin/sh run.sh </your/root/path>
```

e.g., if you want to use the path that you are currently in as your root, then launch via:
```
/bin/sh run.sh /home/app_user
```

In another terminal window, launch another bash session within the container:
```commandline
docker exec -it weavegrid-app bash
```

You can now make API calls from this session. 

### API

This API supports GET, POST, PUT, and DELETE actions. 

#### GET endpoint
Returns name, owner, size, and permissions for each file or directory at a given path. If the path is a file, returns the contents of the file. If the path does not exist, returns a 400 status code.

Example usage: 
```commandline
curl http://127.0.0.1:5000/
```

Returns all files and directories under `/home/app_user/` (assuming that is the root).  

```commandline
curl http://127.0.0.1:5000/src
```

Returns all files and directories under `/home/app_user/src`.

```commandline
curl http://127.0.0.1:5000/requirements.txt
```

Returns the contents of the file.

#### POST endpoint
Creates a file or directory at a specified path. If structure already exists at that path, returns a 400 status code.

Users will need to specify the name and type ('file' or 'dir') of the new structure.

Example usage: 
```commandline
curl -X POST http://127.0.0.1:5000/ -d '{"name": "test_dir", "type": "dir"}' -H 'Content-Type: application/json'
```

Creates a new directory, `test_dir` in `/home/app_user/`.

```commandline
curl -X POST http://127.0.0.1:5000/ -d '{"name": "test_file.txt", "type": "file"}' -H 'Content-Type: application/json'
```

Creates a new file, `test_file.txt` in `/home/app_user/`.

```commandline
curl -X POST http://127.0.0.1:5000/src/ -d '{"name": "test_dir", "type": "dir"}' -H 'Content-Type: application/json'
```

Creates a new directory, `test_dir` in `/home/app_user/src/`.

```commandline
curl -X POST http://127.0.0.1:5000/ -d '{"name": "test_file.txt", "type": "file"}' -H 'Content-Type: application/json'
```

Creates a new file, `test_file.txt` in `/home/app_user/src/`.


#### PUT endpoint
Renames a structure. If the new structure does not exist, creates it. If the new structure already exists, returns a 400 error. 

Similar to POST, but users will need to specify the name of the old structure, `old_name`, the name of the new structure, `new_name`, and the type of the new structure ('file' or 'dir').

Example usage:
```commandline
curl -X PUT http://127.0.0.1:5000/src -d '{"old_name": "test_new1.txt", "new_name": "test_new2.txt", "type": "file"}' -H 'Content-Type: application/json'
```

Renames `/home/app_user/src/test_new1.txt` tp `/home/app_user/src/test_new2.txt`. 
```
curl -X PUT http://127.0.0.1:5000/src -d '{"old_name": "test_new1_dir", "new_name": "test_new2_dir", "type": "dir"}' -H 'Content-Type: application/json'
```

Renames `/home/app_user/src/test_new1_dir/` to `/home/app_user/src/test_new2_dir`. 

#### DELETE endpoint
Deletes a structure. If the structure does not exist, returns a 400 status code. 

Example usage:
```
curl -X DELETE http://127.0.0.1:5000/src/test_new1.txt  -H 'Content-Type: application/json'
```

Deletes `/home/app_user/src/test_new1.txt`. 

