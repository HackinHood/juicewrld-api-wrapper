from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class Artist:
    id: int
    name: str
    bio: str

@dataclass
class Album:
    id: int
    title: str
    type: str
    artist: Artist
    release_date: datetime
    description: str

@dataclass
class Era:
    id: int
    name: str
    description: str
    time_frame: str

@dataclass
class Song:
    id: int
    name: str
    original_key: str
    category: str
    era: Era
    track_titles: List[str]
    credited_artists: str
    producers: str
    engineers: str
    additional_information: str
    file_names: str
    instrumentals: str
    recording_locations: str
    record_dates: str
    preview_date: str
    release_date: str
    dates: str
    length: str
    leak_type: str
    date_leaked: str
    notes: str
    image_url: str
    session_titles: str
    session_tracking: str
    instrumental_names: str
    public_id: str = ""

@dataclass
class FileInfo:
    name: str
    type: str
    size: int
    size_human: str
    path: str
    extension: str
    mime_type: str
    created: datetime
    modified: datetime
    encoding: Optional[str]

@dataclass
class DirectoryInfo:
    current_path: str
    path_parts: List[Dict[str, str]]
    items: List[FileInfo]
    total_files: int
    total_directories: int
    search_query: Optional[str]
    is_recursive_search: bool

@dataclass
class SearchResult:
    songs: List[Song]
    total: int
    category: Optional[str]
    query_time: str

@dataclass
class Stats:
    total_songs: int
    category_stats: Dict[str, int]
    era_stats: Dict[str, int]


