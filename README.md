# Gradhouse
![CI](https://github.com/gradhouse/gradhouse/actions/workflows/ci.yml/badge.svg)

<b>gradhouse</b> is a Python toolkit for processing, validating, and cleaning large-scale academic submission 
datasets—particularly those from sources like the arXiv S3 bulk data service.

It aims to assist researchers and developers by offering robust utilities for data integrity verification and cleaning. 
Future updates will include advanced analysis, metadata extraction, and deeper integration with scientific data repositories.

## Key Features

### Bulk Data Processing
Handle manifest files (e.g., arXiv_src_manifest.xml) and bulk data archives downloaded from arXiv’s S3 service.

### Data Integrity Checking
Automatically detect corrupted, missing, or inconsistent submission files.

### Data Cleaning
Filter out broken, incomplete, or duplicate entries to ensure high-quality datasets for downstream tasks.

### Modular and Extensible
Designed with modularity in mind to support future additions such as analytics, metadata enrichment, or 
integrations with other repositories.

## Learn More
Comprehensive documentation and usage examples are available 
on the [Gradhouse wiki](https://github.com/gradhouse/gradhouse/wiki)

## Disclaimer
Gradhouse is not affiliated with, endorsed by, or sponsored by arXiv or Cornell University.
All arXiv data and trademarks are the property of their respective owners. 

Please refer to [arXiv’s license and terms of use](https://arxiv.org/help/license) 
and their [bulk data policy](https://info.arxiv.org/help/bulk_data_s3.html) for more information.

## Example: Manifest Processing
The manifest module provides utilities to work with arXiv_src_manifest.xml from the arXiv S3 service.

Key capabilities include:
* Summary statistics of submission archives
* File-type distributions
* Submission time range analysis

For reference:
* [arXiv.org](https://www.arxiv.org)
* [arXiv S3 Bulk Data Info](https://info.arxiv.org/help/bulk_data_s3.html)

### Example Visualizations
![image](https://github.com/user-attachments/assets/cdda1543-cea0-4e17-b612-1e3778f31b64)
![image](https://github.com/user-attachments/assets/1063ab4b-992d-41bf-8a76-b2d9f2039845)
![image](https://github.com/user-attachments/assets/909d563e-0090-4e7d-985d-cc4ee4b61f16)

## Installation

```bash
pip install -r requirements.txt
```
