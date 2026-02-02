"""Tests for input_sources module."""

import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from claude_dev_cli.input_sources import (
    read_text_input,
    read_file_input,
    read_pdf_input,
    read_url_input,
    get_input_content
)

# Check for optional dependencies
try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    import requests
    import bs4
    HAS_URL_SUPPORT = True
except ImportError:
    HAS_URL_SUPPORT = False


def test_read_text_input():
    """Test reading direct text input."""
    text = "This is a test specification"
    result = read_text_input(text)
    assert result == text


def test_read_file_input(tmp_path):
    """Test reading from a file."""
    # Create a test file
    test_file = tmp_path / "spec.txt"
    content = "File specification content"
    test_file.write_text(content)
    
    result = read_file_input(str(test_file))
    assert result == content


def test_read_file_input_not_found():
    """Test reading from non-existent file."""
    with pytest.raises(FileNotFoundError):
        read_file_input("nonexistent.txt")


def test_read_pdf_input_no_module():
    """Test PDF reading without pypdf installed."""
    # Mock the import to raise ImportError
    with patch('builtins.__import__', side_effect=ImportError("No module named 'pypdf'")):
        with pytest.raises(ImportError, match="PDF support requires pypdf"):
            read_pdf_input("test.pdf")


@pytest.mark.skipif(not HAS_PYPDF, reason="pypdf not installed")
def test_read_pdf_input_success(tmp_path):
    """Test successful PDF reading."""
    # Create a mock PDF file
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_text("dummy")  # Just need it to exist
    
    # Mock PdfReader
    mock_page = Mock()
    mock_page.extract_text.return_value = "PDF content here"
    
    mock_reader = Mock()
    mock_reader.pages = [mock_page]
    
    # Patch where PdfReader is imported (inside the function)
    with patch('pypdf.PdfReader', return_value=mock_reader):
        result = read_pdf_input(str(pdf_file))
        assert result == "PDF content here"


@pytest.mark.skipif(not HAS_PYPDF, reason="pypdf not installed")
def test_read_pdf_input_empty_pdf(tmp_path):
    """Test PDF with no extractable text."""
    pdf_file = tmp_path / "empty.pdf"
    pdf_file.write_text("dummy")
    
    mock_page = Mock()
    mock_page.extract_text.return_value = None
    
    mock_reader = Mock()
    mock_reader.pages = [mock_page]
    
    # Patch where PdfReader is imported (inside the function)
    with patch('pypdf.PdfReader', return_value=mock_reader):
        with pytest.raises(ValueError, match="No text could be extracted"):
            read_pdf_input(str(pdf_file))


def test_read_url_input_no_modules():
    """Test URL reading without required modules."""
    with patch.dict('sys.modules', {'requests': None}):
        with pytest.raises(ImportError, match="URL support requires"):
            read_url_input("https://example.com")


def test_read_url_input_invalid_url():
    """Test URL reading with invalid URL."""
    # Mock the imports to succeed so we can test the URL validation
    mock_requests = MagicMock()
    mock_bs4 = MagicMock()
    
    with patch.dict('sys.modules', {'requests': mock_requests, 'bs4': mock_bs4}):
        with pytest.raises(ValueError, match="Invalid URL format"):
            read_url_input("not-a-url")


@pytest.mark.skipif(not HAS_URL_SUPPORT, reason="requests/bs4 not installed")
def test_read_url_input_plain_text():
    """Test URL reading with plain text response."""
    mock_response = Mock()
    mock_response.headers = {'Content-Type': 'text/plain'}
    mock_response.text = "Plain text content"
    mock_response.raise_for_status = Mock()
    
    # Patch at the module level where it's imported
    with patch('requests.get', return_value=mock_response):
        result = read_url_input("https://example.com")
        assert result == "Plain text content"


@pytest.mark.skipif(not HAS_URL_SUPPORT, reason="requests/bs4 not installed")
def test_read_url_input_html():
    """Test URL reading with HTML response."""
    html_content = """
    <html>
        <head><title>Test</title></head>
        <body>
            <script>alert('test');</script>
            <h1>Main Content</h1>
            <p>This is text</p>
        </body>
    </html>
    """
    
    mock_response = Mock()
    mock_response.headers = {'Content-Type': 'text/html'}
    mock_response.content = html_content.encode()
    mock_response.raise_for_status = Mock()
    
    # Mock BeautifulSoup behavior
    mock_soup = Mock()
    mock_soup.get_text.return_value = "Main Content\nThis is text"
    mock_soup.__call__ = Mock(return_value=[])  # For script removal
    
    with patch('requests.get', return_value=mock_response):
        with patch('bs4.BeautifulSoup', return_value=mock_soup):
            result = read_url_input("https://example.com")
            assert "Main Content" in result


@pytest.mark.skipif(not HAS_URL_SUPPORT, reason="requests/bs4 not installed")
def test_read_url_input_json():
    """Test URL reading with JSON response."""
    json_data = {"key": "value", "nested": {"data": 123}}
    
    mock_response = Mock()
    mock_response.headers = {'Content-Type': 'application/json'}
    mock_response.json.return_value = json_data
    mock_response.raise_for_status = Mock()
    
    with patch('requests.get', return_value=mock_response):
        result = read_url_input("https://example.com/api")
        assert '"key": "value"' in result


def test_get_input_content_no_source():
    """Test get_input_content with no sources provided."""
    with pytest.raises(ValueError, match="No input source provided"):
        get_input_content()


def test_get_input_content_multiple_sources():
    """Test get_input_content with multiple sources."""
    with pytest.raises(ValueError, match="Multiple input sources provided"):
        get_input_content(description="test", file_path="file.txt")


def test_get_input_content_description():
    """Test get_input_content with description."""
    content, source = get_input_content(description="Test description")
    assert content == "Test description"
    assert source == "text description"


def test_get_input_content_file(tmp_path):
    """Test get_input_content with file."""
    test_file = tmp_path / "spec.txt"
    test_file.write_text("File content")
    
    console = Mock()
    content, source = get_input_content(file_path=str(test_file), console=console)
    assert content == "File content"
    assert "spec.txt" in source
    console.print.assert_called()


@pytest.mark.skipif(not HAS_PYPDF, reason="pypdf not installed")
def test_get_input_content_pdf(tmp_path):
    """Test get_input_content with PDF."""
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_text("dummy")
    
    mock_page = Mock()
    mock_page.extract_text.return_value = "PDF text"
    
    mock_reader = Mock()
    mock_reader.pages = [mock_page]
    
    console = Mock()
    with patch('pypdf.PdfReader', return_value=mock_reader):
        content, source = get_input_content(pdf_path=str(pdf_file), console=console)
        assert content == "PDF text"
        assert "PDF" in source


@pytest.mark.skipif(not HAS_URL_SUPPORT, reason="requests/bs4 not installed")
def test_get_input_content_url():
    """Test get_input_content with URL."""
    mock_response = Mock()
    mock_response.headers = {'Content-Type': 'text/plain'}
    mock_response.text = "URL content"
    mock_response.raise_for_status = Mock()
    
    console = Mock()
    with patch('requests.get', return_value=mock_response):
        content, source = get_input_content(url="https://example.com", console=console)
        assert content == "URL content"
        assert "URL" in source


def test_get_input_content_import_error_graceful():
    """Test that ImportError is raised gracefully with helpful message."""
    pdf_file = Path("test.pdf")
    
    console = Mock()
    # Mock the import to fail
    with patch('builtins.__import__', side_effect=ImportError("No module named 'pypdf'")):
        with pytest.raises(ImportError, match="PDF support requires pypdf"):
            get_input_content(pdf_path=str(pdf_file), console=console)
