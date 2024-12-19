from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import os
import time
import asyncio
from datetime import datetime

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials

from models.schemas.events import EventsSchema


class SheetMiddleware(BaseMiddleware):
    def get_service_sacc(self):
        creds_json = os.path.join(os.getcwd(), 'creds/sheets-credentials.json')
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

        creds_service = Credentials.from_service_account_file(creds_json, scopes=scopes)
        return build('sheets', 'v4', credentials=creds_service), build('drive', 'v3', credentials=creds_service)

    def create_spreadsheet(self, title):
        sheets_service, _ = self.get_service_sacc()
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = sheets_service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId,spreadsheetUrl').execute()
        return spreadsheet['spreadsheetId'], spreadsheet['spreadsheetUrl']

    def set_spreadsheet_permissions(self, file_id):
        try:
            _, drive_service = self.get_service_sacc()
            user_permission = {
                'type': 'anyone',
                'role': 'writer',
            }

            request = drive_service.permissions().create(
                fileId=file_id,
                body=user_permission,
                fields='id',
            )
            request.execute()
        except Exception as e:
            print(f"An error occurred: {e}")

    async def add_data_to_sheet(self, sheet_id, range, data):
        sheets_service, _ = self.get_service_sacc()

        sheet = sheets_service.spreadsheets()

        body = {
            'values': [data]
        }

        result = sheet.values().append(
            spreadsheetId=sheet_id,
            range=range,
            valueInputOption='RAW',
            body=body
        ).execute()

        return result

    async def manage_requests(self, sheet_id, data):
        interval = 60 / 300
        for values in data:
            start_time = time.time()
          
            elapsed_time = time.time() - start_time
            await asyncio.sleep(max(0, interval - elapsed_time))

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # print("Before handler")

        result = await handler(event, data)

        user_id = event.from_user.id
        username = event.from_user.username if hasattr(event.from_user, 'username') else ''
        name = event.from_user.full_name if hasattr(event.from_user, 'full_name') else ''
        message = event.text if hasattr(event, 'text') else ''
        callback = event.data if hasattr(event, 'data') else ''
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # photo = event.photo.file_id if hasattr(event, 'photo') and event.photo is not None else ''

        data = [[user_id, username, name, message, callback, timestamp]]

        evt = EventsSchema(user_id=str(user_id), username=username, display_name=name, value=message, callback=callback, timestamp=datetime.now())
        await evt.create()

        # spreadsheet_id, spreadsheet_url = self.create_spreadsheet('Bot export')

        spreadsheet_id = os.getenv('SPREADSHEET_ID')

        # self.set_spreadsheet_permissions(spreadsheet_id)

        # print(f"Spreadsheet ID: {spreadsheet_id}")
        # print(f"Spreadsheet URL: {spreadsheet_url}")

        asyncio.create_task(self.manage_requests(spreadsheet_id, data))

        # print("After handler")
        return result
