# File: test_manifest.py
# Description: Unit tests for the Manifest class.
#
# Copyright (c) 2025 Jason Stuber
# Licensed under the MIT License. See the LICENSE file for more details.
#
# Disclaimer:
# This software is not affiliated with, endorsed by, or sponsored by arXiv, Cornell University, or any of their affiliates.
# All arXiv data, logos, and trademarks are the property of their respective owners.
# Users of this software are solely responsible for ensuring their use of arXiv data complies with arXiv's policies and terms.
# For more information, see:
# - https://arxiv.org/help/license
# - https://info.arxiv.org/help/bulk_data_s3.html

import copy
import matplotlib.pyplot as plt
import os
import pytest
import tempfile
import warnings

from gradhouse.arxiv.manifest import Manifest

# Sample valid xml_dict
valid_xml_dict = {
    'arXivSRC': {
        'file': [
            {
                'content_md5sum': 'cacbfede21d5dfef26f367ec99384546',
                'filename': 'src/arXiv_src_0001_001.tar',
                'first_item': 'astro-ph0001001',
                'last_item': 'quant-ph0001119',
                'md5sum': '949ae880fbaf4649a485a8d9e07f370b',
                'num_items': '2364',
                'seq_num': '1',
                'size': '225605507',
                'timestamp': '2010-12-23 00:13:59',
                'yymm': '0001'
            }
        ],
        'timestamp': '2010-12-23 00:00:00'
    }
}

def test_manifest_constructor():
    """
    Test the constructor of the Manifest class.
    Ensure that the manifest is initialized with default values.
    """
    manifest = Manifest()
    assert manifest._manifest == {
        'metadata': {},
        'contents': []
    }

def test_manifest_clear():
    """
    Test the clear method of the Manifest class.
    Ensure that the manifest is cleared and reset to default values.
    """
    manifest = Manifest()
    # Modify the manifest to simulate existing data
    manifest._manifest['metadata'] = {'key': 'value'}
    manifest._manifest['contents'] = [{'filename': 'test.txt'}]

    # Call the clear method
    manifest.clear()

    # Assert that the manifest is reset to default values
    assert manifest._manifest == {
        'metadata': {},
        'contents': []
    }

def test_manifest_set_defaults():
    """
    Test the _set_defaults method of the Manifest class.
    Ensure that the manifest is set to default values.
    """
    manifest = Manifest()
    # Modify the manifest to simulate existing data
    manifest._manifest['metadata'] = {'key': 'value'}
    manifest._manifest['contents'] = [{'filename': 'test.txt'}]

    # Call the _set_defaults method
    manifest._set_defaults()

    # Assert that the manifest is reset to default values
    assert manifest._manifest == {
        'metadata': {},
        'contents': []
    }

def test_is_arxiv_keys_present_with_valid_data():
    """
    Test that the method returns True for a valid xml_dict.
    """
    assert Manifest._is_arxiv_keys_present(valid_xml_dict) is True

def test_is_arxiv_keys_present_with_missing_top_level_key():
    """
    Test that the method returns False when the top-level key is missing.
    """
    invalid_dict = {}
    assert Manifest._is_arxiv_keys_present(invalid_dict) is False

def test_is_arxiv_keys_present_with_missing_arxivsrc_keys():
    """
    Test that the method returns False when 'arXivSRC' keys are missing.
    """

    invalid_dict = copy.deepcopy(valid_xml_dict)
    del invalid_dict['arXivSRC']['file']

    assert Manifest._is_arxiv_keys_present(invalid_dict) is False

    invalid_dict = copy.deepcopy(valid_xml_dict)
    del invalid_dict['arXivSRC']['timestamp']

    assert Manifest._is_arxiv_keys_present(invalid_dict) is False


def test_is_arxiv_keys_valid_with_non_string_value_in_timestamp():
    """
    Test that the method returns False when a value in 'file' is not a string.
    """
    invalid_dict = copy.deepcopy(valid_xml_dict)
    invalid_dict['arXivSRC']['timestamp'] = 1234  # should be a string

    assert Manifest._is_arxiv_keys_present(invalid_dict) is False


def test_is_arxiv_keys_present_with_invalid_file_structure():
    """
    Test that the method returns False when 'file' entries have missing keys.
    """
    invalid_dict = {
        'arXivSRC': {
            'file': [
                {
                    'content_md5sum': 'cacbfede21d5dfef26f367ec99384546',
                    'filename': 'src/arXiv_src_0001_001.tar'
                    # Missing other required keys
                }
            ],
            'timestamp': '2010-12-23 00:00:00'
        }
    }
    assert Manifest._is_arxiv_keys_present(invalid_dict) is False

def test_is_arxiv_keys_present_with_invalid_types():
    """
    Test that the method returns False when data types are incorrect.
    """
    invalid_dict = {
        'arXivSRC': {
            'file': [
                {
                    'content_md5sum': 12345,  # Should be a string
                    'filename': 'src/arXiv_src_0001_001.tar',
                    'first_item': 'astro-ph0001001',
                    'last_item': 'quant-ph0001119',
                    'md5sum': '949ae880fbaf4649a485a8d9e07f370b',
                    'num_items': '2364',
                    'seq_num': '1',
                    'size': '225605507',
                    'timestamp': '2010-12-23 00:13:59',
                    'yymm': '0001'
                }
            ],
            'timestamp': '2010-12-23 00:00:00'
        }
    }
    assert Manifest._is_arxiv_keys_present(invalid_dict) is False

def test_convert_arxiv_timestamp_to_iso():
    """
    Test _convert_arxiv_timestamp_to_iso method for converting EST timestamp to ISO 8601 GMT.
    """
    # Input timestamp in EST
    input_timestamp = 'Mon Apr  7 04:58:03 2025'
    # Expected output in GMT
    expected_output = '2025-04-07T08:58:03+00:00'

    # Call the method
    result = Manifest._convert_arxiv_timestamp_to_iso(input_timestamp)

    # Assert the result matches the expected output
    assert result == expected_output


def test_convert_arxiv_file_entry_timestamp_to_iso():
    """
    Test _convert_arxiv_file_timestamp_to_iso method for converting EST file timestamp to ISO 8601 GMT.
    """
    # Input timestamp in EST
    input_timestamp = '2010-12-23 00:13:59'
    # Expected output in GMT
    expected_output = '2010-12-23T05:13:59+00:00'

    # Call the method
    result = Manifest._convert_arxiv_file_entry_timestamp_to_iso(input_timestamp)

    # Assert the result matches the expected output
    assert result == expected_output


def test_convert_arxiv_timestamp_to_iso_invalid_format():
    """
    Test _convert_arxiv_timestamp_to_iso method with an invalid timestamp format.
    """
    # Invalid input timestamp
    input_timestamp = 'Invalid Timestamp'

    # Assert that a ValueError is raised
    with pytest.raises(ValueError):
        Manifest._convert_arxiv_timestamp_to_iso(input_timestamp)


def test_convert_arxiv_file_entry_timestamp_to_iso_invalid_format():
    """
    Test _convert_arxiv_file_timestamp_to_iso method with an invalid timestamp format.
    """
    # Invalid input timestamp
    input_timestamp = 'Invalid Timestamp'

    # Assert that a ValueError is raised
    with pytest.raises(ValueError):
        Manifest._convert_arxiv_file_entry_timestamp_to_iso(input_timestamp)


def test_is_file_entry_consistent_valid_entry():
    """
    Test _is_file_entry_consistent with a valid file entry.
    """
    valid_entry = {
        'content_md5sum': '5f4774a944c17e67f334ebb9bf912dbf',
        'filename': 'src/arXiv_src_1508_002.tar',
        'first_item': '1508.00577',
        'last_item': '1508.01014',
        'md5sum': '271195f030a45b84d397dc8c540bde7f',
        'num_items': '438',
        'seq_num': '2',
        'size': '537749445',
        'timestamp': '2017-08-05 06:13:16',
        'yymm': '1508'
    }
    assert Manifest._is_file_entry_consistent(valid_entry) is True


def test_is_file_entry_consistent_invalid_filename():
    """
    Test _is_file_entry_consistent with an invalid filename.
    """
    invalid_entry = {
        'content_md5sum': '5f4774a944c17e67f334ebb9bf912dbf',
        'filename': 'src/invalid_filename.tar',
        'first_item': '1508.00577',
        'last_item': '1508.01014',
        'md5sum': '271195f030a45b84d397dc8c540bde7f',
        'num_items': '438',
        'seq_num': '2',
        'size': '537749445',
        'timestamp': '2017-08-05 06:13:16',
        'yymm': '1508'
    }
    assert Manifest._is_file_entry_consistent(invalid_entry) is False

def test_is_file_entry_consistent_invalid_month():
    """
    Test _is_file_entry_consistent with an invalid month in 'yymm'.
    """
    invalid_entry = {
        'content_md5sum': '5f4774a944c17e67f334ebb9bf912dbf',
        'filename': 'src/arXiv_src_1508_002.tar',
        'first_item': '1508.00577',
        'last_item': '1508.01014',
        'md5sum': '271195f030a45b84d397dc8c540bde7f',
        'num_items': '438',
        'seq_num': '2',
        'size': '537749445',
        'timestamp': '2017-08-05 06:13:16',
        'yymm': '1513'  # Invalid month
    }
    assert Manifest._is_file_entry_consistent(invalid_entry) is False

def test_is_file_entry_consistent_invalid_seq_num():
    """
    Test _is_file_entry_consistent with an invalid sequence number in the filename.
    """
    invalid_entry = {
        'content_md5sum': '5f4774a944c17e67f334ebb9bf912dbf',
        'filename': 'src/arXiv_src_1508_003.tar',  # seq_num mismatch
        'first_item': '1508.00577',
        'last_item': '1508.01014',
        'md5sum': '271195f030a45b84d397dc8c540bde7f',
        'num_items': '438',
        'seq_num': '2',
        'size': '537749445',
        'timestamp': '2017-08-05 06:13:16',
        'yymm': '1508'
    }
    assert Manifest._is_file_entry_consistent(invalid_entry) is False

def test_process_file_entry_valid():
    """
    Test _process_file_entry with a valid file entry.
    """
    valid_entry = {
        'content_md5sum': '5f4774a944c17e67f334ebb9bf912dbf',
        'filename': 'src/arXiv_src_1508_002.tar',
        'first_item': '1508.00577',
        'last_item': '1508.01014',
        'md5sum': '271195f030a45b84d397dc8c540bde7f',
        'num_items': '438',
        'seq_num': '2',
        'size': '537749445',
        'timestamp': '2017-08-05 06:13:16',
        'yymm': '1508'
    }

    processed_entry = Manifest._process_file_entry(valid_entry)

    assert processed_entry == {
        'filename': 'src/arXiv_src_1508_002.tar',
        'size_bytes': 537749445,
        'timestamp_iso': '2017-08-05T10:13:16+00:00',
        'year': 2015,
        'month': 8,
        'sequence_number': 2,
        'n_submissions': 438,
        'hash': {
            'MD5': '271195f030a45b84d397dc8c540bde7f',
            'MD5_contents': '5f4774a944c17e67f334ebb9bf912dbf',
        }
    }

def test_process_file_entry_inconsistent():
    """
    Test _process_file_entry with an inconsistent file entry.
    """
    inconsistent_entry = {
        'content_md5sum': '5f4774a944c17e67f334ebb9bf912dbf',
        'filename': 'src/arXiv_src_1508_003.tar',  # seq_num mismatch
        'first_item': '1508.00577',
        'last_item': '1508.01014',
        'md5sum': '271195f030a45b84d397dc8c540bde7f',
        'num_items': '438',
        'seq_num': '2',
        'size': '537749445',
        'timestamp': '2017-08-05 06:13:16',
        'yymm': '1508'
    }

    with pytest.raises(ValueError, match="Entry inconsistent"):
        Manifest._process_file_entry(inconsistent_entry)

def test_process_file_entry_invalid_yymm():
    """
    Test _process_file_entry with an invalid 'yymm' value.
    """
    invalid_entry = {
        'content_md5sum': '5f4774a944c17e67f334ebb9bf912dbf',
        'filename': 'src/arXiv_src_1513_002.tar',  # Invalid month
        'first_item': '1508.00577',
        'last_item': '1508.01014',
        'md5sum': '271195f030a45b84d397dc8c540bde7f',
        'num_items': '438',
        'seq_num': '2',
        'size': '537749445',
        'timestamp': '2017-08-05 06:13:16',
        'yymm': '1513'
    }

    with pytest.raises(ValueError, match="Entry inconsistent"):
        Manifest._process_file_entry(invalid_entry)

@pytest.fixture
def valid_xml_file():
    """
    Create a temporary XML file with valid arXiv data for testing.
    """
    xml_content = """<arXivSRC>
        <timestamp>Mon Apr  7 04:58:03 2025</timestamp>
        <file>
            <content_md5sum>cacbfede21d5dfef26f367ec99384546</content_md5sum>
            <filename>src/arXiv_src_0001_001.tar</filename>
            <first_item>astro-ph0001001</first_item>
            <last_item>quant-ph0001119</last_item>
            <md5sum>949ae880fbaf4649a485a8d9e07f370b</md5sum>
            <num_items>2364</num_items>
            <seq_num>1</seq_num>
            <size>225605507</size>
            <timestamp>2010-12-23 00:13:59</timestamp>
            <yymm>0001</yymm>
        </file>
        <file>
            <content_md5sum>d90df481661ccdd7e8be883796539743</content_md5sum>
            <filename>src/arXiv_src_0002_001.tar</filename>
            <first_item>astro-ph0002001</first_item>
            <last_item>quant-ph0002094</last_item>
            <md5sum>4592ab506cf775afecf4ad560d982a00</md5sum>
            <num_items>2365</num_items>
            <seq_num>1</seq_num>
            <size>227036528</size>
            <timestamp>2010-12-23 00:18:09</timestamp>
            <yymm>0002</yymm>
        </file>
    </arXivSRC>"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
        temp_file.write(xml_content.encode('utf-8'))
        temp_file_path = temp_file.name
    yield temp_file_path
    os.remove(temp_file_path)

def test_import_arxiv_xml_valid(valid_xml_file):
    """
    Test import_arxiv_xml with a valid XML file.
    """
    manifest = Manifest()
    manifest.import_arxiv_xml(valid_xml_file)

    assert manifest._manifest['metadata'] == {
        'manifest_timestamp_iso': '2025-04-07T08:58:03+00:00'
    }
    assert len(manifest._manifest['contents']) == 2
    assert manifest._manifest['contents'][0]['filename'] == 'src/arXiv_src_0001_001.tar'
    assert manifest._manifest['contents'][1]['filename'] == 'src/arXiv_src_0002_001.tar'

def test_import_arxiv_xml_file_not_found():
    """
    Test import_arxiv_xml when the file does not exist.
    """
    manifest = Manifest()

    with pytest.raises(FileNotFoundError, match='file not found'):
        manifest.import_arxiv_xml('non_existent_file.xml')

def test_import_arxiv_xml_invalid_structure():
    """
    Test import_arxiv_xml with an invalid XML structure.
    """
    invalid_xml_content = """<invalid></invalid>"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
        temp_file.write(invalid_xml_content.encode('utf-8'))
        temp_file_path = temp_file.name

    manifest = Manifest()

    with pytest.raises(TypeError, match='Entries missing in arXiv XML file'):
        manifest.import_arxiv_xml(temp_file_path)

    os.remove(temp_file_path)

def test_import_arxiv_xml_inconsistent_entry():
    """
    Test import_arxiv_xml with an inconsistent file entry.
    """
    inconsistent_xml_content = """<arXivSRC>
        <timestamp>Mon Apr  7 04:58:03 2025</timestamp>
        <file>
            <content_md5sum>d90df481661ccdd7e8be883796539743</content_md5sum>
            <filename>src/arXiv_src_0002_001.tar</filename>
            <first_item>astro-ph0002001</first_item>
            <last_item>quant-ph0002094</last_item>
            <md5sum>4592ab506cf775afecf4ad560d982a00</md5sum>
            <num_items>2365</num_items>
            <seq_num>1</seq_num>
            <size>227036528</size>
            <timestamp>2010-12-23 00:18:09</timestamp>
            <yymm>0002</yymm>
        </file>
        <file>
            <content_md5sum>cacbfede21d5dfef26f367ec99384546</content_md5sum>
            <filename>invalid_filename.tar</filename>
            <first_item>astro-ph0001001</first_item>
            <last_item>quant-ph0001119</last_item>
            <md5sum>949ae880fbaf4649a485a8d9e07f370b</md5sum>
            <num_items>2364</num_items>
            <seq_num>1</seq_num>
            <size>225605507</size>
            <timestamp>2010-12-23 00:13:59</timestamp>
            <yymm>0001</yymm>
        </file>        
    </arXivSRC>"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
        temp_file.write(inconsistent_xml_content.encode('utf-8'))
        temp_file_path = temp_file.name

    manifest = Manifest()

    with pytest.raises(ValueError, match='Entry inconsistent'):
        manifest.import_arxiv_xml(temp_file_path)

    os.remove(temp_file_path)

@pytest.fixture
def manifest_with_data():
    """
    Fixture to provide a Manifest instance with preloaded data.
    """
    manifest = Manifest()
    manifest._manifest = {
        'metadata': {
            'manifest_filename': '20250411_arXiv_src_manifest.xml',
            'timestamp_iso': '2025-04-07T08:58:03+00:00'
        },
        'contents': [
            {'filename': 'src/arXiv_src_0001_001.tar',
             'size_bytes': 225605507,
             'timestamp_iso': '2010-12-23T05:13:59+00:00',
             'year': 2000,
             'month': 1,
             'sequence_number': 1,
             'n_submissions': 2364,
             'hash': {'MD5': '949ae880fbaf4649a485a8d9e07f370b',
                      'MD5_contents': 'cacbfede21d5dfef26f367ec99384546'}},
            {'filename': 'src/arXiv_src_0002_001.tar',
             'size_bytes': 227036528,
             'timestamp_iso': '2010-12-23T05:18:09+00:00',
             'year': 2000,
             'month': 2,
             'sequence_number': 1,
             'n_submissions': 2365,
             'hash': {'MD5': '4592ab506cf775afecf4ad560d982a00',
                      'MD5_contents': 'd90df481661ccdd7e8be883796539743'}},
            {'filename': 'src/arXiv_src_0003_001.tar',
             'size_bytes': 230986882,
             'timestamp_iso': '2010-12-23T05:22:15+00:00',
             'year': 2000,
             'month': 3,
             'sequence_number': 1,
             'n_submissions': 2600,
             'hash': {'MD5': 'b5bf5e52ae8532cdf82b606b42df16ea',
                      'MD5_contents': '3388afd7bfb2dfd9d3f3e6b353357b33'}},
            {'filename': 'src/arXiv_src_0004_001.tar',
             'size_bytes': 191559408,
             'timestamp_iso': '2010-12-23T05:26:31+00:00',
             'year': 2000,
             'month': 4,
             'sequence_number': 1,
             'n_submissions': 2076,
             'hash': {'MD5': '9bf1b55890dceec9535ef723a2aea16b',
                      'MD5_contents': '46abb309d77065fed44965cc26a4ae2e'}},
            {'filename': 'src/arXiv_src_0005_001.tar',
             'size_bytes': 255509072,
             'timestamp_iso': '2010-12-23T05:30:11+00:00',
             'year': 2000,
             'month': 5,
             'sequence_number': 1,
             'n_submissions': 2724,
             'hash': {'MD5': 'b49af416746146eca13c5a6a76bc7193',
                      'MD5_contents': 'ea665c7b62eaac91110fa344f6ba3fc4'}}
        ]
    }
    return manifest

def test_get_statistics(manifest_with_data):
    """
    Test the get_statistics method to ensure it correctly aggregates data.
    """
    manifest = manifest_with_data
    statistics = manifest.get_statistics()

    # Expected statistics
    expected_statistics = {
        (2000, 1): {'size_bytes': 225605507, 'n_submissions': 2364},
        (2000, 2): {'size_bytes': 227036528, 'n_submissions': 2365},
        (2000, 3): {'size_bytes': 230986882, 'n_submissions': 2600},
        (2000, 4): {'size_bytes': 191559408, 'n_submissions': 2076},
        (2000, 5): {'size_bytes': 255509072, 'n_submissions': 2724},
    }

    assert statistics == expected_statistics

def test_get_statistics_empty_manifest():
    """
    Test the get_statistics method with an empty manifest.
    """
    manifest = Manifest()
    manifest._manifest = {'metadata': {}, 'contents': []}
    statistics = manifest.get_statistics()

    assert statistics == {}

@pytest.fixture
def manifest_with_duplicate_keys():
    """
    Fixture to provide a Manifest instance with duplicate (year, month) keys.
    """
    manifest = Manifest()
    manifest._manifest = {
        'metadata': {
            'manifest_filename': '20250411_arXiv_src_manifest.xml',
            'timestamp_iso': '2025-04-07T08:58:03+00:00'
        },
        'contents': [
            {'filename': 'src/arXiv_src_0001_001.tar',
             'size_bytes': 225605507,
             'timestamp_iso': '2010-12-23T05:13:59+00:00',
             'year': 2025,
             'month': 1,
             'sequence_number': 1,
             'n_submissions': 2364},
            {'filename': 'src/arXiv_src_0002_001.tar',
             'size_bytes': 227036528,
             'timestamp_iso': '2010-12-23T05:18:09+00:00',
             'year': 2025,
             'month': 1,
             'sequence_number': 2,
             'n_submissions': 1000},
        ]
    }
    return manifest

def test_get_statistics_branch_coverage(manifest_with_duplicate_keys):
    """
    Test get_statistics to ensure both branches of the conditional are covered.
    """
    manifest = manifest_with_duplicate_keys
    statistics = manifest.get_statistics()

    # Expected statistics
    expected_statistics = {
        (2025, 1): {
            'size_bytes': 225605507 + 227036528,  # Sum of sizes for the same (year, month)
            'n_submissions': 2364 + 1000          # Sum of submissions for the same (year, month)
        }
    }

    assert statistics == expected_statistics

@pytest.fixture
def mock_statistics():
    """
    Fixture to provide mock statistics data for testing.
    """
    return {
        (2025, 1): {'size_bytes': 225605507, 'n_submissions': 2364},
        (2025, 2): {'size_bytes': 227036528, 'n_submissions': 2365},
        (2025, 3): {'size_bytes': 230986882, 'n_submissions': 2600},
    }

@pytest.fixture(autouse=True)
def use_agg_backend():
    """
    Automatically set the matplotlib backend to 'Agg' for all tests.
    This prevents plots from being displayed during testing.
    """
    plt.switch_backend('Agg')

def test_plot_summary_statistics(monkeypatch, mock_statistics):
    """
    Test the plot_summary_statistics method by mocking the output of get_statistics.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        # Create a Manifest instance
        manifest = Manifest()

        # Mock the get_statistics method
        def mock_get_statistics(self):
            return mock_statistics

        monkeypatch.setattr(Manifest, "get_statistics", mock_get_statistics)

        # Call the method
        manifest.plot_summary_statistics()

        # Get all active figures
        figures = [plt.figure(i) for i in plt.get_fignums()]

        # Ensure three figures were created
        assert len(figures) == 3

        # Check the titles of the plots
        expected_titles = [
            'Number of Submissions per Month',
            'Size in GB per Month',
            'Averaged Monthly Submission Size in MB'
        ]
        for fig, expected_title in zip(figures, expected_titles):
            assert fig.axes[0].get_title() == expected_title

        # Check the x-axis labels
        expected_xlabels = ['Date (Year-Month)', 'Date (Year-Month)', 'Date (Year-Month)']
        for fig, expected_xlabel in zip(figures, expected_xlabels):
            assert fig.axes[0].get_xlabel() == expected_xlabel

        # Check the y-axis labels
        expected_ylabels = ['Number of Submissions', 'Size (GB)', 'Average Submission Size (MB)']
        for fig, expected_ylabel in zip(figures, expected_ylabels):
            assert fig.axes[0].get_ylabel() == expected_ylabel

        # Clean up the figures after the test
        plt.close('all')


def test_info(mocker):
    """
    Test the info() method of the Manifest class.
    """

    # Create a mock Manifest instance with test data
    manifest = Manifest()
    manifest._manifest = {
        'metadata': {
            'manifest_timestamp_iso': '2025-04-07T08:58:03+00:00',
        },
        'contents': [
            {
                'filename': 'src/arXiv_src_0001_001.tar',
                'size_bytes': 225605507,
                'timestamp_iso': '2010-12-23T05:13:59+00:00',
                'year': 2000,
                'month': 1,
                'sequence_number': 1,
                'n_submissions': 2364,
                'hash': {
                    'MD5': '949ae880fbaf4649a485a8d9e07f370b',
                    'MD5_contents': 'cacbfede21d5dfef26f367ec99384546'
                }
            },
            {
                'filename': 'src/arXiv_src_0002_001.tar',
                'size_bytes': 227036528,
                'timestamp_iso': '2010-12-23T05:18:09+00:00',
                'year': 2000,
                'month': 2,
                'sequence_number': 1,
                'n_submissions': 2365,
                'hash': {
                    'MD5': '4592ab506cf775afecf4ad560d982a00',
                    'MD5_contents': 'd90df481661ccdd7e8be883796539743'
                }
            }
        ]
    }

    # Mock the print function to capture output
    mock_print = mocker.patch("builtins.print")

    # Call the info() method
    manifest.info()

    # Verify the printed output in the correct order
    expected_calls = [
        mocker.call("Manifest Information:"),
        mocker.call("Metadata:"),
        mocker.call("  Manifest Timestamp: 2025-04-07T08:58:03+00:00"),
        mocker.call("Number of Bulk Archives: 2"),
        mocker.call("Total Number of Submissions: 4729"),
        mocker.call("Total Size: 0.453 GB"),
        mocker.call("Average Submission Size: 0.096 MB"),
    ]

    mock_print.assert_has_calls(expected_calls, any_order=False)

def test_info_with_empty_metadata(capsys):
    """
    Test the info() method when metadata is empty.
    """
    manifest = Manifest()
    manifest._manifest = {
        'metadata': {},  # Empty metadata
        'contents': [
            {
                'filename': 'src/arXiv_src_0001_001.tar',
                'size_bytes': 225605507,
                'timestamp_iso': '2010-12-23T05:13:59+00:00',
                'year': 2000,
                'month': 1,
                'sequence_number': 1,
                'n_submissions': 2364,
                'hash': {
                    'MD5': '949ae880fbaf4649a485a8d9e07f370b',
                    'MD5_contents': 'cacbfede21d5dfef26f367ec99384546'
                }
            }
        ]
    }

    # Call the info() method
    manifest.info()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert that no output is printed for metadata
    assert captured.out.strip() == ""

def test_manifest_init_with_filename(monkeypatch):
    """
    Test Manifest.__init__ when a filename is provided.
    Ensures import_arxiv_xml is called with the correct argument.
    """
    called = {}

    def mock_import_arxiv_xml(self, file_path):
        called['file_path'] = file_path

    monkeypatch.setattr(Manifest, "import_arxiv_xml", mock_import_arxiv_xml)

    test_path = "dummy/path/arXiv_src_manifest.xml"
    manifest = Manifest(arxiv_xml_file=test_path)

    assert called['file_path'] == test_path

def test_import_arxiv_xml_invalid_format(monkeypatch, tmp_path):
    """
    Test that import_arxiv_xml raises TypeError if the file is not a valid XML format.
    """
    # Create a dummy file
    file_path = tmp_path / "not_xml.txt"
    file_path.write_text("not xml content")

    # Patch XmlHandler.is_xml_format to return False
    monkeypatch.setattr("gradhouse.arxiv.manifest.XmlHandler.is_xml_format", lambda x: False)

    manifest = Manifest()
    with pytest.raises(TypeError, match="file is not in XML format."):
        manifest.import_arxiv_xml(str(file_path))