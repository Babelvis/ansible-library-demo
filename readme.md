# Ansible library demo

A small demonstration to show how you can deploy a web application on a Windows Server using Ansible.

Bas Magré <bas.magre@babelvis.nl>

## Build and publish demo api

```bash
docker build . -t opvolger/demo-api-ansible
docker push opvolger/demo-api-ansible
docker run -p 5041:8080  opvolger/demo-api-ansible
```

## Developer Setup

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
ANSIBLE_LIBRARY=./library ansible -m api_demo -a 'endpoint=https://127.0.0.1:5000/api/v1/ token=12345 action=clear' localhost
# with ansible-playbook
ansible-playbook playbook-demo.yaml -vvv
```

## License

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
