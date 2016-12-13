# Sample Web Client

This is a sample Web Client that exploits [JQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload)
[(documentation)](https://github.com/blueimp/jQuery-File-Upload/wiki) in order to upload large files in chunks.

## The protocol between the client and the FROGv.4-datastore

The client upload the first chunk of data with a POST request and the datastore replies with an ``upload_id`` which identifies the upload session.
Then the client could send subsequent POST requests with other chunks of data and the associated ``upload_id`` until the end.
For further details see the documentation of [django-chunked-uploads](https://github.com/juliomalegria/django-chunked-upload/blob/master/README.rst#typical-usage).
