# Oslo Cycle update

This application consumes the public API and reports all station statuses. The view is automatically refreshed each 10 seconds; the same refresh rate as the API.

## Requirements

* Python 3.9 with pip3
* pipenv  
  ```shell
  pip3 install --user pipenv
  ```

## Install

* Clone repository  
  ```shell
  git clone git@github.com:are3k/ocu.git
  cd ocu
  ```
* Initialize and install required Python packets in the virtual environment  
  ```shell
  pipenv shell && pipenv update
  ```

## Run application locally

```shell
export FLASK_APP=ocu
flask run
```
Access the application in your browser using [localhost port 5000](http://120.0.0.1:5000/) as address

