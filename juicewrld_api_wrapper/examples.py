#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client import JuiceWRLDAPI
from exceptions import JuiceWRLDAPIError, RateLimitError, NotFoundError
import json

def basic_api_usage():
    print("=== Basic API Usage ===")
    
    api = JuiceWRLDAPI(base_url="https://juicewrldapi.com")
    
    try:
        overview = api.get_api_overview()
        print(f"API Overview: {overview.get('title', 'N/A')}")
        
        stats = api.get_stats()
        print(f"Total Songs: {stats.total_songs}")
        print(f"Category Stats: {stats.category_stats}")
        
        categories = api.get_categories()
        print(f"Available Categories: {[cat['label'] for cat in categories]}")
        
        eras = api.get_eras()
        print(f"Available Eras: {[era.name for era in eras[:5]]}...")
        
    except JuiceWRLDAPIError as e:
        print(f"API Error: {e}")
    finally:
        api.close()

def song_search_examples():
    print("\n=== Song Search Examples ===")
    
    api = JuiceWRLDAPI()
    
    try:
        print("Testing song retrieval instead of search (search endpoint may be limited)")
        
        songs = api.get_songs(page=1, page_size=5)
        print(f"Retrieved {len(songs['results'])} songs from first page")
        
        for song in songs['results'][:3]:
            print(f"- {song.name} ({song.category}) - {song.length}")
            print(f"  Era: {song.era.name}")
            print(f"  Producers: {song.producers}")
        
        unreleased_songs = api.get_songs_by_category("unreleased", page=1, page_size=5)
        print(f"\nUnreleased Songs (Page 1): {unreleased_songs['count']} total")
        
        for song in unreleased_songs['results'][:3]:
            print(f"- {song.name} - {song.length}")
        
    except JuiceWRLDAPIError as e:
        print(f"Song retrieval error: {e}")
    finally:
        api.close()

def file_operations_examples():
    print("\n=== File Operations Examples ===")
    
    api = JuiceWRLDAPI()
    
    try:
        print("Testing file operations with valid paths")
        
        try:
            directory_info = api.browse_files(path="", search="")
            print(f"Root directory - Files: {directory_info.total_files}, Directories: {directory_info.total_directories}")
            
            if directory_info.items:
                print("Sample items:")
                for item in directory_info.items[:3]:
                    if item.type == 'file':
                        print(f"  File: {item.name} ({item.size_human})")
                    else:
                        print(f"  Directory: {item.name}")
                
                if directory_info.total_directories > 0:
                    print(f"\nTrying to browse a subdirectory...")
                    try:
                        subdir = next(item for item in directory_info.items if item.type == 'directory')
                        subdir_info = api.browse_files(path=subdir.name, search="")
                        print(f"Subdirectory '{subdir.name}' - Files: {subdir_info.total_files}, Directories: {subdir_info.total_directories}")
                    except JuiceWRLDAPIError as e:
                        print(f"Subdirectory browsing error: {e}")
        except JuiceWRLDAPIError as e:
            print(f"File browsing error: {e}")
        
    except JuiceWRLDAPIError as e:
        print(f"File Operations Error: {e}")
    finally:
        api.close()

def advanced_search_examples():
    print("\n=== Advanced Search Examples ===")
    
    api = JuiceWRLDAPI()
    
    try:
        print("Testing alternative search methods")
        
        try:
                era_songs = api.get_songs(era="jute", page_size=5)
                print(f"JUTE Era Songs: {era_songs['count']} total")
                
                for song in era_songs['results'][:3]:
                    print(f"- {song.name} ({song.category}) - {song.length}")
            except JuiceWRLDAPIError as e2:
                print(f"Era-based search also failed: {e2}")
                print("Trying category-based search...")
                
                try:
                    released_songs = api.get_songs_by_category("released", page_size=5)
                    print(f"Released Songs: {released_songs['count']} total")
                    
                    for song in released_songs['results'][:3]:
                        print(f"- {song.name} ({song.category}) - {song.length}")
                except JuiceWRLDAPIError as e3:
                    print(f"Category-based search failed: {e3}")
        
    except JuiceWRLDAPIError as e:
        print(f"Advanced Search Error: {e}")
    finally:
        api.close()

def context_manager_examples():
    print("\n=== Context Manager Examples ===")
    
    with JuiceWRLDAPI() as api:
        try:
            stats = api.get_stats()
            print(f"Using context manager - Total songs: {stats.total_songs}")
            
            songs = api.get_songs(page=1, page_size=3)
            print(f"Retrieved {len(songs['results'])} songs")
            
            if songs['results']:
                print("Sample songs:")
                for song in songs['results']:
                    print(f"  - {song.name} ({song.category}) - Era: {song.era.name}")
            
        except JuiceWRLDAPIError as e:
            print(f"Context manager error: {e}")

def error_handling_examples():
    print("\n=== Error Handling Examples ===")
    
    try:
        api = JuiceWRLDAPI(base_url="https://invalid-url.com")
        api.get_api_overview()
    except JuiceWRLDAPIError as e:
        print(f"✓ Expected error for invalid URL: {e}")
    
    try:
        api = JuiceWRLDAPI()
        api.get_song(999999)
    except NotFoundError as e:
        print(f"✓ Expected NotFoundError: {e}")
    except JuiceWRLDAPIError as e:
        print(f"✓ Expected API error: {e}")

def main():
    print("Juice WRLD API Wrapper Examples")
    print("=" * 50)
    
    basic_api_usage()
    song_search_examples()
    file_operations_examples()
    advanced_search_examples()
    context_manager_examples()
    error_handling_examples()
    
    print("\n" + "=" * 50)
    print("Examples completed!")

if __name__ == "__main__":
    main()
