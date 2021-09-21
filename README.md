# zemmourify

## Setup env

Install dependencies
```bash
make init
```

Some useful commands
```bash
make test       # run coverage tests
make            # get all commands
```
## Docker

The Dockerfile is parametrized with two config: DEV and PROD

**Build**
```
make docker-build         # build DEV docker image  (name: zemmourify_LOCAL)
make docker-prod-build    # build PROD docker image (name: zemmourify)
```

**Test**
```
make docker-test          # run tests in DEV image
make docker-prod-test     # run tests in PROD image
```

**Interactive console**
```
make docker-exec cmd=zsh args="-p 80:80 -p 8501:8501 -p 8000:8000"
```
### Use vscode inside container

Setup
```bash
mkdir -p .devcontainer && cp .vscode/devcontainer.tpl.json .devcontainer/devcontainer.json
```

In vscode: <kbd>CMD</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> then select *Remote-Containers: Reopen in Container*

To rebuild vscode container: <kbd>CMD</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> then select *Rebuild...*