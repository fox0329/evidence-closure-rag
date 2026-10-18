# Third-Party Notices

This repository is distributed under the MIT License. The exported research artifact includes an adapted subset of the PrivacyQA benchmark.

## PrivacyQA

- Source: <https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP>
- Paper: A. Ravichander, A. W. Black, S. Wilson, T. Norton, and N. Sadeh. "Question Answering for Privacy Policies: Combining Computational and Legal Perspectives." EMNLP-IJCNLP 2019, pp. 4949-4959. arXiv:1911.00841.
- License: MIT, <https://github.com/AbhilashaRavichander/PrivacyQA_EMNLP/blob/master/LICENSE>
- Modification: The artifact uses the frozen `privacyqa-public-pilot-v1.4-clean-heldout` adapter with 500-character chunks and balanced answerability quotas. The dataset annotations and policy text are not relabeled.

The adapter implementation referenced by the frozen data manifest is from LegalBench-RAG and is used only as an external implementation reference; its source code is not redistributed in this artifact.
