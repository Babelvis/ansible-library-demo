# Ansible library demo

A small demonstration to show how you make a simple Ansible Module.

Bas Magré <bas.magre@babelvis.nl>

## Storyline

We have a simple api that can get, set, change and delete a key-value pair. The key must be a letter and the value a number. The api needs authentication with username and password or a token. See `Run demo api` for the complite definition.
In ansible we need to build a module that can set/get a charachter with a number and clear all charachters. This is what we need in the playbooks.

So we need:

- the arguments charachter and number (key and value)
- 3 actions in the module: set, get and clear
- authentication with username/password OR the use of a token
- an endpoint where the API can be accessed.

## Run demo api

There is a demo api in the folder `api-dotnet-src` we only need the run the docker container. But the source code is here if you want to see it.

```bash
cd api-dotnet-src
# build the docker image (already done)
# docker build . -t opvolger/demo-api-ansible
# push the docker image to docker hub (already done, only I can do this)
# docker push opvolger/demo-api-ansible
# run the docker container (you only need to do this)
docker run -p 5041:8080  opvolger/demo-api-ansible
```

Now you can visit the swagger interface of the demo api: [http://localhost:5041/swagger](http://localhost:5041/swagger)

## Developer Setup

Normally I do use a virtual environment, but since I only use standard modules/application that are already installed on my machine, I skip this now

There are 2 ansible modules `api_demo_start.py` and `api_demo.py`. The `api_demo_start.py` is a first setup with only the arguments and description of the module. The `api_demo.py` has the full interaction with the docker container.

### Python virtual environment

If you want to use python environments, you can do it

```bash
# setup of the virtual environment (only onetime)
python -m venv venv
# use the venv
source venv/bin/activate
# install required python libs (only onetime)
pip install ansible-core requests
```

### Debug modules

In vscode create file `.vscode/launch.json`

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: api_demo.py with Arguments",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/ansible-playbook/library/api_demo.py",
            "console": "integratedTerminal",
            "args": [
                "${workspaceFolder}/tests/arguments.json"
            ]
        },
        {
            "name": "Python Debugger: api_demo_start.py with Arguments",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/ansible-playbook/library/api_demo_start.py",
            "console": "integratedTerminal",
            "args": [
                "${workspaceFolder}/tests/arguments.json"
            ]
        }
    ]
}
```

and create `tests/arguments.json`

```json
{
    "ANSIBLE_MODULE_ARGS": {
        "endpoint": "https://127.0.0.1:5000/api/v1/",
        "character": "B",
        "number": 4,
        "action": "set"
    }
}
```

### Generate/Test Docs

```bash
# test doc generation
cd ansible-playbook
ANSIBLE_LIBRARY=./library ansible-doc -t module api_demo
```

## Run the module

```bash
cd ansible-playbook
# with ansible
ANSIBLE_LIBRARY=./library ansible -m api_demo -a 'endpoint=http://127.0.0.1:5041/ token=secret action=clear' localhost
# with ansible-playbook
ansible-playbook playbook-demo-start.yaml -vvv
ansible-playbook playbook-demo.yaml -vvv
```

## License

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
