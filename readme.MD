# Azure Fastapi Loader Template

**REQUIRES: `>=Python 3.9`**

### After Cloning
Run the following commands in the root directory.
```
$ py -m venv .venv
$ py -m pip install -r requirements.txt
```


## Usage
---
### Using Azure Functions
* Load into vscode with Azure Functions Plugin
* Press `F5` to launch and debug.
* Change/Add API functionality in `src/api`
    * To create a new API, just duplucate the sample api, the loader will automatically bootstrap it on start.
* To change the name and description, modify `app/init.py`
### Running directly
* Run the command in the root directory
* This gives you the ability to develop with hot reloading.
```
$ uvicorn app.init:app --reload
```


## Configuration
* Configuration can be found in `config.py`
* The precedence of looking for configuration values follows `.env -> environment_variables -> default value`
* You can ensure that the required configuration strings has been loaded by specifying a value as `internal.UNSET` and calling `cfg.has_unset()`

## Deployment
* Create an Azure function with and set the repo as a CI deployment source.
* Azure and Github will handle everything.