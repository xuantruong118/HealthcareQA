from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Trainer
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "2"


if __name__ == '__main__':
    with Run().context(RunConfig(nranks=1, experiment="test_v3")):
        colbert_config = ColBERTConfig(
            bsize=64,
            gpus=1,
            doc_maxlen=256,
            lr=2e-5,
            query_maxlen=128,
            dim=128,
            accumsteps=1,
            similarity="cosine",
        )

        trainer = Trainer(
            triples="medical/data/training_data/triple_data.json",
            queries="medical/data/f/queries.tsv",
            collection="medical/data/training_data/collection.tsv",
            config=colbert_config,
        )

        checkpoint_path = trainer.train(checkpoint="bkai-foundation-models/vietnamese-bi-encoder")

        print(f"Checkpoint saved at {checkpoint_path}...")
