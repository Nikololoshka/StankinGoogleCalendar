"""
Файл с созданием Calendar API сервиса.
"""

import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


def create_service(client_secret_file: str, api_name: str, api_version: str, scopes: list):
    """
    Создает Calendar API сервис для доступа к календарю пользователя.
    """

    if not os.path.exists(client_secret_file):
        raise FileNotFoundError("Файл для доступа к API не найден!")

    cred = None
    pickle_file = os.path.join(os.path.dirname(client_secret_file), f'token_{api_name}_{api_version}.pickle')

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    service = build(api_name, api_version, credentials=cred)
    print(f'Calendar API {api_version} сервис успешно создан!')

    return service
