# DeepCas12a_2026 数据审计

## 范围

本轮只处理 `01_raw/DeepCas12a_2026` 和论文 PDF `/Users/linzibo/Cas12a_ML_Project_Data/01_raw/DeepCas12a_2026/paper/s12864-026-13003-3_reference.pdf`。`01_raw` 未被修改；没有训练模型；没有把 DeepCas12a 与 EasyDesign 或任何 diagnostic activity 数据合并。

## 确认事实

- DeepCas12a 属于 `editing_activity` 路径。
- 模型输入是 34 bp AsCas12a target-context sequence、34 位 methylation feature 和 34 位 DNase accessibility feature。
- 原始模型文件中的 `label` 是二分类 AsCas12a on-target activity 标签，`1` 表示 high activity，`0` 表示 low activity。
- 论文说明二分类标签来自 background-corrected indel frequency 阈值，不是 fluorescence/RFU。

## 文件清单

| file_path | file_type | file_size_bytes | possible_usage |
| --- | --- | ---: | --- |
| 01_raw/DeepCas12a_2026/.DS_Store | file | 6148 | Repository artifact. |
| 01_raw/DeepCas12a_2026/Dataset/Data_Descriptions.txt | text table or text documentation | 985 | DeepCas12a data table or manifest. |
| 01_raw/DeepCas12a_2026/Dataset/HEK_lenti_in_situ.txt | text table or text documentation | 15836 | DeepCas12a data table or manifest. |
| 01_raw/DeepCas12a_2026/Dataset/HEKplasmid_in_situ.txt | text table or text documentation | 5885 | DeepCas12a data table or manifest. |
| 01_raw/DeepCas12a_2026/Dataset/HT1-1_train.txt | text table or text documentation | 1605000 | DeepCas12a data table or manifest. |
| 01_raw/DeepCas12a_2026/Dataset/HT1-2_test.txt | text table or text documentation | 138244 | DeepCas12a data table or manifest. |
| 01_raw/DeepCas12a_2026/Dataset/HT2_test.txt | text table or text documentation | 317041 | DeepCas12a data table or manifest. |
| 01_raw/DeepCas12a_2026/Dataset/HT3_test.txt | text table or text documentation | 133857 | DeepCas12a data table or manifest. |
| 01_raw/DeepCas12a_2026/Dataset/README.md | markdown documentation | 2816 | Source documentation. |
| 01_raw/DeepCas12a_2026/Dataset/dataset_summary.tsv | tsv | 651 | DeepCas12a data table or manifest. |
| 01_raw/DeepCas12a_2026/Dataset/train_HT1-1_plus_HEK_in_situ.txt | text table or text documentation | 1626721 | DeepCas12a data table or manifest. |
| 01_raw/DeepCas12a_2026/DeepCas12a/__init__.py | python source | 65 | Repository artifact. |
| 01_raw/DeepCas12a_2026/DeepCas12a/model.py | python source | 5536 | Repository artifact. |
| 01_raw/DeepCas12a_2026/DeepCas12a/utils.py | python source | 1790 | Repository artifact. |
| 01_raw/DeepCas12a_2026/LICENSE | file | 11357 | Repository artifact. |
| 01_raw/DeepCas12a_2026/README.md | markdown documentation | 3156 | Source documentation. |
| 01_raw/DeepCas12a_2026/baselines/train_c_svr.py | python source | 4957 | Repository artifact. |
| 01_raw/DeepCas12a_2026/baselines/train_crispr_dt.py | python source | 5666 | Repository artifact. |
| 01_raw/DeepCas12a_2026/example/Readme.md | markdown documentation | 171 | Source documentation. |
| 01_raw/DeepCas12a_2026/example/example_sequences.txt | text table or text documentation | 10700 | Source documentation. |
| 01_raw/DeepCas12a_2026/images/encoding.png | image | 587471 | Repository artifact. |
| 01_raw/DeepCas12a_2026/paper/s12864-026-13003-3_reference.pdf | pdf | 1762648 | Repository artifact. |
| 01_raw/DeepCas12a_2026/requirements.txt | text table or text documentation | 88 | Source documentation. |
| 01_raw/DeepCas12a_2026/run_example.py | python source | 2290 | Repository artifact. |
| 01_raw/DeepCas12a_2026/scripts/README.md | markdown documentation | 1252 | Source documentation. |
| 01_raw/DeepCas12a_2026/scripts/optuna_search_deepcas12a.py | python source | 4648 | Repository artifact. |
| 01_raw/DeepCas12a_2026/scripts/train_deepcas12a.py | python source | 7301 | Repository artifact. |
| 01_raw/DeepCas12a_2026/splits/README.md | markdown documentation | 907 | Source documentation. |
| 01_raw/DeepCas12a_2026/splits/deepcas12a_9fold_partitions.csv | csv table | 21768462 | Split or cross-validation metadata. |
| 01_raw/DeepCas12a_2026/splits/ht1_train_test_split.csv | csv table | 2270059 | Split or cross-validation metadata. |
| 01_raw/DeepCas12a_2026/trained_model/fold1.pth | trained PyTorch checkpoint | 23881156 | Pretrained model checkpoint; not a raw label source. |
| 01_raw/DeepCas12a_2026/trained_model/fold2.pth | trained PyTorch checkpoint | 23881289 | Pretrained model checkpoint; not a raw label source. |
| 01_raw/DeepCas12a_2026/trained_model/fold3.pth | trained PyTorch checkpoint | 23881156 | Pretrained model checkpoint; not a raw label source. |
| 01_raw/DeepCas12a_2026/trained_model/fold4.pth | trained PyTorch checkpoint | 23881156 | Pretrained model checkpoint; not a raw label source. |
| 01_raw/DeepCas12a_2026/trained_model/fold5.pth | trained PyTorch checkpoint | 23881156 | Pretrained model checkpoint; not a raw label source. |
| 01_raw/DeepCas12a_2026/trained_model/fold6.pth | trained PyTorch checkpoint | 23881156 | Pretrained model checkpoint; not a raw label source. |
| 01_raw/DeepCas12a_2026/trained_model/fold7.pth | trained PyTorch checkpoint | 23881156 | Pretrained model checkpoint; not a raw label source. |
| 01_raw/DeepCas12a_2026/trained_model/fold8.pth | trained PyTorch checkpoint | 23881156 | Pretrained model checkpoint; not a raw label source. |
| 01_raw/DeepCas12a_2026/trained_model/fold9.pth | trained PyTorch checkpoint | 23881156 | Pretrained model checkpoint; not a raw label source. |

## 表格判断

| file_name | n_rows | label_counts | recommended_action |
| --- | ---: | --- | --- |
| HT1-1_train.txt | 15000 | {"0": 8656, "1": 6344} | extract_to_csv |
| HT1-2_test.txt | 1292 | {"0": 748, "1": 544} | extract_to_csv |
| HT2_test.txt | 2963 | {"0": 1880, "1": 1083} | extract_to_csv |
| HT3_test.txt | 1251 | {"0": 1002, "1": 249} | extract_to_csv |
| HEKplasmid_in_situ.txt | 55 | {"0": 46, "1": 9} | extract_to_csv |
| HEK_lenti_in_situ.txt | 148 | {"0": 107, "1": 41} | extract_to_csv |
| train_HT1-1_plus_HEK_in_situ.txt | 15203 | {"0": 8809, "1": 6394} | extract_to_csv |

## PDF 证据

| page | evidence_id | snippet |
| ---: | --- | --- |
| 1 | title | BMC Genomics https://doi.org/10.1186/s12864-026-13003-3 Article in Press DeepCas12a: a hybrid deep learning framework for accurate AsCas12a efficiency prediction from sequence and epigenetic information Received: 30 January 2026 Yiming Shi, Junkai Yin, Shurui Ning, Jinling Yuan, Degang Yang & Guohui Chuai Accepted: 27 May 2026 We are providing an unedited version of this manuscript to give early access to its S findings. Before final publication, the manuscript will undergo further editing. Please Cite this article as: Shi Y., Yin J., S note there may be errors present which affect the  |
| 2 | title | ACCAERPTTICEDLE M IANN PURSECSRSIPT DeepCas12a: A hybrid deep learning framework for accurate AsCas12a efficiency prediction from sequence and epigenetic information Yiming Shi1,2*, Junkai Yin1,2*, Shurui Ning1,2*, Jinling Yuan1,2*, Degang Yang1 #, Guohui Chuai 1,2 # *These authors contributed equally to this work. #Corresponding authors 1 Department of Infectious Dermatosis, Center of Infectious Skin Diseases, Shanghai Skin Disease Hospital, Bioinformatics Department, School of Life Sciences and Technology, Tongji University, Shanghai 200092, China  |
| 4 | data_preparation | ntegrating N Convolutional and Vision TransfIormer Modules for Predicting CRISPR- AsCas12a on-target cleavagEe efficiency. L C I 2. Material and Methods T R A 2.1 Data Preparation CRISPR-AsCas12a on-target cleavage efficiency data were retrieved from Kim et al. (2018)[11]. This dataset (HT1) quantifies AsCas12a editing efficiency across target sites in HEK293T cells via high-throughput sequencing. The complete dataset (N=16,292) was randomly partitioned into a training set (n=15,000) and an independent test set (n=1,292). In addition to HT1, two additional AsCas12a activity datasets from Kim et al. (2018) were incorporated as supplementary training data: the HEK-lenti dataset (n = 148) and t |
| 5 | binary_label | hese supplementary datasets were included in the training data for DeepCas12a and, when retraining was required, for the baseline models under the same data-partitioning strategy. For binary classification, labels were assigned based on background- corrected indel frequencies: samples exhibiting a >2-fold change over controls and an absolute indel frequency >50% were labeled positive (1); all others were labeled negative (0). This threshold aligns with high-efficacy classification standards used in prior CRISPR studies.[14] To model epigenetic effects, DNA methylation (RRBS) and chromatin accessibility (DNase-seq) data for HEK293T cells were obtained from the ENCODE project[15]. Target seque |
| 5 | input_sequence | r CRISPR studies.[14] To model epigenetic effects, DNA methylation (RRBS) and chromatin accessibility (DNase-seq) data for HEK293T cells were obtained from the ENCODE project[15]. Target sequences (34 bp) were aligned to the human reference genome (hg38) using Bowtie 2[16]. We identified target sites overlapping with RRBS-covered regions or DNase narrow peaks to generate binary epigenetic feature maps (presence=1, absence=0)[14]. Input sequences were encoded as 6-channel tensors. Channels 1–4 represented S nucleotide identity via one-hot encoding (A, C, G, ST). Channel 5 encoded DNA methylation status, and Channel 6 encoded chrEomatin accessibility, as shown R in Figure 2. P N This represent |
| 5 | input_tensor |  using Bowtie 2[16]. We identified target sites overlapping with RRBS-covered regions or DNase narrow peaks to generate binary epigenetic feature maps (presence=1, absence=0)[14]. Input sequences were encoded as 6-channel tensors. Channels 1–4 represented S nucleotide identity via one-hot encoding (A, C, G, ST). Channel 5 encoded DNA methylation status, and Channel 6 encoded chrEomatin accessibility, as shown R in Figure 2. P N This representation captures both local sequence context and the epigenetic I landscape, reflecting the various f actors which influence AsCas12a activity. E L C I T R A Figure 2. One-hot Encoding and Epigenetic Channel Representation of the 6×34 Input Tensor Structur |
| 16 | data_availability | ics. Declarations Ethics approval and consent to participate Not applicable. Consent for publication Not applicable. Availability of data and materials S Data availability S E R P The datasets analyzed during the current study are available on the Github N at https://github.com/bm2-lab-submission/DeepCas12a. I E Code availability L C I T The model and model usage are available on the Github at R https://github.com/bm2-lab-submission/DeepCas12a. A Competing interests The authors declare no competing interests. Funding This study was supported by National Natural Science Foundation of China [62002265]; Tongji University "Medicine + X" Cross Research Program [2025080107]. Authors' contributions |

## 最值得清洗的表

- `Dataset/train_HT1-1_plus_HEK_in_situ.txt`：推荐训练集。
- `Dataset/HT1-2_test.txt`：HT1 holdout test。
- `Dataset/HT2_test.txt` 和 `Dataset/HT3_test.txt`：独立测试集。
- `splits/deepcas12a_9fold_partitions.csv`：训练集 9-fold validation 划分。

## 不确定问题

- 当前仓库只提供 model-ready binary labels；若后续需要连续 indel frequency，需要追溯 Kim et al. 原始数值。
- 34 bp target-context sequence 可推断 PAM/protospacer，但没有独立 crRNA sequence；若要生成 crRNA 序列需要确认方向和互补规则。
- HEK in situ 数据的 A/N epigenetic feature calls 需要在后续模型解释中与 HT standardized features 分开讨论。
