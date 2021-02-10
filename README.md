# PYHANDLE

PyHandle is a Python client library for interaction with a [Handle System](https://handle.net) server, providing basic create, read, update and delete capabilities for Handles. The library offers a client for the HTTP REST interface, a client that interacts directly with a Handle server SQL back-end and a client that creates customized Batch files.
The latter contain Batch operations, that can be performed using the GenericBatch command utility provided by the Handle System.

PyHandle currently supports Python >=3.5 (tested up to 3.8), and requires at least a Handle System server 8.1. The library requires OpenSSL v1.0.1 or higher. Python 2.7 and 3.5 used to be supported, but now the PyMysql dependencies fails (02/2021).

PyHandle is based on a prior development of the [EUDAT project](https://eudat.eu) under the name B2Handle.
As [B2Handle](https://github.com/EUDAT-B2SAFE/B2HANDLE) was developed with a specific scope - Handle operations in the EUDAT project - in mind, it has been improved and made more generic to cater to a broader audience.



# Installation

You can install the PyHandle library as follows:

```bash
git clone https://github.com/EUDAT-B2SAFE/PYHANDLE.git
cd PYHANDLE/
python setup.py install
```
 
The library is also available on PyPi and can be installed via pip:

```bash
 pip install pyhandle
```

For more information on the methods offered by the library, please consult the [technical documentation](http://eudat-b2safe.github.io/PYHANDLE).



# Link to documentation


Check out the documentation [here](https://eudat-b2safe.github.io/PYHANDLE/).

(You can find the source in the GitHub repository at [/docs/source/index.rst](./docs/source/index.rst)!)

## Building the documentation

For more details about the library you can build the documention using [Sphinx](http://www.sphinx-doc.org), requiring at least version 1.3. Sphinx and can be installed via pip. To build HTML documentation locally, then run:

```bash
python setup.py build_sphinx
```



# License

Copyright 2015-2021, Deutsches Klimarechenzentrum GmbH, GRNET S.A., SURFsara

   The PYHANDLE library is licensed under the Apache License,
   Version 2.0 (the "License"); you may not use this product except in 
   compliance with the License.
   You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


# Some usage notes

(to be migrated to documentation)

Instantiate:

```

credentials_file = './credentials/creds.json'
# Path must be relative to current working dir
# JSON file must contain absolute paths, or paths relative to the creds.json file!!

creds = pyhandle.clientcredentials.PIDClientCredentials.load_from_JSON(credentials_file)
client = pyhandle.handleclient.PyHandleClient('rest').instantiate_with_credentials(
        creds, HTTPS_verify=https_verify)
```


* `register_handle_kv(handle, **kv-pairs)` allows to pass (additionally to the handle name) key-value pairs.

* `register_handle_json(handle, list_of_entries, ...)` allow to pass JSON snippets instead of key-value pairs, so you can specify the indices. An entry looks like this: `{'index':index, 'type':entrytype, 'data':data}`. This is the format in which the changes are communicated to the handle server via its REST interface. An entry of type `HS_ADMIN` will be added if you do not provide one.

* `register_handle(...)` allows to pass (additionally to the handle name) a mandatory URL, and optionally a CHECKSUM, and more types as key-value pairs. Old method, made for legacy reasons, as this library was created to replace an earlier library that had a method with specifically this signature.

* `generate_and_register_handle(prefix, ...)` is a similar legacy method. Instead, just use `generate_PID_name(prefix)` to create a handle name and use one of the above. 



## JSON formats: Retrieval

You can retrieve handle records in three ways:

1. `requests.get('http://hdl.handle.net/api/handles/prefix/suffix').json()`
2. `pyclient.retrieve_handle_record_json('prefix/suffix')`
3. `pyclient.retrieve_handle_record('prefix/suffix')`


The first two methods return a JSON object with:

* `resposeCode`
* `handle`
* `values`, which is a list of JSON objects (_entries_) that represent KV pairs that a record consists of, but with some more info:

```
{
'index': 1,
'type': 'URL', 
'data':
   {
   'format': 'string',
   'value': 'https://abd.def/000120_EBL_V0.xlsx'
   }, 
'ttl': 86400, 
'timestamp': '2021-01-25T08:05:01Z'
}
```

In case the type is `HS_ADMIN`, then the entry looks a bit different:

```
{
'index': 100,
'type': 'HS_ADMIN',
'data': 
   {
   'format': 'admin', 
   'value': 
      {
      'handle': '0.NA/21.123456',
      'index': 200,
      'permissions': '011111110011'
      }
   },
'ttl': 86400,
'timestamp': '2021-01-25T08:05:01Z'
}
```

The third method returns a simple key-value dictionary, stripped off the index, ttl and timestamp. (Here, `HS_ADMIN` is simply represented as a string):

```
{
   'URL': 'https://abd.def/000120_EBL_V0.xlsx',
   'key1': 'value1',
   'key2': 'value2',
   'key3': 'value3',
   'HS_ADMIN': "{'handle': '0.NA/21.T12996', 'index': 200, 'permissions': '011111110011'}"
}
```


Example:

```
#resp = requests.get('http://hdl.handle.net/api/handles/21.T123456/0610bd95ee41a13')
#resp.json()

#record = pyclient.retrieve_handle_record_json('21.T123456/0610bd95ee41a13)
#record

{
   'responseCode': 1,
   'handle': '21.T123456/0610bd95ee41a13',
   'values': [
      {
      'index': 1,
      'type': 'URL', 
      'data':
         {
         'format': 'string',
         'value': 'https://abd.def/000120_EBL_V0.xlsx'
         }, 
      'ttl': 86400, 
      'timestamp': '2021-01-25T08:05:01Z'
      }, 
      {
      'index': 2, 
      'type': 'CHECKSUM',
      'data': 
         {
         'format': 'string', 
         'value': '575b8540896e202082c9cf4'
         }, 
      'ttl': 86400,
      'timestamp': '2021-01-25T08:05:01Z'
      },
      ...
      {
      'index': 100,
      'type': 'HS_ADMIN',
      'data': 
         {
         'format': 'admin', 
         'value': 
            {
            'handle': '0.NA/21.T12996',
            'index': 200,
            'permissions': '011111110011'
            }
         },
      'ttl': 86400,
      'timestamp': '2021-01-25T08:05:01Z'
      }
   ]
}

#record = pyclient.retrieve_handle_record('21.T123456/0610bd95ee41a13)
#record

{
   'URL': 'https://abd.def/000120_EBL_V0.xlsx',
   'CHECKSUM': '575b8540896e202082c9cf4',
   'HS_ADMIN': "{'handle': '0.NA/21.T12996', 'index': 200, 'permissions': '011111110011'}"
}
```


## JSON formats: Upload

When uploading, you can pass the values as key-value-pairs, or as JSON snippets. The former selects indices for you. The latter allows you to also specify _index_ and optionally _ttl_ and _HS_ADMIN_.


Simple kv pairs:

```
kv_pairs = {
   'URL': 'https://abd.def/000120_EBL_V0.xlsx',
   'CHECKSUM': '575b8540896e202082c9cf4',
   'key': 'value'
}
pyclient.register_handle_kv(handle, overwrite=True, **kv_pairs)
# TODO TEST

* This will always add a `HS_ADMIN` entry (as you cannot specify such an entry in this simple format, and we mustn't have handles without it).
```

JSON, more complex:

```
list_of_entries = [
   {'index': 1, 'type': 'URL',      'data': 'https://abd.def/000120_EBL_V0.xlsx'},
   {'index': 2, 'type': 'CHECKSUM', 'data': '575b8540896e202082c9cf4'},
   {'index': 3, 'type': 'key',      'data': 'value', 'ttl':86400}
]
pyclient.register_handle_json(handle, overwrite=False, list_of_entries)
```
* You can optionally add a ttl (TODO: integer, right?). If not, the default is used by the Handle Server (TODO is is usually 86400, apparently).
* You can also use the more complex _data_: `{'data': {'format': 'string', 'value': '575b854089'}}` instead of `{'data': '575b854089'}`. I THINK. TODO. ALSO CHECK IF integers are recognized.
* An entry of type `HS_ADMIN` with some default values (can be customized) will be added if you do not provide one:
```
   {
   'index': 100,
   'type': 'HS_ADMIN',
   'data':
      {
      'value':
         {
         'index': '200',
         'handle': '0.NA/prefix',
         'permissions': '011111110011'
         },
      'format':'admin'
      }
   }
```


# How to run the unit tests

The simplest way (tested with python 3.7.1):

```bash
python setup.py test
```

(More info in the GitHub repository at [./pyhandle/tests/README.md](./pyhandle/tests/README.md)!)

To quickly test different versions using docker (see [./pyhandle/tests/testdockers](./pyhandle/tests/testdockers)):

```
today=`date +%m%d%Y`
version="1.x.x" # pyhandle version, e.g. 1.0.4

docker build -t temp_pyhandle:36_$version_$today -f pyhandle/tests/testdockers/Dockerfile36 . 
docker run  -it --rm temp_pyhandle:36_$version_$today python setup.py test

docker build -t temp_pyhandle:37_$version_$today -f pyhandle/tests/testdockers/Dockerfile37 . 
docker run  -it --rm temp_pyhandle:37_$version_$today python setup.py test

docker build -t temp_pyhandle:38_$version_$today -f pyhandle/tests/testdockers/Dockerfile38 . 
docker run  -it --rm temp_pyhandle:38_$version_$today python setup.py test
```

There are also Dockerfiles in [./pyhandle/tests/testdockers](./pyhandle/tests/testdockers), but they are not documented and fail.

# TODO Fix these Dockerfiles eventually, or update to functioning versions.

```
# build successful, but fails to run:
docker build -t eudat-pyhandle:py3.5 -f Dockerfile-py3.5 .
cd ./pyhandle/tests
docker build -t temp:temp -f Dockerfile-py3.5 .
docker run -it --rm temp:temp

# build fails:
docker build -t eudat-pyhandle:py2.6 -f Dockerfile-python2.6 .
```


For coverage (in python 3):

```
pip install coverage
coverage erase
coverage run --include=pyhandle/* --branch -m pyhandle.tests.main_test_script
coverage run --omit=pyhandle/tests/* --branch -m pyhandle.tests.main_test_script
coverage html -i
#tar cfvz htmlcov.tar htmlcov
#tar xfvz htmlcov.tar 
firefox htmlcov/index.html
```
Please note that the REST client has decent unit test coverage, while the other clients have much less test coverage.



# Github contributions

Devs:

* Please make contributions based on the devel branch, then issue a PR to the devel branch.
* Small contributions (e.g. typos, README, ...) can be pushed directly to devel if you have permissions.

Owners:

* Run unit tests on PR
* Merged PR into devel
* If/when changes are ready for a next release, bump the version number (no PR, but push directly to the repo)
* Run unit tests again on this devel branch.
* Merge devel into master (no PR, directly merge them **with --no-ff to keep history** and push to master)
* Add "-dev" to the incremented version number on devel
* Send release to pypi: 

```
virtualenv venv 
source venv/bin/activate
pip install pypandoc
python setup.py sdist upload -r pypi

# TODO: Deprecated, move to twine!
```


