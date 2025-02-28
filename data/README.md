This folder contains all data used during this project.

**data_sources.csv** shows which univerities were considered and which link houses the RDM policy.  
**pdf/** contains the RDM policies from the universities in the .pdf format.  
**markdown/** features the markdown files after extraction via the MinerU project. The extraction was done online (https://huggingface.co/spaces/opendatalab/MinerU) using MinerU Version 2025/01/22 1.1.0. For local extraction, see the MinerU documentation (https://mineru.readthedocs.io/en/latest/index.html).  
**output/** contains the extracted documents in a single table in file **documents.csv**, as well as the cleaned documents in table **documents_cleaned.csv**. Additionally, this directory houses the chunked documents, which are named after their respective chunking method. 