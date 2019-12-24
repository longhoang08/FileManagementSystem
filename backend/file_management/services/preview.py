import logging

from file_management import repositories
from file_management.constant import pathconst
from preview_generator.manager import PreviewManager

_logger = logging.getLogger(__name__)

def get_zip_preview(file_id, path):
    cache_path = pathconst.TEMP
    manager = PreviewManager(cache_path, create_folder= True)
    path_to_zip_json = manager.get_json_preview(
        file_path=path,
    )
    return path_to_zip_json

def get_docs_preview(file_id, path):
    cache_path = pathconst.TEMP
    manager = PreviewManager(cache_path, create_folder = True)
    path_to_pdf_preview = manager.get_pdf_preview(file_path=path)
    return path_to_pdf_preview

def get_image_preview(file_id,path):
    cache_path = pathconst.TEMP
    manager = PreviewManager(cache_path, create_folder= True)
    path_to_jpeg_preview = manager.get_jpeg_preview(file_path=path, height=800, width=800)
    return path_to_jpeg_preview
