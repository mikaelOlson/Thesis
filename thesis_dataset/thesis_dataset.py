# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition"""

import os
from pyexpat import features

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{tjong-kim-sang-de-meulder-2003-introduction,
    title = "Introduction to the {C}o{NLL}-2003 Shared Task: Language-Independent Named Entity Recognition",
    author = "Tjong Kim Sang, Erik F.  and
      De Meulder, Fien",
    booktitle = "Proceedings of the Seventh Conference on Natural Language Learning at {HLT}-{NAACL} 2003",
    year = "2003",
    url = "https://www.aclweb.org/anthology/W03-0419",
    pages = "142--147",
}
"""

_DESCRIPTION = """\
Test dataset of Mikael and Ludvigs thesis
"""

_URL = "N/A"
_TRAINING_FILE = "train.txt"
_DEV_FILE = "valid.txt"
_TEST_FILE = "test.txt"


class thesis_dataset(datasets.BuilderConfig):
    """BuilderConfig for thesis_dataset"""

    def __init__(self, **kwargs):
        """BuilderConfig for thesis_dataset.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(thesis_dataset, self).__init__(**kwargs)


class thesis_dataset(datasets.GeneratorBasedBuilder):
    """Thesis dataset."""

    BUILDER_CONFIGS = [
        thesis_dataset(name="thesis_dataset", version=datasets.Version("1.0.0"), description="thesis dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "B-STREET",
                                "I-STREET",
                                "E-STREET",
                                "S-STREET",
                                "S-NUMBER",
                                "S-LEVEL",
                                "B-UNIT",
                                "E-UNIT",
                                "S-UNIT",
                                "B-VEJBY",
                                "I-VEJBY",
                                "E-VEJBY",
                                "S-VEJBY",
                                "S-POSTCODE",
                                "B-POSTNAVN",
                                "I-POSTNAVN",
                                "E-POSTNAVN",
                                "S-POSTNAVN",
                                "O"                                
                            ]
                        )
                    ),
                    "context_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=["0",
                                   "1"]
                        )
                    )
                }
            ),
            supervised_keys=None,
            homepage="afry.com",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        #downloaded_file = dl_manager.download_and_extract(_URL)
        downloaded_file = '/home/ludvig/Thesis/thesis_dataset/'
        data_files = {
            "train": os.path.join(downloaded_file, _TRAINING_FILE),
            "dev": os.path.join(downloaded_file, _DEV_FILE),
            "test": os.path.join(downloaded_file, _TEST_FILE),
        }

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": data_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": data_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            #pos_tags = []
            #chunk_tags = []
            ner_tags = []
            context_tags = []
            for line in f:
                if line.startswith("-DOCSTART-") or line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            #"pos_tags": pos_tags,
                            #"chunk_tags": chunk_tags,
                            "ner_tags": ner_tags,
                            "context_tags": context_tags,
                        }
                        guid += 1
                        tokens = []
                        #pos_tags = []
                        #chunk_tags = []
                        ner_tags = []
                        context_tags = []
                else:
                    # conll2003 tokens are space separated
                    splits = line.split(" ")
                    tokens.append(splits[0])
                    #pos_tags.append(splits[1])
                    #chunk_tags.append(splits[2])
                    ner_tags.append(splits[1].rstrip())
                    context_tags.append(splits[2].rstrip())
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                #"pos_tags": pos_tags,
                #"chunk_tags": chunk_tags,
                "ner_tags": ner_tags,
                "context_tags": context_tags,
            }
