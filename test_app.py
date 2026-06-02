import pytest
import pandas as pd
import base64
from App import fetch_yt_video, get_table_download_link

def test_fetch_yt_video():
    """
    Test that the fetch_yt_video function returns the expected static string.
    """
    # Arrange
    test_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Act
    result = fetch_yt_video(test_link)
    
    # Assert
    assert result == "Video Tip"
    
def test_get_table_download_link():
    """
    Test that the function generates a correct HTML anchor tag for a CSV download.
    """
    # Arrange
    data = {
        'Name': ['Alice', 'Bob'],
        'Score': [85, 92]
    }
    df = pd.DataFrame(data)
    filename = "test_report.csv"
    text_label = "Download My Report"
    
    # Act
    html_link = get_table_download_link(df, filename, text_label)
    
    # Assert
    # 1. Check if it's an anchor tag
    assert html_link.startswith('<a href=')
    assert html_link.endswith('</a>')
    
    # 2. Check if the filename is injected correctly
    assert f'download="{filename}"' in html_link
    
    # 3. Check if the display text is injected correctly
    assert f'>{text_label}</a>' in html_link
    
    # 4. Check if the base64 data structure is present
    assert 'data:file/csv;base64,' in html_link

def test_get_table_download_link_content_encoding():
    """
    Test that the data encoded in the link matches the dataframe content.
    """
    # Arrange
    data = {'Name': ['Charlie']}
    df = pd.DataFrame(data)
    
    # Act
    html_link = get_table_download_link(df, "data.csv", "DL")
    
    # Extract the base64 string from the href
    # Format: <a href="data:file/csv;base64,EncodedStringHere" download="...">
    start_index = html_link.find('base64,') + 7
    end_index = html_link.find('"', start_index)
    encoded_csv = html_link[start_index:end_index]
    
    # Decode the base64 string
    decoded_csv = base64.b64decode(encoded_csv).decode('utf-8')
    
    # Assert
    # The CSV should have the header 'Name' and the value 'Charlie'
    assert 'Name' in decoded_csv
    assert 'Charlie' in decoded_csv
