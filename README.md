# Commerce

A project that allows users to watch, bid, and if he/she is the seller, the user may close the auction. 

See it live: [commerce.catbirdseat.io](https://commerce.catbirdseat.io)

## .env

This project uses [django-environ](https://django-environ.readthedocs.io/en/latest/), which allows the use of environment variables to set settings. The following settings are expected to be in environment variables or in an .env file:

| Setting| Description | 
| :---|    :----:| 
| DEBUG     | Determines whether the running application is in debug mode.| 
| SECRET_KEY   | Secret key used for the application.| 
|ALLOWED_HOSTS| IPs and domains allowed to acces the application|
|DATABASE_URL| The URL used to access the application's database. To use SQLite locally, use `sqlite:///db.sqlite3`|

If Amazon S3 is used for media, the following settings are expected:

| Setting| Description | 
| :---|    :----:| 
| S3     |Flag for determining if S3 storage is to be used. Set this to True.| 
| AWS_S3_ACCESS_KEY_ID| S3 access key.| 
| AWS_S3_SECRET_ACCESS_KEY| Secret key used for S3.| 
| AWS_STORAGE_BUCKET_NAME| The name of the bucket used to store media.|



