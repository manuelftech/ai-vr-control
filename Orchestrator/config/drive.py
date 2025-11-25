from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
from config import config
import logging
import io
logger = logging.getLogger(__name__)

class Drive():
    _singleton = None
    _is_already_initialized = False

    def __init__(self):
        if not self._is_already_initialized:
            self.client = self._connect()
            self._is_already_initialized = True
            self._setup_prompts()

    def _connect(self):
        logger.debug("Connecting to Drive")
        try:
            client = build('drive', 'v3', credentials=service_account.Credentials.from_service_account_file(
                    config.SERVICE_ACCOUNT_FILE, 
                    scopes=config.SCOPES)
                )
            # Testing the connection
            client.files().list(pageSize=1, fields="nextPageToken, files(id, name)").execute().get('files', [])
            logger.debug("Successfuly connected to Drive")
            return client
        except Exception as e:
            raise Exception(e)
        
    def get_status(self):
        return self.connection_status
    
    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Drive, cls).__new__(cls)
        return cls._singleton
    
    def _download_file(self, file_id):
        file_name = self.client.files().get(fileId=file_id, fields='mimeType, name').execute().get('name')
        download = MediaIoBaseDownload(io.FileIO(f"./Orchestrator/prompts/{file_name}", 'wb'), self.client.files().get_media(fileId=file_id))
        while True:
            _, completed = download.next_chunk()
            if completed:
                return
    
    def _setup_prompts(self):
        logger.debug("Downloading Prompt files from Drive")
        for file_id in config.DRIVE_PROMPT_FILES:
            self._download_file(file_id)
        logger.debug("Prompt files successfully downloaded")