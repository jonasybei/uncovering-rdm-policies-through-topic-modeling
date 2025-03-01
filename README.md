# Uncovering RDM Policies through Topic Modeling

Big data and data-driven methods in research have increased interest in guidelines and processes for handling research data, including data acquisition, data sharing, data retention, and many more topics, which are known as Research Data Management (RDM). While RDM is governed by research institutes through RDM policies, the policy documents developed or adopted by organizations may vary in focus and structure. This project applies topic modelling to identify commonalities found in RDM policies, helping policymakers create and improve existing policies, and helping researchers learn about key RDM concepts to promote better RDM practices. Further, this work introduces a topic-based retrieval-augmented generation for accessing and summarizing implementations of common clauses in a conversational format. Additionally, a Knowledge Graph is created, connecting policies and topics to facilitate explainable comparison.

In this project, three goals are defined:

- Find common clauses from RDM Policies via topic modeling
- Create a retrieval-augmented generation for verifyable summaries of the common clauses
- Represent the policy-topic relationships in a knowledge graph

This project uses a four-step methodology for extracting and representing topics from RDM policies:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/jonasybei/uncovering-rdm-policies-through-topic-modeling/refs/heads/new/docs/img/methodology_dark_mode.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/jonasybei/uncovering-rdm-policies-through-topic-modeling/refs/heads/new/docs/img/methodology.png">
  <img alt="The methodology of the project." src="https://raw.githubusercontent.com/jonasybei/uncovering-rdm-policies-through-topic-modeling/refs/heads/new/docs/img/methodology.png">
</picture>

# Getting Started

To get started, navigate into the folder in the terminal and type:

```
conda env create -f env.yml
```

This creates a conda environment titled rdm-analysis allowing you to run the code. The repository is structured as following:

├── **data**: data relevant to this project  
├── **docs**: documentation files (such as the methodology image you see above)  
├── **notebooks**: jupyter notebooks containing most of the code used in this project  
└── **src**: helper functions  


Each directory features its own README.md file, which explains the directory structure more in-depth.