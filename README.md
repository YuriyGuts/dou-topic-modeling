# dou-topic-modeling

Analyzing the topic structure of DOU comments using Latent Dirichlet Allocation (LDA).

## Trained model

Instead of training your own LDA, you can use a saved version from the `trained` folder. You can find an 18-topic snapshot on the [Releases](https://github.com/YuriyGuts/dou-topic-modeling/releases) page.

Run the following line in the IPython Notebook:

`ldamodel = models.ldamodel.LdaModel.load(os.path.join("trained", "checkpoint-18topics.lda"))`

## Example output

    data/clean/clean-comments-10405.txt
    
                         work   51%
            living-conditions   17%
                relationships   16%
                     cashflow   6%
    
    data/clean/clean-comments-10445.txt
    
                         work   44%
                     market-2   10%
            living-conditions   9%
                      tractor   8%
                 moral-rights   7%
                     cashflow   6%
