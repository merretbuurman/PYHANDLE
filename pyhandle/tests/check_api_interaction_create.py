'''
Little manual test script that uses pyhandle REST client to create
a handle record, to test the Handle Server's reaction/response for
various wrong / weird inputs.

Merret Buurman (DKRZ), 2021-02-11
'''

import pyhandle

# Handles to be created:
handle = '21.xxx/TESTTESTTEST'
credentials_file = "credentials_for_my_prefix.json"

###
### Start...
###
if __name__ == '__main__':

    creds = pyhandle.clientcredentials.PIDClientCredentials.load_from_JSON(
        credentials_file)
    client = pyhandle.handleclient.PyHandleClient('rest').instantiate_with_credentials(
        creds, HTTPS_verify=False)

    # Delete test handle before recreating it:
    try:
        client.delete_handle(handle)
    except Exception as e:
        print(e)

    # Which info to put into new record?
    record = []

    # Test adding the minimum and let the server add ttl and timestamp:
    # Works fine! Handle Server adds format "string".
    entry = {
        "index": 1,
        "type": "TEST",
        "data": "This was added without a specified format."
    }
    record.append(entry)

    # Test adding the minimum but with format:
    # Works fine! Format string is used all right.
    entry = {
        "index": 2,
        "type": "TEST",
        "data": {
            "format": "string",
            "value": "This was added with specified format 'string'."
        }
    }
    record.append(entry)

    # Test adding the minimum but with wrong format:
    # Fails!
    # Handle Server responds with:
    # Response from Handle Server: HTTP 400: {'responseCode': 4, 'message': 'com.google.gson.JsonParseException: java.text.ParseException: Unexpected type blabla'}
    #entry = {
    #    "index": 3,
    #    "type": "TEST",
    #    "data": {
    #        "format": "blabla",
    #        "value": "Is this format blabla?"
    #    }
    #}
    #record.append(entry)

    # Test specifying ttl
    # Works fine! ttl is set to 200
    entry = {
        "index": 4,
        "type": "TEST",
        "data": "This should have ttl 200.",
        "ttl": 200,
    }
    record.append(entry)

    # Test specifying timestamp, where timestamp is a wildly wrong value, unparseable, e.g. 66:99:99
    # Fails!
    # The timestamp is set to 2021-02-10T22:05:04Z
    # Response: b'{"responseCode":4,"message":"com.google.gson.JsonParseException: java.text.ParseException: Can\'t parse 1968-01-02T66:99:99Z"}'
    #entry = {
    #    "index": 5,
    #    "type": "TEST",
    #    "data": "This should have a timestamp from 1968.",
    #    "timestamp": "1968-01-02T66:99:99Z"
    #}
    #record.append(entry)

    # Test specifying a timestamp, a valid value:
    # We still end up with a wrong value: 2021-02-10T22:43:17Z
    # Does not raise error, but also not correct! This is mean: It obviously 
    # parses the timestamp, but then does not use it!!
    entry = {
        "index": 6,
        "type": "TEST",
        "data": "This should have a timestamp from 2017.",
        "timestamp": "2017-01-02T10:04:60Z"
    }
    record.append(entry)

    # Test adding any string as timestamp
    # Fails!
    # Response from Handle Server: HTTP 400: {'responseCode': 4, 'message': "com.google.gson.JsonParseException: java.text.ParseException: Can't parse BLABLABLA"}
    #entry = {
    #    "index": 7,
    #    "type": "TEST",
    #    "data": "This should have the timestamp 'BLABLABLA'.",
    #    "timestamp": "BLABLABLA"
    #}
    #record.append(entry)

    # Test adding two values at same index:
    # Fails!
    # Response from Handle Server: HTTP 409: {'responseCode': 201, 'message': 'Index conflict for 8', 'handle': '21.xxx/TESTTESTTEST'}
    #entry = {
    #    "index": 8,
    #    "type": "INDEXOVERRIDE_1",
    #    "data": "Added two entries with same index, this is first."
    #}
    #record.append(entry)
    #entry = {
    #    "index": 8,
    #    "type": "INDEXOVERRIDE_2",
    #    "data": "Added two entries with same index, this is second."
    #}
    #record.append(entry)

    # Test whether you can add without an index.
    # Fails!
    # Fails when creating HS_ADMIN entry, as then it looks for all indices.
    # TODO May have to test when HS_ADMIN is given.
    #entry = {
    #    "type": "TEST",
    #    "data": "This one has no index. It would have 9."
    #}
    #record.append(entry)

    # Test whether you can add with a string index.
    # Works fine: Index is like all other indices! HS seems to make it integer.
    entry = {
        "index": "10",
        "type": "TEST",
        "data": "This one has an index given as string '10'."
    }
    record.append(entry)

    # Test whether you can add without a type.
    # Fails, because library checks it!
    # KeyError / BrokenHandleRecordException
    # The Handle Server would not raise an error, but just omit this entry!
    #entry = {
    #    "index": 11,
    #    "data": "This one has no type."
    #}
    #record.append(entry)

    # Test whether you can add without a value.
    # Fails!
    # Response from Handle Server: HTTP 400: {'responseCode': 4, 'message': 'com.google.gson.JsonParseException: java.lang.NullPointerException'}
    #entry = {
    #    "index": 12,
    #    "type": "This one has no value."
    #}
    #record.append(entry)

    # Test adding the minimum but with wrong:
    # Fails!
    # Response from Handle Server: HTTP 400: {'responseCode': 4, 'message': 'com.google.gson.JsonParseException: java.text.ParseException: Unexpected type integer'}
    #entry = {
    #    "index": 13,
    #    "type": "TEST",
    #    "data": {
    #        "format": "integer",
    #        "value": "I specified format integer, but this value is not integer."
    #    }
    #}
    #record.append(entry)

    # Test whether, if we specify type Integer, and then really add an integer (in double quotes), whether is will be parsed.
    # Fails!
    # {"responseCode":4,"message":"com.google.gson.JsonParseException: java.text.ParseException: Unexpected type integer"}'
    #entry = {
    #    "index": 14,
    #    "type": "TEST_IS_INTEGER_PASSED_STR_666",
    #    "data": {
    #        "format": "integer",
    #        "value": "666"
    #    }
    #}
    #record.append(entry)

    # Test whether, if we specify type Integer, and then really add an integer (no quotes), whether is will be parsed.
    # Fails!
    # '{"responseCode":4,"message":"com.google.gson.JsonParseException: java.text.ParseException: Unexpected type integer"}'
    #entry = {
    #    "index": 15,
    #    "type": "TEST_IS_INTEGER_PASSED_INT_999",
    #    "data": {
    #        "format": "integer",
    #        "value": 999
    #    }
    #}
    #record.append(entry)

    # Test, will HS_ADMIN be created if none is passed?
    # Yes, it will, because our library does that.
    # Result:
    ###{
    ###"index": 100,
    ###"type": "HS_ADMIN",
    ###"data": {
    ###    "format": "admin",
    ###    "value": {
    ###        "handle": "0.NA/21.xxx",
    ###        "index": 200,
    ###        "permissions": "011111110011"
    ###    }
    ###},
    ###"ttl": 86400,
    ###"timestamp": "2021-02-10T22:43:17Z"
    ###}

    # Test whether we can change the permissions by manually creating
    # HS_ADMIN instead of letting the library do so:
    # Works fine!
    #hs_entry = {
    #    "index": 100,
    #    "type": "HS_ADMIN",
    #    "data": {
    #        "format": "admin",
    #        "value": {
    #            "handle": "0.NA/21.xxx",
    #            "index": 200,
    #            "permissions": "111111111111"
    #        }
    #    }
    #}
    #record.append(hs_entry)

    # Test whether we can change the permissions BACK by manually creating
    # HS_ADMIN instead of letting the library do so (well this only tests
    # whether we can delete the ones with the 111111111111 perissions, which
    # is a no-brainer, as that's very permissive permissions!)
    # Works fine!
    hs_entry = {
        "index": 100,
        "type": "HS_ADMIN",
        "data": {
            "format": "admin",
            "value": {
                "handle": "0.NA/21.xxx",
                "index": 200,
                "permissions": "011111110011"
            }
        }
    }
    record.append(hs_entry)

    # TODO Just curiosity: Some more possible HS_ADMIN tests (not urgent):
    # Don't test all this on a production prefix!
    # Test whether HS creates a handle without HS_ADMIN if the library does not create it.
    # Test create+modify handles which have no HS_ADMIN.
    # Test create+modify handles which have a different owner in HS_ADMIN.
    # Test create+modify handles which have only-zero permissions in HS_ADMIN.

    # Printing
    print('NEW RECORD:\n\n%s\n' % record)


    # Create:
    client.register_handle_json(
        handle,
        record,
        overwrite=False
    )

    print('Created. Check: hdl.handle.net/%s?noredirect' % handle)

    cont = input('Should we delete now? Type yyy! ')
    if cont == 'yyy':
        client.delete_handle(handle)



print('Bye!')

