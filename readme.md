<h1 align="center">Yandex disk file synchroniser.</h1>

<img src="https://img.shields.io/badge/python3.12-blue">

## Description

Simple file synchroniser, working with yandex disk service. Monitor and upload last versions of files in given folder to yandex disk.

## Yandex permissions
### This operation is required!!!

You need to give yandex application permissions to read and write to entire disk.

## Setup enviroment variables
### This operation is required!!!

Copy or rename '.tempate' file to .env file, then fill it with your values.

## Running

    cd ya_disk_file_synchroniser
    pip install -r requirements.txt
    python main.py