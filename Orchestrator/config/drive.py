from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.oauth2 import service_account
from core.utils import get_base_workdir
from config.config_vars import config
import io
import structlog
logger = structlog.get_logger()

class Drive():
    _singleton = None
    _is_already_initialized = False

    def __init__(self):
        if not self._is_already_initialized:
            self.client = self._connect()
            self._download_default_config_files(config.DRIVE_CONFIG_FILES)
            self._is_already_initialized = True

    def _connect(self):
        logger.debug("Connecting to Drive")
        try:
            base_workdir = get_base_workdir()
            client = build('drive', 'v3', credentials=service_account.Credentials.from_service_account_file(
                    f"{base_workdir}/{config.SERVICE_ACCOUNT_FILE}", 
                    scopes=config.SCOPES)
                )
            client.files().list(pageSize=1, fields="nextPageToken, files(id, name)").execute().get('files', [])
            logger.debug("Connected to Drive")
            return client
        except Exception as e:
            raise Exception(e)
    
    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super(Drive, cls).__new__(cls)
        return cls._singleton
    
    def _download_file(self, file_id):
        file_name = self.client.files().get(fileId=file_id, fields='mimeType, name').execute().get('name')
        base_workdir = get_base_workdir()
        download = MediaIoBaseDownload(io.FileIO(f"{base_workdir}/prompts/{file_name}", 'wb'), self.client.files().get_media(fileId=file_id))
        while True:
            _, completed = download.next_chunk()
            if completed:
                return
    
    def _download_default_config_files(self, filenames=[]):
        logger.debug("Downloading config files from Drive")
        if len(filenames) < 1:
            logger.warning("No files to download from Drive")
            return
        for file_id in filenames:
            self._download_file(file_id)
        logger.debug("Downloaded %s config files from Drive", len(filenames))