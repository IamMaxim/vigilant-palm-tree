'''A collection of sink nodes.'''
from .file_store import FileStore
from .video_display import VideoDisplay
from .sqlite_store import SQLiteStore
from .graph_view import GraphView

__all__ = (
    'FileStore',
    'VideoDisplay',
    'SQLiteStore',
    'GraphView'
)
