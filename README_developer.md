# Developer's guide

This README is intended to provide some insights for developers about the APIs exposed by the FROGv.4-datastore.
 
## NF Image upload API

In order to upload large NF Image files [django-chunked-uploads](https://github.com/juliomalegria/django-chunked-upload/) it was exploited.

When the client uploads the first chunk of file with a POST request, the datastore replies with an ``upload_id`` which identifies the upload session.
Then the client could send subsequent POST requests with other chunks of data and the associated ``upload_id`` until the end of file transfer.
Uploads can be also resumed as long as the client sends the same ``upload_id`` with the last unsent chunk of file. 

A [Sample Web client](https://github.com/netgroup-polito/frog4-datastore/tree/master/sample-clients/Web) for NF Image's upload that works together with the FROGv.4-datastore it is also provided.

For further details see the documentation of [django-chunked-uploads](https://github.com/juliomalegria/django-chunked-upload/blob/master/README.rst#typical-usage).
