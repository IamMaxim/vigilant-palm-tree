'''A collection of sink nodes.'''
from .file_store import FileStore
from .video_display import VideoDisplay
from .csv_store import CSVStore
from .graph_view import GraphView

__all__ = (
    'FileStore',
    'VideoDisplay',
    'CSVStore',
    'GraphView'
)
