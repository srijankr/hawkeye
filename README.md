## HawkEye: A Robust Reputation System for Community-based Counter-Misinformation

#### Authors : [Rohit Mujumdar](https://rohitmujumdar.github.io/), [Srijan Kumar](http://cs.stanford.edu/~srijan)

#### [Link to the paper]()
#### [Link to the slides]()
#### [Brief video explanation]()

### About HawkEye

Identifying misinformation is a critical task on web and social media platforms. Recent efforts have focused on leveraging the community of ordinary users to detect, counter, and curb misinformation. Twitter launched a community-driven misinformation detection service called [Birdwatch](https://blog.twitter.com/en_us/topics/product/2021/introducing-birdwatch-a-community-based-approach-to-misinformation), where users provide notes to label tweets as misleading or not, and rate other users' notes as being 'helpful' or not. However, malicious users can inject fake notes and helpfulness ratings to manipulate the system for their gains. In this work, we investigate the robustness of Birdwatch against adversaries. We show that the current Birdwatch system is vulnerable to adversarial attacks - using only a few fake accounts, an adversary can promote any random note as one of the top ranking notes. 

To overcome this vulnerability, we propose **HawkEye**, a graph-based recursive algorithm that leverages the global graph structure to quantifyall the quality metrics. Since many users will only write andrate a few notes and many tweets will only have a few notes, we introduce a Laplacian smoothing technique to overcomethis cold-start problem. We posit that HawkEye will be more robust to adversaries.

We compare the Birdwatch and HawkEye models' robustness against an attacker whose goal is to manipulate the ranking of notes. We show that our proposed HawkEye algorithm is more robust against this attack. Furthermore, we show that the HawkEye algorithm performs better than the Birdwatch system in identifying accurate and misleading tweets in both unsupervised and supervised settings. 

If you make use of this code, the HawkEye algorithm, please cite the following paper:
```
 @inproceedings{kumar2019predicting,
	title={Predicting Dynamic Embedding Trajectory in Temporal Interaction Networks},
	author={Kumar, Srijan and Zhang, Xikun and Leskovec, Jure},
	booktitle={Proceedings of the 25th ACM SIGKDD international conference on Knowledge discovery and data mining},
	year={2019},
	organization={ACM}
 }
```

### Short Video Explanation of HawkEye (External Link to YouTube)

[![HawkEye short video]()]()

### Repository Structure

All code and data is stored in `src/code/` and `src/data/` folder respectively. 

### Dataset
Links to datasets used in the paper:
- [Birdwatch Data](https://twitter.github.io/birdwatch/contributing/download-data/)


### Dataset format

The data files used for this work are stored under the `data/` folder, one CSV file each for notes and ratings. The filename is according to the nomenclature on the official [Birdwatch data download page](https://twitter.github.io/birdwatch/contributing/download-data/). The format of CSV files and the meaning of the columns can be found on the [Birdwatch data download page](https://twitter.github.io/birdwatch/contributing/download-data/). 


### Code setup and Requirements

Recent versions of Pandas, numpy, sklearn, tqdm, matplotlib, seaborn, and tweepy. `requirements.txt` can be found in the `code/` folder. You can install all the required packages using the following command:
```
    $ pip install -r requirements.txt
```

A `results/` directory needs to be created in the `code/` folder.


### Running the HawkEye scripts

To train the JODIE model using the `data/<network>.csv` dataset, use the following command. This will save a model for every epoch in the `saved_models/<network>/` directory.
```
   $ python jodie.py --network <network> --model jodie --epochs 50
```

This code can be given the following command-line arguments:
1. `--network`: this is the name of the file which has the data in the `data/` directory. The file should be named `<network>.csv`. The dataset format is explained below. This is a required argument. 
2. `--model`: this is the name of the model and the file where the model will be saved in the `saved_models/` directory. Default value: jodie.
3. `--gpu`: this is the id of the gpu where the model is run. Default value: -1 (to run on the GPU with the most free memory).
4. `--epochs`: this is the maximum number of interactions to train the model. Default value: 50.
5. `--embedding_dim`: this is the number of dimensions of the dynamic embedding. Default value: 128.
6. `--train_proportion`: this is the fraction of interactions (from the beginning) that are used for training. The next 10% are used for validation and the next 10% for testing. Default value: 0.8
7. `--state_change`: this is a boolean input indicating if the training is done with state change prediction along with interaction prediction. Default value: True.

### Evaluate the model

#### Interaction prediction

To evaluate the performance of the model for the interaction prediction task, use the following command. The command iteratively evaluates the performance for all epochs of the model and outputs the final test performance. 
```
    $ chmod +x evaluate_all_epochs.sh
    $ ./evaluate_all_epochs.sh <network> interaction
```

To evaluate the trained model's performance for predicting interactions in **only one epoch**, use the following command. This will output the performance numbers to the `results/interaction_prediction_<network>.txt` file.
```
    $ python evaluate_interaction_prediction.py --network <network> --model jodie --epoch 49
```

The file `get_final_performance_numbers.py` reads all the outputs of each epoch, stored in the `results/` folder, and finds the best validation epoch. 

#### State change prediction

To evaluate the performance of the model for the state change prediction task, use the following command. The command iteratively evaluates the performance for all epochs of the model and outputs the final test performance. 
```
    $ chmod +x evaluate_all_epochs.sh
    $ ./evaluate_all_epochs.sh <network> state
```
To evaluate the trained model's performance for predicting state change in **only one epoch**, use the following command. This will output the performance numbers to the `results/state_change_prediction_<network>.txt` file.
```
   $ python evaluate_state_change_prediction.py --network <network> --model jodie --epoch 49
```

### Run the T-Batch code

To create T-Batches of a temporal network, use the following command. This will save a file with T-Batches in the `results/tbatches_<network>.csv` file. Note that the entire input will be converted to T-Batches. To convert only training data, please input a file with only the training interactions. 

```
   $ python tbatch.py --network <network>
```

This code can be given the following command-line arguments:
1. `--network`: this is the name of the file which has the data in the `data/` directory. The file should be named `<network>.csv`. The dataset format is explained below. This is a required argument. 


### References 
*Predicting Dynamic Embedding Trajectory in Temporal Interaction Networks*. Srijan Kumar, Xikun Zhang, Jure Leskovec. ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2019. 

If you make use of this code or the HawkEye algorithm in your work, please cite the following paper:
```
 @inproceedings{kumar2019predicting,
	title={Predicting Dynamic Embedding Trajectory in Temporal Interaction Networks},
	author={Kumar, Srijan and Zhang, Xikun and Leskovec, Jure},
	booktitle={Proceedings of the 25th ACM SIGKDD international conference on Knowledge discovery and data mining},
	year={2019},
	organization={ACM}
 }
```
