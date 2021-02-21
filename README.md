# Zenodotus
Keeper of Records

<p align="center">
<img src="https://github.com/AlexandriaILS/Zenodotus/blob/master/assets/image.png?raw=true" alt="the man himself">
</p>

This dude with the awesome beard is the head librarian of Alexandria and the keeper of records -- a service that allows individual installations of Alexandria to both back up records and download them from other installs (if they want to share).

## Local dev:

```shell
python manage.py migrate
python manage.py bootstrap_data
python manage.py createinitialrevisions
```

Useful command to clean up the `images` folder: `python manage.py cleanup_unused_media --no-input`
