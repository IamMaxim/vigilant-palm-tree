'''A collection of sink nodes.'''
from .file_store import FileStore
from .video_display import VideoDisplay
from .sqlite_store import SQLiteStore

__all__ = (
    'FileStore',
    'VideoDisplay',
    'SQLiteStore',
)
