# Juice WRLD API Endpoints

This document lists all the API endpoints available in the Juice WRLD API Wrapper.

## Core API Endpoints

### 1. API Overview
- **GET** `/juicewrld/` - Get API overview and status
- **Method**: `get_api_overview()`

### 2. Artist Endpoints
- **GET** `/juicewrld/artists/` - Get all artists
- **GET** `/juicewrld/artists/{id}/` - Get artist by ID
- **Methods**: `get_artists()`, `get_artist(artist_id)`

### 3. Album Endpoints
- **GET** `/juicewrld/albums/` - Get all albums
- **GET** `/juicewrld/albums/{id}/` - Get album by ID
- **Methods**: `get_albums()`, `get_album(album_id)`

### 4. Song Endpoints
- **GET** `/juicewrld/songs/` - Get songs with pagination and filtering
- **GET** `/juicewrld/songs/{id}/` - Get song by ID
- **Methods**: `get_songs()`, `get_song(song_id)`

### 5. Era Endpoints
- **GET** `/juicewrld/eras/` - Get all eras
- **GET** `/juicewrld/eras/{id}/` - Get era by ID
- **Methods**: `get_eras()`, `get_era(era_id)`

### 6. Statistics & Categories
- **GET** `/juicewrld/stats/` - Get song statistics
- **GET** `/juicewrld/categories/` - Get available categories
- **Methods**: `get_stats()`, `get_categories()`

### 7. Juice WRLD Specific Songs
- **GET** `/juicewrld/player/songs/` - Get Juice WRLD songs
- **GET** `/juicewrld/player/songs/{id}/` - Get Juice WRLD song by ID
- **Methods**: `get_juicewrld_songs()`, `get_juicewrld_song(song_id)`

## Audio Streaming Endpoints

### 8. Modern Audio Streaming
- **GET** `/juicewrld/files/download/?path={file_path}` - Stream audio files directly
- **Methods**: `stream_audio_file(file_path)`, `play_juicewrld_song(song_id)`

**Note**: The old `/juicewrld/player/songs/{id}/play/` endpoint is deprecated. Use the files/download endpoint for modern audio streaming.

## File Management Endpoints

### 9. File Browser
- **GET** `/juicewrld/files/browse/` - Browse directory structure
- **Method**: `browse_files(path, search)`

### 10. File Operations
- **GET** `/juicewrld/files/download/` - Download file
- **GET** `/juicewrld/files/info/` - Get file information
- **GET** `/juicewrld/files/cover-art/` - Extract cover art
- **Methods**: `download_file(file_path)`, `get_file_info(file_path)`, `get_cover_art(file_path)`

### 11. ZIP Operations
- **POST** `/juicewrld/files/zip-selection/` - Create ZIP from file selection
- **POST** `/juicewrld/start-zip-job/` - Start ZIP creation job
- **GET** `/juicewrld/zip-job-status/{job_id}/` - Get ZIP job status
- **POST** `/juicewrld/cancel-zip-job/{job_id}/` - Cancel ZIP job
- **Methods**: `create_zip(file_paths)`, `start_zip_job(file_paths)`, `get_zip_job_status(job_id)`, `cancel_zip_job(job_id)`

## Search & Filtering Endpoints

### 12. Song Search
- **GET** `/juicewrld/songs/` - Search songs with query parameter
- **Method**: `search_songs(query, category, year, tags, limit, offset)`

### 13. Category Filtering
- **GET** `/juicewrld/songs/` - Get songs by category
- **Method**: `get_songs_by_category(category, page, page_size)`



## Endpoint Parameters

### Common Parameters
- `page` - Page number for pagination
- `page_size` - Number of items per page
- `category` - Song category filter
- `era` - Era filter
- `search` - Search term
- `limit` - Maximum number of results
- `offset` - Result offset for pagination

### File Operation Parameters
- `path` - File or directory path (relative to comp directory)
- `search` - Search term for file browsing
- `file_paths` - List of file paths for ZIP operations

### Audio Streaming Parameters
- `file_path` - Relative path from comp directory (e.g., "Compilation/2. Unreleased Discography/song.mp3")

## Response Formats

### Song Object
```json
{
  "id": 123,
  "name": "Song Title",
  "category": "unreleased",
  "era": {
    "id": 1,
    "name": "JUTE",
    "description": "Juice The Kidd Era"
  },
  "length": "3:45",
  "producers": "Producer Name",
  "track_titles": ["Title 1", "Title 2"]
}
```

### Search Result
```json
{
  "songs": [...],
  "total": 150,
  "category": "unreleased",
  "query_time": "45ms"
}
```

### Directory Info
```json
{
  "current_path": "/audio/unreleased",
  "items": [...],
  "total_files": 150,
  "total_directories": 12,
  "is_recursive_search": true
}
```

### Stream Result
```json
{
  "status": "success",
  "stream_url": "https://juicewrldapi.com/juicewrld/files/download/?path=...",
  "file_path": "path/to/file.mp3",
  "content_type": "audio/mpeg",
  "content_length": "10837871",
  "supports_range": true
}
```

## Rate Limits

- **Search queries**: 100 requests/minute
- **File downloads**: 50 requests/minute
- **ZIP creation**: 10 requests/minute
- **Audio streaming**: 30 requests/minute

## HTTP Codes

- **200** - Success
- **206** - Partial Content (for range requests)
- **400** - Bad Request
- **401** - Unauthorized
- **404** - Not Found
- **405** - Method Not Allowed (HEAD requests not supported)
- **429** - Rate Limit Exceeded
- **500** - Internal Server Error

## Usage Examples

### Basic API Usage
```python
from juicewrld_api_wrapper import JuiceWRLDAPI

api = JuiceWRLDAPI(base_url="https://juicewrldapi.com")
songs = api.get_songs(page=1, category="unreleased", page_size=20)
api.close()
```

### Audio Streaming
```python
from juicewrld_api_wrapper import JuiceWRLDAPI

api = JuiceWRLDAPI(base_url="https://juicewrldapi.com")

# Stream a specific audio file
stream_result = api.stream_audio_file("Compilation/2. Unreleased Discography/song.mp3")
if stream_result['status'] == 'success':
    stream_url = stream_result['stream_url']
    print(f"Stream URL: {stream_url}")
    print(f"Supports range: {stream_result['supports_range']}")

# Play a song from player endpoint (uses modern streaming)
play_result = api.play_juicewrld_song(song_id)
if play_result.get('stream_url'):
    print(f"Stream URL: {play_result['stream_url']}")

api.close()
```

### Context Manager Usage
```python
from juicewrld_api_wrapper import JuiceWRLDAPI

with JuiceWRLDAPI(base_url="https://juicewrldapi.com") as api:
    songs = api.get_songs(page=1, page_size=20)
```

## File Path Structure

The API expects file paths relative to the `comp` directory:

```
comp/
├── Compilation/
│   ├── 1. Released Discography/
│   └── 2. Unreleased Discography/
├── Session Edits/
├── Snippets/
└── Original Files/
```

**Example paths:**
- `"Compilation/2. Unreleased Discography/1. JUICED UP THE EP (Sessions)/Ain't Talkin' Toronto (feat. JuiceTheKidd).mp3"`
- `"Snippets/Auto/Auto.mp4"`
- `"Session Edits/song.mp3"`

## Notes

- All endpoints require API access
- All endpoints support proper error handling
- Context managers ensure proper resource cleanup
- Audio streaming uses modern files/download endpoint
- HEAD requests are not supported (use GET with Range header)
- File paths must be relative to comp directory
- ZIP operations require valid file paths that exist
