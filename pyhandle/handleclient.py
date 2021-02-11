'''
This module provides the main client for the PYHANDLE
    library.
'''
from __future__ import absolute_import

import logging
import pyhandle
import requests

from pyhandle.client.batchhandleclient import BatchHandleClient
from pyhandle.client.dbhandleclient import DBHandleClient
from pyhandle.client.resthandleclient import RESTHandleClient
from . import util

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(util.NullHandler())
REQUESTLOGGER = logging.getLogger('log_all_requests_of_testcases_to_file')
REQUESTLOGGER.propagate = False
REQUESTLOGGER.addHandler(util.NullHandler())


class PyHandleClient(object):
    ''' PYHANDLE main client class '''

    HANDLE_CLIENTS = [DBHandleClient, RESTHandleClient, BatchHandleClient]
    ALLOWED_CLIENT_TYPES = ['rest', 'db', 'batch']

    def __init__(self, client_type, mysql_credentials=None, batch_file_path=None):
        '''
        Initialize a REST or Db client.

        :param client_type: A string that can be 'rest' or 'db' or 'batch'
        :param mysql_credentials: Optional: key-value pairs to specify credentials for the MySQL database.
        '''
        # TODO: The mysql-credentials should not be passed to this generic
        # class, but hidden in a subclass.

        if client_type in self.ALLOWED_CLIENT_TYPES:
            self.type = client_type # TODO Rename to client_type to avoid confusion.
            self.credentials = mysql_credentials # TODO Rename to mysql_credentials to avoid confusion.
            self.batch_file_path = batch_file_path
            self.handle_client = self.select_handle_client()
        else:
            raise ValueError("Allowed client types: %s" % self.ALLOWED_CLIENT_TYPES)

    def select_handle_client(self):
        '''
        Instantiate REST, DB or Batch client.
        :return: Instance of the client.
        '''

        for ClientSubclass in self.HANDLE_CLIENTS:

            # Find the correct client for our type:
            if ClientSubclass.is_this_correct_client_type(self.client):

                # Depending on the client type, pass different args.
                # TODO: Shouldn't this kind of difference be hidden in subclass?
                # Like this, we would not need the check_client method, we could
                # just call the relevant subclass by name.
                if self.client == 'db':
                    return ClientSubclass(self.credentials)
                elif self.client == 'batch':
                    return ClientSubclass(batch_file_path=self.batch_file_path)
                else:
                    return ClientSubclass()

    def create_batch_file(self, overwrite=False):
        return self.handle_client.create_batch_file(overwrite)

    def instantiate_for_read_access(self, **config):
        return self.handle_client.instantiate_for_read_access(**config)

    def instantiate_with_credentials(self, credentials, **config):
        return self.handle_client.instantiate_with_credentials(credentials, **config)

    def instantiate_with_username_and_password(self, handle_server_url, username, password, **config):
        return self.handle_client.instantiate_with_username_and_password(handle_server_url, username, password,
                                                                         **config)

    def instantiate_for_read_and_search(self, handle_server_url, reverselookup_username, reverselookup_password,
                                        **config):
        return self.handle_client.instantiate_for_read_and_search(handle_server_url, reverselookup_username,
                                                                  reverselookup_password, **config)

    def retrieve_handle_record_json(self, handle):
        return self.handle_client.retrieve_handle_record_json(handle)

    def retrieve_handle_record(self, handle, handle_record_json=None):
        return self.handle_client.retrieve_handle_record(handle, handle_record_json)

    def get_value_from_handle(self, handle, key, handle_record_json=None):
        return self.handle_client.get_value_from_handle(handle, key, handle_record_json)

    def modify_handle_value(self, handle, **kvpairs):
        self.handle_client.modify_handle_value(handle, **kvpairs)

    def delete_handle_value(self, handle, key):
        self.handle_client.delete_handle_value(handle, key)

    def delete_handle(self, handle):
        self.handle_client.delete_handle(handle)

    def generate_and_register_handle(self, prefix, location, checksum=None, **extratypes):
        return self.handle_client.generate_and_register_handle(prefix, location, checksum, **extratypes)

    def register_handle(self, handle, location, overwrite=False, **extratypes):
        return self.handle_client.register_handle(handle, location, overwrite, **extratypes)

    def search_handle(self, pattern=None, **args):
        return self.handle_client.search_handle(pattern, **args)

    def search_handle_multiple_keys(self, **args):
        return self.handle_client.search_handle_multiple_keys(**args)

    def authenticate_seckey(self, user, password):
        self.handle_client.authenticate_seckey(user, password)

    def authenticate_pubkey(self, user, priv_key_path, pass_phrase=None):
        self.handle_client.authenticate_pubkey(user, priv_key_path, pass_phrase)

    def authenticate_with_credentials(self, credentials, auth_type):
        self.handle_client.authenticate_with_credentials(credentials, auth_type)

    def get_query_from_user(self, query):
        return self.handle_client.get_query_from_user(query)

    def list_all_handles(self):
        return self.handle_client.list_all_handles()

    def check_if_handle_exists(self, handle):
        return self.handle_client.check_if_handle_exists(handle)

    def __get_handle_record_if_necessary(self, handle, handlerecord_json):
        return self.handle_client.__get_handle_record_if_necessary(handle, handlerecord_json)

    def pretty_print(self, record):
        return self.handle_client.pretty_print(record)

    def register_handle_batch(self, handle, url, hdl_admin_index, admin_handle, perm):
        return self.handle_client.register_handle_batch(handle, url, hdl_admin_index, admin_handle, perm)

    def add_handle_value(self, handle, **kvpairs):
        self.handle_client.add_handle_value(handle, **kvpairs)
