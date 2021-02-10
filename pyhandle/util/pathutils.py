import os

def get_absolute_path(path, file_path_string):
    '''
    Used for getting the absolute path of the key and
    certificate used as credentials.

    The argument "path" contains the path to the
    private key or certificate, as provided by the user
    in the JSON file. It can be absolute or relative 
    **to where the JSON file is located**!

    "certificate_and_key": "./21.T12996_certificate.pem"
    "private_key": "./21.T12996_privkey.pem"
    "certificate_only": "./21.T12996_certificate_only.pem"

    The argument "file_path_string" contains the path to
    the JSON file itself.


    Developer's note:
    It's used in `pyhandle/clientcredentials.py`, during
    `PIDClientCredentials.load_from_JSON(json_filename)`.

    `file_path_string` is the location of the JSON file as
    stored in `self.__credentials_filename`, which is filled
    with whatever the user passed in `load_from_json(...)`.

    `path` is one of `self.__certificate_only` or 
    `self.__private_key` or `self.__certificate_and_key`, which
    are simply the contents of the JSON file.
    '''
    # if JSON contains absolute path to private key/certificate_
    # simply return it:
    if os.path.isabs(path):
        return path

    # if JSON file contains relative path to
    # private key/certificate:
    elif path.startswith(os.path.curdir):
        path = path.lstrip(os.path.curdir)
        pathlist = path.split(os.path.sep)

        # Absolute path to directory where "file_path_string" file
        # resides (which is the JSON credentials file):
        thisdir = get_this_directory(file_path_string, as_list=True)

        # Return absolute path to JSON file location plus relative
        # path contained in that JSON file!
        newdir = thisdir + list(pathlist)
        return os.path.sep+os.path.join(*newdir)

    else:
        # TODO FIXME: It might be a path relative to "..", but who would
        # use it that way in the real world?
        raise ValueError('Path is neither absolute nor relative to %s.' % os.path.curdir)

def get_this_directory(file_path_string, as_list=False):
    '''
    Rather: Get absolute path of the containing directory
    of a given file, given the (absolute or relative) path
    to that file.

    I.e. for a path to a file (absolute or relative), it returns
    the absolute path to the containing directory.

    Example: For "./credentials/mycreds.json", it returns
    "/foo/bar/baz/credentials"
    '''
    this_directory_string = os.path.split(os.path.realpath(file_path_string))[0]

    if as_list:
        this_directory_list = this_directory_string.split(os.path.sep)
        return this_directory_list
    else:
        return this_directory_string

def get_super_directory(file_path_string, as_list=False):
    this_directory_list = get_this_directory(file_path_string, as_list=True)
    super_directory_list = this_directory_list[0:len(this_directory_list)-1]

    if as_list:
        return super_directory_list
    else:
        super_directory_string = os.path.join(*super_directory_list)
        return os.path.sep+super_directory_string


def get_neighbour_directory(file_path_string, dirname):
    super_directory_list = get_super_directory(file_path_string, as_list=True)
    super_directory_list.append(dirname)
    neighbour_directory_string = os.path.join(*super_directory_list)
    return os.path.sep+neighbour_directory_string