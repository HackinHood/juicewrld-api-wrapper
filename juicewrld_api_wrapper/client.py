import requests
import time
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from urllib.parse import quote
from .models import Song, Artist, Album, Era, FileInfo, DirectoryInfo, SearchResult, Stats
from .exceptions import JuiceWRLDAPIError, RateLimitError, NotFoundError, AuthenticationError, ValidationError

class JuiceWRLDAPI:
    """
    A comprehensive Python wrapper for the Juice WRLD API.
    
    This class provides easy access to Juice WRLD's complete discography
    including released tracks, unreleased songs, recording sessions,
    and unsurfaced content. It handles all API communication, error
    handling, and data parsing.
    
    Attributes:
        base_url (str): The base URL for API requests
        timeout (int): Request timeout in seconds
        session (requests.Session): HTTP session for persistent connections
        rate_limit_remaining (int): Remaining API requests in current window
        rate_limit_reset (float): Timestamp when rate limit resets
    """
    
    def __init__(self, base_url: str = "https://juicewrldapi.com", timeout: int = 30):
        """
        Initialize the Juice WRLD API client.
        
        Args:
            base_url (str, optional): Base URL for the API. Defaults to "https://juicewrldapi.com".
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JuiceWRLD-API-Wrapper/1.0.4',
            'Accept': 'application/json'
        })
        self.rate_limit_remaining = 100
        self.rate_limit_reset = time.time() + 60

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        This is an internal method that handles all HTTP communication,
        error handling, and response parsing.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint path
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Dict[str, Any]: JSON response from the API
            
        Raises:
            RateLimitError: When API rate limit is exceeded
            NotFoundError: When the requested resource is not found
            AuthenticationError: When authentication is required
            JuiceWRLDAPIError: For other API errors
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            elif response.status_code == 404:
                raise NotFoundError("Resource not found")
            elif response.status_code == 401:
                raise AuthenticationError("Authentication required")
            elif response.status_code >= 400:
                raise JuiceWRLDAPIError(f"API error: {response.status_code} - {response.text}")
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise JuiceWRLDAPIError(f"Request failed: {str(e)}")

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API.
        
        Args:
            endpoint (str): API endpoint path
            params (Dict[str, Any], optional): Query parameters. Defaults to None.
            
        Returns:
            Dict[str, Any]: JSON response from the API
        """
        return self._make_request('GET', endpoint, params=params)

    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request to the API.
        
        Args:
            endpoint (str): API endpoint path
            data (Dict[str, Any], optional): Request data. Defaults to None.
            
        Returns:
            Dict[str, Any]: JSON response from the API
        """
        return self._make_request('POST', endpoint, json=data)

    def get_api_overview(self) -> Dict[str, Any]:
        """
        Get an overview of the Juice WRLD API.
        
        Returns information about available endpoints, API title,
        description, and version.
        
        Returns:
            Dict[str, Any]: API overview containing endpoints, title, description, and version
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> overview = api.get_api_overview()
            >>> print(overview['title'])
            'Juice WRLD API'
        """
        data = self._get('/juicewrld/')
        return {
            'endpoints': data,
            'title': 'Juice WRLD API',
            'description': 'Comprehensive API for Juice WRLD discography and content',
            'version': '1.0.4'
        }

    def get_artists(self) -> List[Artist]:
        """
        Get all artists from the API.
        
        Returns:
            List[Artist]: List of Artist objects containing artist information
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> artists = api.get_artists()
            >>> for artist in artists:
            ...     print(f"Artist: {artist.name}")
        """
        data = self._get('/juicewrld/artists/')
        return [Artist(**artist) for artist in data.get('results', [])]

    def get_artist(self, artist_id: int) -> Artist:
        """
        Get a specific artist by ID.
        
        Args:
            artist_id (int): The unique identifier of the artist
            
        Returns:
            Artist: Artist object containing detailed artist information
            
        Raises:
            NotFoundError: If the artist ID doesn't exist
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> artist = api.get_artist(1)
            >>> print(f"Artist: {artist.name}")
        """
        data = self._get(f'/juicewrld/artists/{artist_id}/')
        return Artist(**data)

    def get_albums(self) -> List[Album]:
        """
        Get all albums from the API.
        
        Returns:
            List[Album]: List of Album objects containing album information
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> albums = api.get_albums()
            >>> for album in albums:
            ...     print(f"Album: {album.name}")
        """
        data = self._get('/juicewrld/albums/')
        return [Album(**album) for album in data.get('results', [])]

    def get_album(self, album_id: int) -> Album:
        """
        Get a specific album by ID.
        
        Args:
            album_id (int): The unique identifier of the album
            
        Returns:
            Album: Album object containing detailed album information
            
        Raises:
            NotFoundError: If the album ID doesn't exist
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> album = api.get_album(1)
            >>> print(f"Album: {album.name}")
        """
        data = self._get(f'/juicewrld/albums/{album_id}/')
        return Album(**data)

    def get_songs(self, page: int = 1, category: Optional[str] = None, 
                  era: Optional[str] = None, search: Optional[str] = None, 
                  page_size: int = 20) -> Dict[str, Any]:
        """
        Get songs with pagination and filtering options.
        
        Args:
            page (int, optional): Page number for pagination. Defaults to 1.
            category (str, optional): Filter by song category (e.g., 'released', 'unreleased'). Defaults to None.
            era (str, optional): Filter by musical era. Defaults to None.
            search (str, optional): Search query for song titles or content. Defaults to None.
            page_size (int, optional): Number of songs per page. Defaults to 20.
            
        Returns:
            Dict[str, Any]: Dictionary containing songs, count, and pagination info
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> songs = api.get_songs(category="unreleased", page_size=10)
            >>> print(f"Found {songs['count']} songs")
            >>> for song in songs['results']:
            ...     print(f"- {song.name}")
        """
        params = {'page': page, 'page_size': page_size}
        if category:
            params['category'] = category
        if era:
            params['era'] = era
        if search:
            params['search'] = search
            
        data = self._get('/juicewrld/songs/', params=params)
        
        if 'results' in data:
            songs = []
            for song_data in data['results']:
                if isinstance(song_data, dict):
                    era_obj = Era(
                        id=song_data.get('era', {}).get('id', 0),
                        name=song_data.get('era', {}).get('name', 'Unknown'),
                        description=song_data.get('era', {}).get('description', ''),
                        time_frame=song_data.get('era', {}).get('time_frame', '')
                    )
                    
                    song = Song(
                        id=song_data.get('id', 0),
                        name=song_data.get('name', 'Unknown'),
                        original_key=song_data.get('original_key', ''),
                        category=song_data.get('category', 'unknown'),
                        era=era_obj,
                        track_titles=song_data.get('track_titles', []),
                        credited_artists=song_data.get('credited_artists', ''),
                        producers=song_data.get('producers', ''),
                        engineers=song_data.get('engineers', ''),
                        additional_information=song_data.get('additional_information', ''),
                        file_names=song_data.get('file_names', ''),
                        instrumentals=song_data.get('instrumentals', ''),
                        recording_locations=song_data.get('recording_locations', ''),
                        record_dates=song_data.get('record_dates', ''),
                        preview_date=song_data.get('preview_date', ''),
                        release_date=song_data.get('release_date', ''),
                        dates=song_data.get('dates', ''),
                        length=song_data.get('length', ''),
                        leak_type=song_data.get('leak_type', ''),
                        date_leaked=song_data.get('date_leaked', ''),
                        notes=song_data.get('notes', ''),
                        image_url=song_data.get('image_url', ''),
                        session_titles=song_data.get('session_titles', ''),
                        session_tracking=song_data.get('session_tracking', ''),
                        instrumental_names=song_data.get('instrumental_names', ''),
                        public_id=song_data.get('public_id', '')
                    )
                    songs.append(song)
            
            return {
                'results': songs,
                'count': data.get('count', 0),
                'next': data.get('next'),
                'previous': data.get('previous')
            }
        
        return data

    def get_song(self, song_id: int) -> Song:
        """
        Get a specific song by ID.
        
        Args:
            song_id (int): The unique identifier of the song
            
        Returns:
            Song: Song object containing detailed song information
            
        Raises:
            NotFoundError: If the song ID doesn't exist
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> song = api.get_song(36310)
            >>> print(f"Song: {song.name}")
            >>> print(f"Category: {song.category}")
        """
        data = self._get(f'/juicewrld/songs/{song_id}/')
        return Song(**data)

    def get_eras(self) -> List[Era]:
        """
        Get all musical eras from the API.
        
        Returns:
            List[Era]: List of Era objects containing era information
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> eras = api.get_eras()
            >>> for era in eras:
            ...     print(f"Era: {era.name} - {era.time_frame}")
        """
        data = self._get('/juicewrld/eras/')
        return [Era(**era) for era in data.get('results', [])]

    def get_era(self, era_id: int) -> Era:
        """
        Get a specific musical era by ID.
        
        Args:
            era_id (int): The unique identifier of the era
            
        Returns:
            Era: Era object containing detailed era information
            
        Raises:
            NotFoundError: If the era ID doesn't exist
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> era = api.get_era(34)
            >>> print(f"Era: {era.name}")
            >>> print(f"Time Frame: {era.time_frame}")
        """
        data = self._get(f'/juicewrld/eras/{era_id}/')
        return Era(**data)

    def get_stats(self) -> Stats:
        """
        Get comprehensive statistics about the Juice WRLD discography.
        
        Returns:
            Stats: Stats object containing total songs, artists, albums, etc.
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> stats = api.get_stats()
            >>> print(f"Total songs: {stats.total_songs}")
            >>> print(f"Total artists: {stats.total_artists}")
        """
        data = self._get('/juicewrld/stats/')
        return Stats(**data)

    def get_categories(self) -> List[Dict[str, str]]:
        """
        Get available song categories.
        
        Returns:
            List[Dict[str, str]]: List of category dictionaries with name and description
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> categories = api.get_categories()
            >>> for category in categories:
            ...     print(f"Category: {category['name']}")
        """
        data = self._get('/juicewrld/categories/')
        return data.get('categories', [])

    def get_juicewrld_songs(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        Get songs from the player endpoint with pagination.
        
        This endpoint provides songs optimized for the player interface
        with additional metadata for streaming.
        
        Args:
            page (int, optional): Page number for pagination. Defaults to 1.
            page_size (int, optional): Number of songs per page. Defaults to 20.
            
        Returns:
            Dict[str, Any]: Dictionary containing songs and pagination info
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> songs = api.get_juicewrld_songs(page_size=10)
            >>> print(f"Found {len(songs['results'])} songs")
        """
        params = {'page': page, 'page_size': page_size}
        return self._get('/juicewrld/player/songs/', params=params)

    def get_juicewrld_song(self, song_id: int) -> Dict[str, Any]:
        """
        Get a specific song from the player endpoint.
        
        This endpoint provides additional streaming metadata and file
        information optimized for the player interface.
        
        Args:
            song_id (int): The unique identifier of the song
            
        Returns:
            Dict[str, Any]: Dictionary containing song details and streaming info
            
        Raises:
            NotFoundError: If the song ID doesn't exist
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> song = api.get_juicewrld_song(12345)
            >>> print(f"Title: {song.get('title')}")
            >>> print(f"File: {song.get('file')}")
        """
        return self._get(f'/juicewrld/player/songs/{song_id}/')

    def play_juicewrld_song(self, song_id: int) -> Dict[str, Any]:
        """
        Get streaming information for a song from the player endpoint.
        
        This method attempts to find the correct file path for a song
        and returns streaming information. It tries multiple possible
        file paths to locate the actual audio file.
        
        Args:
            song_id (int): The unique identifier of the song
            
        Returns:
            Dict[str, Any]: Dictionary containing streaming status and URL
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> result = api.play_juicewrld_song(12345)
            >>> if result['status'] == 'success':
            ...     print(f"Stream URL: {result['stream_url']}")
        """
        try:
            song_data = self.get_juicewrld_song(song_id)
            if 'file' not in song_data:
                return {'error': 'Song file information not found', 'song_id': song_id, 'status': 'no_file_info'}
            
            file_url = song_data['file']
            if '/media/' in file_url:
                file_path = file_url.split('/media/')[-1]
            else:
                return {'error': 'Invalid file URL format', 'song_id': song_id, 'status': 'invalid_url'}
            
            possible_paths = [
                f"Compilation/1. Released Discography/{song_data.get('album', '')}/{song_data.get('title', '')}.mp3",
                f"Compilation/2. Unreleased Discography/{song_data.get('title', '')}.mp3",
                f"Snippets/{song_data.get('title', '')}/{song_data.get('title', '')}.mp4",
                f"Session Edits/{song_data.get('title', '')}.mp3"
            ]
            
            for test_path in possible_paths:
                try:
                    stream_url = f"{self.base_url}/juicewrld/files/download/?path={quote(test_path)}"
                    headers = {'Range': 'bytes=0-0'}
                    response = self.session.get(stream_url, headers=headers, timeout=5)
                    if response.status_code in [200, 206]:
                        return {
                            'status': 'success', 
                            'song_id': song_id, 
                            'stream_url': stream_url,
                            'file_path': test_path,
                            'content_type': response.headers.get('content-type', 'audio/mpeg')
                        }
                except:
                    continue
            
            stream_url = f"{self.base_url}/juicewrld/files/download/?path={quote(file_path)}"
            return {
                'status': 'file_not_found_but_url_provided', 
                'song_id': song_id, 
                'stream_url': stream_url,
                'file_path': file_path,
                'note': 'File may not exist at this path, but streaming URL is provided'
            }
                
        except Exception as e:
            return {'error': f'Request failed: {str(e)}', 'song_id': song_id, 'status': 'request_error'}

    def stream_audio_file(self, file_path: str) -> Dict[str, Any]:
        """
        Get streaming information for an audio file.
        
        This method checks if an audio file exists and returns streaming
        information including content type and range request support.
        
        Args:
            file_path (str): Path to the audio file relative to the comp directory
            
        Returns:
            Dict[str, Any]: Dictionary containing streaming status and metadata
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> result = api.stream_audio_file("Compilation/2. Unreleased Discography/song.mp3")
            >>> if result['status'] == 'success':
            ...     print(f"Stream URL: {result['stream_url']}")
            ...     print(f"Supports range: {result['supports_range']}")
        """
        try:
            stream_url = f"{self.base_url}/juicewrld/files/download/?path={quote(file_path)}"
            
            headers = {'Range': 'bytes=0-0'}
            response = self.session.get(stream_url, headers=headers, timeout=self.timeout)
            
            if response.status_code in [200, 206]:
                return {
                    'status': 'success',
                    'stream_url': stream_url,
                    'file_path': file_path,
                    'content_type': response.headers.get('content-type', 'audio/mpeg'),
                    'content_length': response.headers.get('content-length'),
                    'supports_range': 'bytes' in response.headers.get('accept-ranges', '')
                }
            elif response.status_code == 404:
                return {'error': 'Audio file not found', 'file_path': file_path, 'status': 'file_not_found'}
            else:
                return {'error': f'HTTP {response.status_code}', 'file_path': file_path, 'status': 'http_error'}
                
        except Exception as e:
            return {'error': f'Request failed: {str(e)}', 'file_path': file_path, 'status': 'request_error'}

    def browse_files(self, path: str = '', search: Optional[str] = None) -> DirectoryInfo:
        """
        Browse the file system structure.
        
        This method allows you to explore the directory structure and
        search for files. It returns both files and directories with
        detailed metadata including file sizes, dates, and types.
        
        Args:
            path (str, optional): Directory path to browse. Defaults to '' (root).
            search (str, optional): Search query for file names. Defaults to None.
            
        Returns:
            DirectoryInfo: Object containing directory structure and file information
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> directory = api.browse_files("Compilation")
            >>> print(f"Total files: {directory.total_files}")
            >>> for item in directory.items:
            ...     print(f"- {item.name} ({item.type})")
        """
        params = {}
        if path:
            params['path'] = path
        if search:
            params['search'] = search
            
        data = self._get('/juicewrld/files/browse/', params=params)
        
        items = []
        for item in data.get('items', []):
            if item['type'] == 'file':
                try:
                    created = datetime.fromisoformat(item.get('created', '')) if item.get('created') else datetime.now()
                    modified = datetime.fromisoformat(item.get('modified', '')) if item.get('modified') else datetime.now()
                except (ValueError, TypeError):
                    created = datetime.now()
                    modified = datetime.now()
                
                items.append(FileInfo(
                    name=item.get('name', ''),
                    type=item.get('type', 'file'),
                    size=item.get('size', 0),
                    size_human=item.get('size_human', ''),
                    path=item.get('path', ''),
                    extension=item.get('extension', ''),
                    mime_type=item.get('mime_type', ''),
                    created=created,
                    modified=modified,
                    encoding=item.get('encoding')
                ))
            else:
                try:
                    modified = datetime.fromisoformat(item.get('modified', '')) if item.get('modified') else datetime.now()
                except (ValueError, TypeError):
                    modified = datetime.now()
                
                items.append(FileInfo(
                    name=item['name'],
                    type='directory',
                    size=0,
                    size_human='',
                    path=item['path'],
                    extension='',
                    mime_type='',
                    created=modified,
                    modified=modified,
                    encoding=None
                ))
        
        return DirectoryInfo(
            current_path=data.get('current_path', ''),
            path_parts=data.get('path_parts', []),
            items=items,
            total_files=data.get('total_files', 0),
            total_directories=data.get('total_directories', 0),
            search_query=data.get('search_query'),
            is_recursive_search=data.get('is_recursive_search', False)
        )

    def get_file_info(self, file_path: str) -> FileInfo:
        """
        Get detailed information about a specific file.
        
        Args:
            file_path (str): Path to the file relative to the comp directory
            
        Returns:
            FileInfo: Object containing detailed file metadata
            
        Raises:
            NotFoundError: If the file doesn't exist
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> file_info = api.get_file_info("Compilation/2. Unreleased Discography/song.mp3")
            >>> print(f"File: {file_info.name}")
            >>> print(f"Size: {file_info.size_human}")
            >>> print(f"Type: {file_info.mime_type}")
        """
        data = self._get('/juicewrld/files/info/', {'path': file_path})
        return FileInfo(**data)

    def download_file(self, file_path: str, save_path: Optional[str] = None) -> Union[bytes, str]:
        """
        Download a file from the API.
        
        This method downloads a file and either returns the content as bytes
        or saves it to a local file path, depending on the save_path parameter.
        
        Args:
            file_path (str): Path to the file relative to the comp directory
            save_path (str, optional): Local path to save the file. If None, returns bytes. Defaults to None.
            
        Returns:
            Union[bytes, str]: File content as bytes if save_path is None, otherwise the save path
            
        Raises:
            JuiceWRLDAPIError: If the download fails
            NotFoundError: If the file doesn't exist
            
        Example:
            >>> api = JuiceWRLDAPI()
            # Download as bytes
            >>> content = api.download_file("Compilation/2. Unreleased Discography/song.mp3")
            >>> print(f"Downloaded {len(content)} bytes")
            
            # Save to file
            >>> path = api.download_file("Compilation/2. Unreleased Discography/song.mp3", "song.mp3")
            >>> print(f"Saved to: {path}")
        """
        url = f"{self.base_url}/juicewrld/files/download/?path={quote(file_path)}"
        
        try:
            response = self.session.get(url, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            if save_path:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return save_path
            else:
                return response.content
        except requests.exceptions.RequestException as e:
            raise JuiceWRLDAPIError(f"Download failed: {str(e)}")

    def get_cover_art(self, file_path: str) -> bytes:
        """
        Extract cover art from an audio file.
        
        This method retrieves the embedded cover art from audio files
        such as MP3s. The cover art is returned as raw bytes that can
        be saved as an image file.
        
        Args:
            file_path (str): Path to the audio file relative to the comp directory
            
        Returns:
            bytes: Cover art image data
            
        Raises:
            JuiceWRLDAPIError: If cover art retrieval fails
            NotFoundError: If the file doesn't exist
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> cover_art = api.get_cover_art("Compilation/2. Unreleased Discography/song.mp3")
            >>> with open("cover.png", "wb") as f:
            ...     f.write(cover_art)
        """
        url = f"{self.base_url}/juicewrld/files/cover-art/?path={quote(file_path)}"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise JuiceWRLDAPIError(f"Cover art retrieval failed: {str(e)}")

    def create_zip(self, file_paths: List[str]) -> bytes:
        """
        Create a ZIP archive containing multiple files.
        
        This method creates a ZIP file containing all the specified files
        and returns the ZIP content as bytes.
        
        Args:
            file_paths (List[str]): List of file paths to include in the ZIP
            
        Returns:
            bytes: ZIP file content as bytes
            
        Raises:
            JuiceWRLDAPIError: If ZIP creation fails
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> file_paths = ["song1.mp3", "song2.mp3", "song3.mp3"]
            >>> zip_content = api.create_zip(file_paths)
            >>> with open("songs.zip", "wb") as f:
            ...     f.write(zip_content)
        """
        data = {'paths': file_paths}
        response = self.session.post(
            f"{self.base_url}/juicewrld/files/zip-selection/",
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.content

    def start_zip_job(self, file_paths: List[str]) -> str:
        """
        Start a background ZIP creation job.
        
        This method starts a ZIP creation job in the background and returns
        a job ID that can be used to check the status and download the result.
        
        Args:
            file_paths (List[str]): List of file paths to include in the ZIP
            
        Returns:
            str: Job ID for tracking the ZIP creation progress
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> file_paths = ["song1.mp3", "song2.mp3", "song3.mp3"]
            >>> job_id = api.start_zip_job(file_paths)
            >>> print(f"Started ZIP job: {job_id}")
        """
        data = {'paths': file_paths}
        response = self._post('/juicewrld/start-zip-job/', data)
        return response.get('job_id')

    def get_zip_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of a ZIP creation job.
        
        Args:
            job_id (str): The job ID returned by start_zip_job()
            
        Returns:
            Dict[str, Any]: Dictionary containing job status and progress information
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> status = api.get_zip_job_status("job_12345")
            >>> print(f"Status: {status['status']}")
            >>> print(f"Progress: {status['progress']}%")
        """
        return self._get(f'/juicewrld/zip-job-status/{job_id}/')

    def cancel_zip_job(self, job_id: str) -> bool:
        """
        Cancel a ZIP creation job.
        
        Args:
            job_id (str): The job ID returned by start_zip_job()
            
        Returns:
            bool: True if the job was successfully cancelled, False otherwise
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> success = api.cancel_zip_job("job_12345")
            >>> if success:
            ...     print("Job cancelled successfully")
        """
        try:
            self._post(f'/juicewrld/cancel-zip-job/{job_id}/')
            return True
        except:
            return False

    def search_songs(self, query: str, category: Optional[str] = None, 
                    year: Optional[int] = None, tags: Optional[List[str]] = None,
                    limit: int = 50, offset: int = 0) -> SearchResult:
        """
        Search for songs with advanced filtering options.
        
        This method provides comprehensive search functionality across all
        song categories with multiple filtering options.
        
        Args:
            query (str): Search query for song titles or content
            category (str, optional): Filter by song category. Defaults to None.
            year (int, optional): Filter by recording/release year. Defaults to None.
            tags (List[str], optional): Filter by musical tags. Defaults to None.
            limit (int, optional): Maximum number of results. Defaults to 50.
            offset (int, optional): Number of results to skip for pagination. Defaults to 0.
            
        Returns:
            SearchResult: Object containing search results and metadata
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> results = api.search_songs("lucid dreams", category="released", limit=10)
            >>> print(f"Found {results.total} songs")
            >>> for song in results.songs:
            ...     print(f"- {song.name}")
        """
        page = (offset // limit) + 1 if limit > 0 else 1
        params = {'search': query, 'page_size': limit, 'page': page}
        if category:
            params['category'] = category
        if year:
            params['year'] = year
        if tags:
            params['tags'] = ','.join(tags)
            
        data = self._get('/juicewrld/songs/', params=params)
        
        songs = []
        for song_data in data.get('results', []):
            if isinstance(song_data, dict):
                era_obj = Era(
                    id=song_data.get('era', {}).get('id', 0),
                    name=song_data.get('era', {}).get('name', 'Unknown'),
                    description=song_data.get('era', {}).get('description', ''),
                    time_frame=song_data.get('era', {}).get('time_frame', '')
                )
                
                song = Song(
                    id=song_data.get('id', 0),
                    name=song_data.get('name', 'Unknown'),
                    original_key=song_data.get('original_key', ''),
                    category=song_data.get('category', 'unknown'),
                    era=era_obj,
                    track_titles=song_data.get('track_titles', []),
                    credited_artists=song_data.get('credited_artists', ''),
                    producers=song_data.get('producers', ''),
                    engineers=song_data.get('engineers', ''),
                    additional_information=song_data.get('additional_information', ''),
                    file_names=song_data.get('file_names', ''),
                    instrumentals=song_data.get('instrumentals', ''),
                    recording_locations=song_data.get('recording_locations', ''),
                    record_dates=song_data.get('record_dates', ''),
                    preview_date=song_data.get('preview_date', ''),
                    release_date=song_data.get('release_date', ''),
                    dates=song_data.get('dates', ''),
                    length=song_data.get('length', ''),
                    leak_type=song_data.get('leak_type', ''),
                    date_leaked=song_data.get('date_leaked', ''),
                    notes=song_data.get('notes', ''),
                    image_url=song_data.get('image_url', ''),
                    session_titles=song_data.get('session_titles', ''),
                    session_tracking=song_data.get('session_tracking', ''),
                    instrumental_names=song_data.get('instrumental_names', ''),
                    public_id=song_data.get('public_id', '')
                )
                songs.append(song)
        
        return SearchResult(
            songs=songs,
            total=data.get('count', 0),
            category=category,
            query_time='0ms'
        )

    def get_songs_by_category(self, category: str, page: int = 1, 
                            page_size: int = 20) -> Dict[str, Any]:
        """
        Get songs filtered by a specific category.
        
        This is a convenience method that wraps get_songs() with category filtering.
        
        Args:
            category (str): Song category to filter by (e.g., 'released', 'unreleased')
            page (int, optional): Page number for pagination. Defaults to 1.
            page_size (int, optional): Number of songs per page. Defaults to 20.
            
        Returns:
            Dict[str, Any]: Dictionary containing songs and pagination info
            
        Example:
            >>> api = JuiceWRLDAPI()
            >>> unreleased = api.get_songs_by_category("unreleased", page_size=10)
            >>> print(f"Found {unreleased['count']} unreleased songs")
        """
        return self.get_songs(page, category, page_size=page_size)





    def close(self):
        """
        Close the API client and clean up resources.
        
        This method closes the underlying HTTP session and should be called
        when you're done using the API client to free up system resources.
        
        Example:
            >>> api = JuiceWRLDAPI()
            >>> # Use the API...
            >>> api.close()
        """
        self.session.close()

    def __enter__(self):
        """
        Enter the context manager.
        
        Returns:
            JuiceWRLDAPI: The API client instance
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.
        
        This method automatically closes the API client when exiting
        a context manager (with statement).
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        """
        self.close()

