# Velocidapter: Task-oriented Dialogue Comprehension Modeling | Pairing Synthetic Text Generation with Domain Adaptation
[![Conference](https://img.shields.io/badge/SIGDIAL-2021-blueviolet)](https://github.com/cuthalionn/cuthalionn.github.io/blob/master/files/Velocidapter_SIGDIAL_CR.pdf)

This is the code and data (MRCWOZ) for the SIGDIAL paper [Velocidapter: Task-oriented Dialogue Comprehension Modeling | Pairing Synthetic Text Generation with Domain Adaptation](https://github.com/cuthalionn/cuthalionn.github.io/blob/master/files/Velocidapter_SIGDIAL_CR.pdf)

Feel free to open issues related to the project and email me regarding research related discussions.

This project has started with the research question: "Do current MRC models comprehend our everyday task-oriented dialogues". Motivated by this question we create a new task-oriented dialogue comprehension benchmark: MRCWOZ.

MRCWOZ is created using the same dialogues from a large DST dataset: MultiWOZ 2.1. We annotate each slot in MultiWOZ with a few questions and eventually match each dialogue with a set of questions regarding the slot values they incorporote. Our dataset follows the same format that SQuAD 2.0?? introduced.

We also share the code for Velocidapter which is an augmentation framework that exploits little human interference to enlargen datasets in emerging TOD domains (with 5-10 development dialogues) by several orders of magnitudes. It intermingles chunks extracted by human annotators using predefined rules and creates new dialogues from scratch. Please refer to the paper for more details.

# Usage
```bash
python dialogueGenerator.py -nt -ur -if="<insert input_folder_path>" -of="<insert output_folder_name>" -maxD N
```
Like:
```
python dialogueGenerator.py -nt -ur -if="Data/Taxi" -of="Results/out" -maxD 50 
```
* -nt: If passed as an argument the framework creates new dialogue templates. (If not included the framework will use generated templates from the previous run).
* -ur: If passed as an argument the framework considers the user defined rules while generating the dialogues.
* -if: Path to the input file
* -of: Path to the output file
* -maxD: Max number of dialogues to be generated
* -maxT: Max number of templates to be generated
* -vs : Proportion for validation split

After the run you will get three files in your output folder: 
1. out.xml: The whole unsepareted augmented set in xml format. 
2. outtrain.json: The training split of augmented set in SQUAD 2.0 format.
3. outval.json: The validation split of augmented set in SQUAD 2.0 format.

## Using for a new domain

In order to use Velocidapter with a new domain you need to provide 4 files within the input folder: 
1. modulaterTemplates.xml: File that includes extracted dialogue chunks from the development set dialogues. 
2. questions.xml: File that includes set of questions for each slot.
3. slots.json: File that includes set of values for each slot.
4. rules.json [Optional]: File that defines certain sequential rules for adding slots to dialogues.

Then you can follow the previous usage steps to create a new task-oriented dialogue comprehension dataset.

For a more detailed explanation of how to create modular Templates please follow the x file we used for user studies in our paper.
# Citation
If you use Velocidapter in your paper, please cite as below:
```
@InProceedings{taha-aksu-2021-velocidapter,
title = "Velocidapter: Task-oriented Dialogue Comprehension Modeling | Pairing Synthetic Text Generation with Domain Adaptation",
author = "Aksu, Taha and Liu, Zhengyuan and Kan, Min-Yen and Chen, Nancy F.",
booktitle = "Proceedings of the 21th Annual Meeting of the Special Interest Group in Discourse and Dialogue",
month = "July",
year = "2021",
address = "Singapore",
publisher = "Association for Computational Linguistics"
}
```