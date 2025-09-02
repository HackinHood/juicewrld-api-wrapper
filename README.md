# Juice WRLD API Wrapper

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Python wrapper for the Juice WRLD API, providing easy access to Juice WRLD's complete discography including released tracks, unreleased songs, recording sessions, and unsurfaced content.

## Features

- **Full API Coverage**: Access to all Juice WRLD API endpoints
- **Type Safety**: Full type hints and data models
- **Error Handling**: Comprehensive exception handling
- **Context Manager Support**: Safe resource management
- **Search & Filtering**: Advanced song search across all categories
- **File Operations**: Browse, download, and manage audio files
- **Audio Streaming**: Modern streaming support with range requests
- **ZIP Operations**: Create and manage ZIP archives

## Requirements

- **Python**: 3.7+ (for dataclasses support)
- **Dependencies**: Only `requests>=2.28.0` (all other imports are built-in Python modules)

## Installation

### Quick Install (Recommended)
```bash
pip install juicewrld-api-wrapper
```

### Alternative Installation Methods

**From PyPI (Latest Release)**
```bash
pip install juicewrld-api-wrapper
```

**From GitHub Repository (Development Version)**
```bash
pip install git+https://github.com/hackinhood/juicewrld-api-wrapper.git
```

**From Source**
```bash
git clone https://github.com/hackinhood/juicewrld-api-wrapper.git
cd juicewrld-api-wrapper
pip install -e .
```

### Verify Installation
```bash
python -c "from juicewrld_api_wrapper import JuiceWRLDAPI; print('Installation successful!')"
```

## Quick Start

### Basic Usage

```python
from juicewrld_api_wrapper import JuiceWRLDAPI

# Initialize the API client
api = JuiceWRLDAPI()

# Get API overview
overview = api.get_api_overview()

# Search for songs
results = api.search_songs("lucid dreams", limit=10)

# Get songs by category
unreleased = api.get_songs_by_category("unreleased", page=1, page_size=20)

# Close the client
api.close()
```

### Audio Streaming

```python
from juicewrld_api_wrapper import JuiceWRLDAPI

api = JuiceWRLDAPI()

# Stream audio directly
stream_result = api.stream_audio_file("Compilation/2. Unreleased Discography/song.mp3")
if stream_result['status'] == 'success':
    stream_url = stream_result['stream_url']
    print(f"Stream URL: {stream_url}")
    print(f"Supports range: {stream_result['supports_range']}")

# Play songs from player endpoint (uses modern streaming)
play_result = api.play_juicewrld_song(song_id)
if play_result.get('stream_url'):
    print(f"Stream URL: {play_result['stream_url']}")

api.close()
```

### Context Manager Usage

```python
from juicewrld_api_wrapper import JuiceWRLDAPI

with JuiceWRLDAPI() as api:
    stats = api.get_stats()
    print(f"Total songs: {stats.total_songs}")
    
    songs = api.get_songs(category="released", page_size=5)
    for song in songs['results']:
        print(f"- {song.name} ({song.length})")
```

## API Endpoints

### Song Management

- `get_songs()` - Get songs with pagination and filtering
- `get_song()` - Get song by ID
- `search_songs()` - Search songs across all categories
- `get_songs_by_category()` - Get songs by specific category


### Categories & Eras

- `get_categories()` - Get available song categories
- `get_eras()` - Get all musical eras
- `get_stats()` - Get comprehensive statistics

### Audio Streaming

- `stream_audio_file(file_path)` - Stream audio files directly
- `play_juicewrld_song(song_id)` - Get streaming URL for player songs

### File Operations

- `browse_files()` - Browse directory structure
- `download_file()` - Download audio files
- `get_cover_art()` - Extract cover art
- `create_zip()` - Create ZIP archives
- `start_zip_job()` - Start background ZIP creation
- `get_zip_job_status()` - Check ZIP job status
- `cancel_zip_job()` - Cancel ZIP jobs

### Artist & Album Information

- `get_artists()` - Get all artists
- `get_artist()` - Get artist by ID
- `get_albums()` - Get all albums
- `get_album()` - Get album by ID

## Data Models

The wrapper provides structured data models for all entities:

```python
from juicewrld_api_wrapper.models import Song, Artist, Album, Era

# Song object with full metadata
song = Song(
    id=36310,
    name="Hit-Boys 2030",
    category="recording_session",
    era=Era(
        id=34,
        name="DRFL", 
        description="Death Race For Love era (December 2018-December 2019)",
        time_frame="(December 2018-December 2019)"
    ),
    track_titles=["Hit-Boys 2030", "Big"],
    credited_artists="Juice WRLD",
    producers="Corbett, Hit-Boy & TreShaunBeatz",
    engineers="Evan Swayne, Jacob Richards, Jaycen Joshua, Max Lord, Mike Seaberg & Rashawn McLean",
    recording_locations="Blue Room West Recording Studio, West Hollywood, Los Angeles, CA.",
    record_dates="Recorded January 11, 2019.",
    length="",
    session_titles="Big-OG Multitrack.ptx",
    session_tracking="Stem Track Files: 27, Total Vocal Takes: 44",
    instrumental_names="Hit-Boys2030 2018, Big-Instrumental V5 FNL",
    dates="Surfaced July 8, 2023."
)

# Access song metadata
print(f"Song: {song.name}")
print(f"Category: {song.category}")
print(f"Era: {song.era.name} ({song.era.time_frame})")
print(f"Track Titles: {', '.join(song.track_titles)}")
print(f"Producers: {song.producers}")
print(f"Recording Location: {song.recording_locations}")
print(f"Session: {song.session_titles}")
print(f"Stem Tracks: {song.session_tracking}")
```

## Audio Streaming

The wrapper provides modern audio streaming capabilities:

### Direct File Streaming
```python
# Stream any audio file directly
stream_result = api.stream_audio_file("Compilation/2. Unreleased Discography/song.mp3")

if stream_result['status'] == 'success':
    stream_url = stream_result['stream_url']
    content_type = stream_result['content_type']
    supports_range = stream_result['supports_range']
    
    print(f"Stream URL: {stream_url}")
    print(f"Content Type: {content_type}")
    print(f"Range Support: {supports_range}")
```

### Player Song Streaming
```python
# Get streaming URL for songs from player endpoint
play_result = api.play_juicewrld_song(song_id)

if play_result.get('stream_url'):
    stream_url = play_result['stream_url']
    print(f"Stream URL: {stream_url}")
```

### Streaming Features
- **Range Requests**: Support for partial content (206 responses)
- **Content Type Detection**: Automatic audio/mpeg detection
- **File Validation**: Checks if files exist before streaming
- **Error Handling**: Graceful fallback for missing files

## Error Handling

```python
from juicewrld_api_wrapper.exceptions import (
    JuiceWRLDAPIError, 
    RateLimitError, 
    NotFoundError,
    AuthenticationError,
    ValidationError
)

try:
    songs = api.get_songs(category="invalid_category")
except NotFoundError:
    print("Category not found")
except RateLimitError:
    print("Rate limit exceeded")
except AuthenticationError:
    print("Authentication required")
except JuiceWRLDAPIError as e:
    print(f"API error: {e}")
```

## Examples

See `examples.py` for comprehensive usage examples covering:

- Basic API operations
- Song search and filtering
- Audio streaming
- Error handling
- Context manager usage

## Configuration

### Environment Variables

```bash
export JUICE_WRLD_API_
export JUICE_WRLD_API_TIMEOUT="30"
```

## Data Categories

- **Released**: Officially released tracks and albums
- **Unreleased**: Confirmed unreleased songs with metadata
- **Recording Sessions**: Studio session recordings and snippets
- **Unsurfaced**: Rare and unsurfaced content

## Search Capabilities

- **Text Search**: Search by song title, artist, or lyrics
- **Category Filtering**: Filter by release status
- **Era Filtering**: Filter by musical era
- **Year Filtering**: Filter by recording/release year
- **Tag Filtering**: Filter by musical tags

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

## Rate Limiting

The wrapper respects API rate limits:
- Search queries: 100 requests/minute
- File downloads: 50 requests/minute
- ZIP creation: 10 requests/minute
- Audio streaming: 30 requests/minute

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Project Status

- **Version**: 1.0.4
- **Status**: Production Ready
- **Python Support**: 3.7+
- **Dependencies**: Minimal (only requests)

## Support

For support or questions:
- Check the examples in `examples.py`
- Review the API documentation in `API_ENDPOINTS.md`
- Open an issue on GitHub
- Check the [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

## Changelog

### v1.0.0
- Initial release
- Full API coverage
- Comprehensive error handling
- Type hints and data models
- Audio streaming support
- ZIP operations
- Modern files/download endpoint integration

