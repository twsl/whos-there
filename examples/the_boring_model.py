import os
from typing import Optional

import pytorch_lightning as pl
import torch
from pytorch_lightning import LightningModule
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset

from whos_there.callback import NotificationCallback
from whos_there.senders.debug import DebugSender

tmpdir = os.getcwd()


class RandomDataset(Dataset):
    def __init__(self, size, num_samples):
        self.len = num_samples
        self.data = torch.randn(num_samples, size)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return self.len


class RandomDataModule(pl.LightningDataModule):
    def __init__(self, size: int = 32, num_samples: int = 10000, batch_size: int = 32):
        super().__init__()
        self.size = size
        self.num_sampes = num_samples
        self.batch_size = batch_size

    def setup(self, stage: Optional[str] = None):
        self.mnist_test = RandomDataset(self.size, self.num_sampes)
        self.mnist_train = RandomDataset(self.size, self.num_sampes)
        self.mnist_val = RandomDataset(self.size, self.num_sampes)

    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=self.batch_size)


class BoringModel(LightningModule):
    def __init__(self, fail=False):
        super().__init__()
        self.layer = torch.nn.Linear(32, 2)
        self.fail = fail

    def forward(self, x):
        return self.layer(x)

    def loss(self, batch, prediction):
        # An arbitrary loss to have a loss that updates the model weights during `Trainer.fit` calls
        return torch.nn.functional.mse_loss(prediction, torch.ones_like(prediction))

    def training_step(self, batch, batch_idx):
        output = self.layer(batch)
        loss = self.loss(batch, output)
        return {"loss": loss}

    def training_step_end(self, training_step_outputs):
        return training_step_outputs

    def training_epoch_end(self, outputs) -> None:
        torch.stack([x["loss"] for x in outputs]).mean()

    def validation_step(self, batch, batch_idx):
        output = self.layer(batch)
        loss = self.loss(batch, output)
        return {"x": loss}

    def validation_epoch_end(self, outputs) -> None:
        if self.fail:
            raise MemoryError("Fake Error")
        torch.stack([x["x"] for x in outputs]).mean()

    def test_step(self, batch, batch_idx):
        output = self.layer(batch)
        loss = self.loss(batch, output)
        self.log("fake_test_acc", loss)
        return {"y": loss}

    def test_epoch_end(self, outputs) -> None:
        torch.stack([x["y"] for x in outputs]).mean()

    def configure_optimizers(self):
        optimizer = torch.optim.SGD(self.layer.parameters(), lr=0.1)
        lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1)
        return [optimizer], [lr_scheduler]


dm = RandomDataModule()

model = BoringModel(fail=True)

# Initialize a trainer
trainer = pl.Trainer(
    max_epochs=1,
    progress_bar_refresh_rate=20,
    callbacks=[
        NotificationCallback(
            senders=[
                DebugSender(print=True),
            ]
        )
    ],
)

# Train the model ⚡
trainer.fit(model, datamodule=dm)

trainer.test(datamodule=dm)
