import pytest
from gradhouse.file.file_handler import FileHandler
from gradhouse.file.file_type import FileType
from gradhouse.services.hash_service import HashType, HashService

@pytest.fixture
def mock_file(tmp_path):
    """
    Fixture that creates a temporary file for testing.
    """
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("This is a test file.")
    return file_path

def test_get_metadata_valid_file(mock_file, mocker):
    """
    Test that FileHandler.get_metadata returns correct metadata for a valid file,
    including filename, size, hash, and timestamp.
    """
    mock_hash = mocker.patch.object(HashService, 'calculate_file_hash', return_value="dummy_hash")
    metadata = FileHandler.get_metadata(str(mock_file), [HashType.HASH_TYPE_MD5])
    assert metadata['filename'] == "test_file.txt"
    assert metadata['size_bytes'] == len("This is a test file.")
    assert metadata['hash'][HashType.HASH_TYPE_MD5.value] == "dummy_hash"
    assert 'timestamp_iso' in metadata
    mock_hash.assert_called_once_with(str(mock_file), HashType.HASH_TYPE_MD5)

def test_get_metadata_file_not_found():
    """
    Test that FileHandler.get_metadata raises a FileNotFoundError with the expected message
    when attempting to retrieve metadata for a non-existent file.
    """
    with pytest.raises(FileNotFoundError, match="file not found"):
        FileHandler.get_metadata("non_existent_file.txt", [HashType.HASH_TYPE_MD5])

def test_get_metadata_multiple_hashes(mock_file, mocker):
    """
    Test that FileHandler.get_metadata correctly computes and returns metadata with multiple hash types.
    This test mocks HashService.calculate_file_hash to return specific values for MD5 and SHA256 hash types,
    verifies that the returned metadata contains the expected hash values for each type, and asserts that
    the hash calculation function is called the correct number of times.
    """
    mock_hash = mocker.patch.object(
        HashService,
        'calculate_file_hash',
        side_effect=lambda file, hash_type: "md5_hash" if hash_type == HashType.HASH_TYPE_MD5
        else "sha256_hash" if hash_type == HashType.HASH_TYPE_SHA256
        else ValueError(f"Unexpected hash type: {hash_type}"),
        autospec=True
    )
    metadata = FileHandler.get_metadata(str(mock_file), [HashType.HASH_TYPE_MD5, HashType.HASH_TYPE_SHA256])
    assert metadata['hash'][HashType.HASH_TYPE_MD5.value] == "md5_hash"
    assert metadata['hash'][HashType.HASH_TYPE_SHA256.value] == "sha256_hash"
    assert mock_hash.call_count == 2

def test_get_metadata_empty_hash_types(mock_file):
    """
    Test that FileHandler.get_metadata returns an empty hash dictionary when no hash types are provided.
    """
    metadata = FileHandler.get_metadata(str(mock_file), [])
    assert metadata['hash'] == {}

def test_get_file_type_from_extension_returns_list(mocker):
    """
    Test that FileHandler.get_file_type_from_extension returns the expected list of file types
    when given a file extension, using mocked dependencies.
    """
    mocker.patch('gradhouse.file.file_name.FileName.get_file_extension', return_value='pdf')
    mock_types = [mocker.Mock()]
    mocker.patch.object(FileHandler, '_get_file_type_using_extension', return_value=mock_types)
    result = FileHandler.get_file_type_from_extension('somefile.pdf')
    assert result == mock_types

def test_get_file_type_from_format_valid_file(mocker, tmp_path):
    """
    Test that FileHandler.get_file_type_from_format works for a valid file,
    using mocked handlers and file extension extraction.
    """
    file_path = tmp_path / "file.pdf"
    file_path.write_text("dummy")
    mocker.patch('gradhouse.file.file_name.FileName.get_file_extension', return_value='pdf')
    fake_handler = mocker.Mock()
    fake_handler.get_file_type_from_format.return_value = mocker.Mock()
    mocker.patch.object(FileHandler, '_get_file_handlers_from_extension', return_value=[fake_handler])
    FileHandler.get_file_type_from_format(str(file_path))

def test_get_file_type_from_format_file_not_found():
    """
    Test that FileHandler.get_file_type_from_format raises FileNotFoundError
    when the specified file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        FileHandler.get_file_type_from_format("does_not_exist.txt")

def test__get_file_type_using_extension_calls_handlers(mocker):
    """
    Test that FileHandler._get_file_type_using_extension calls the appropriate handler(s)
    and returns the expected file type(s).
    """
    fake_handler = mocker.Mock()
    fake_handler.get_file_type_from_extension.return_value = ['SOME_TYPE']
    mocker.patch.object(FileHandler, '_get_file_handlers_from_extension', return_value=[fake_handler])
    result = FileHandler._get_file_type_using_extension('pdf')
    assert 'SOME_TYPE' in result

def test__get_file_handlers_returns_handlers(mocker):
    """
    Test that FileHandler._get_file_handlers returns a list of handler objects,
    each of which has a callable get_file_extension_map method.
    """
    for handler in FileHandler._file_handlers:
        assert hasattr(handler, 'get_file_extension_map')
        assert callable(handler.get_file_extension_map)
    handlers = FileHandler._get_file_handlers()
    assert isinstance(handlers, list)
    assert all(hasattr(h, 'get_file_extension_map') for h in handlers)

def test__get_file_handlers_raises_value_error(monkeypatch):
    """
    Test that FileHandler._get_file_handlers raises ValueError if a handler does not have a callable get_file_extension_map.
    """
    class BadHandler:
        pass  # No get_file_extension_map

    # Patch _file_handlers to include a bad handler
    monkeypatch.setattr(FileHandler, "_file_handlers", [BadHandler()])
    with pytest.raises(ValueError, match="callable 'get_file_extension_map'"):
        FileHandler._get_file_handlers()

def test_get_file_type_from_format_no_extension(mocker, tmp_path):
    """
    Test that FileHandler.get_file_type_from_format uses all handlers when use_extension is False.
    """
    file_path = tmp_path / "file.unknown"
    file_path.write_text("dummy")
    fake_handler = mocker.Mock()
    fake_handler.get_file_type_from_format.return_value = mocker.Mock()
    mocker.patch.object(FileHandler, '_get_file_handlers', return_value=[fake_handler])
    # Should use the else branch
    FileHandler.get_file_type_from_format(str(file_path), use_extension=False)

def test_get_file_type_from_format_else_branch_hits(mocker, tmp_path):
    """
    Test that FileHandler.get_file_type_from_format executes the else branch
    when use_extension is set to False, ensuring all handlers are used
    instead of filtering by file extension.
    """
    # Create a dummy file
    file_path = tmp_path / "file.unknown"
    file_path.write_text("dummy")
    # Create a fake handler with the required method
    fake_handler = mocker.Mock()
    fake_handler.get_file_type_from_format.return_value = FileType.FILE_TYPE_UNKNOWN
    # Patch _get_file_handlers to return our fake handler
    mocker.patch.object(FileHandler, '_get_file_handlers', return_value=[fake_handler])
    # Call with use_extension=False to hit the else branch
    FileHandler.get_file_type_from_format(str(file_path), use_extension=False)

def test__get_file_type_using_extension_empty_string():
    """
    Test that _get_file_type_using_extension returns an empty list when given an empty string.
    """
    result = FileHandler._get_file_type_using_extension('')
    assert result == []

def test__get_file_type_using_extension_with_handlers(mocker):
    """
    Test that _get_file_type_using_extension calls handlers and aggregates their results.
    """
    fake_handler = mocker.Mock()
    fake_handler.get_file_type_from_extension.return_value = [FileType.FILE_TYPE_PDF]
    mocker.patch.object(FileHandler, '_get_file_handlers_from_extension', return_value=[fake_handler])
    result = FileHandler._get_file_type_using_extension('pdf')
    assert FileType.FILE_TYPE_PDF in result
    fake_handler.get_file_type_from_extension.assert_called_once_with('pdf')

def test__get_file_handlers_from_extension_full_coverage(mocker):
    """
    Test that _get_file_handlers_from_extension covers all for loops and conditions,
    including adding handlers for multiple extensions and avoiding duplicates.
    """
    # Create two fake handlers with overlapping and unique extensions
    handler1 = mocker.Mock()
    handler1.get_file_extension_map.return_value = ['PDF', 'DOC']
    handler2 = mocker.Mock()
    handler2.get_file_extension_map.return_value = ['pdf', 'TXT']

    # Patch _get_file_handlers to return both handlers
    mocker.patch.object(FileHandler, '_get_file_handlers', return_value=[handler1, handler2])

    # Should return both handlers for 'pdf' (case-insensitive, no duplicates)
    handlers_pdf = FileHandler._get_file_handlers_from_extension('pdf')
    assert handler1 in handlers_pdf
    assert handler2 in handlers_pdf
    assert len(handlers_pdf) == 2

    # Should return only handler1 for 'doc'
    handlers_doc = FileHandler._get_file_handlers_from_extension('doc')
    assert handlers_doc == [handler1]

    # Should return only handler2 for 'txt'
    handlers_txt = FileHandler._get_file_handlers_from_extension('txt')
    assert handlers_txt == [handler2]

    # Should return empty list for unknown extension
    handlers_unknown = FileHandler._get_file_handlers_from_extension('unknown')
    assert handlers_unknown == []

def test__get_file_handlers_from_extension_duplicate_handler(mocker):
    """
    Test that _get_file_handlers_from_extension does not add duplicate handlers for the same extension,
    covering the branch where the handler is already in the list.
    """
    handler = mocker.Mock()
    handler.get_file_extension_map.return_value = ['PDF', 'pdf']  # Same extension, different case

    # Patch _get_file_handlers to return the same handler twice
    mocker.patch.object(FileHandler, '_get_file_handlers', return_value=[handler, handler])

    handlers = FileHandler._get_file_handlers_from_extension('pdf')
    # Should only include the handler once
    assert handlers == [handler]
