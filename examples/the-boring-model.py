from pathlib import Path
from typing import Any

import lightning.pytorch as pl
from lightning.pytorch import LightningModule
import torch
from torch import Tensor
from torch.nn import functional as F  # noqa: N812
from torch.optim.lr_scheduler import StepLR
from torch.optim.sgd import SGD
from torch.utils.data import DataLoader, Dataset

from whos_there.callback import NotificationCallback
from whos_there.senders.debug import DebugSender

tmpdir = Path.cwd()


class RandomDataset(Dataset):
    def __init__(self, size, num_samples: int) -> None:
        self.len = num_samples
        self.data = torch.randn(num_samples, size)

    def __getitem__(self, index: int) -> Tensor:
        return self.data[index]

    def __len__(self) -> int:
        return self.len


class RandomDataModule(pl.LightningDataModule):
    def __init__(self, size: int = 32, num_samples: int = 10000, batch_size: int = 32) -> None:
        super().__init__()
        self.size = size
        self.num_sampes = num_samples
        self.batch_size = batch_size

    def setup(self, stage: str | None = None) -> None:
        self.mnist_test = RandomDataset(self.size, self.num_sampes)
        self.mnist_train = RandomDataset(self.size, self.num_sampes)
        self.mnist_val = RandomDataset(self.size, self.num_sampes)

    def train_dataloader(self) -> DataLoader[Any]:
        return DataLoader(self.mnist_train, batch_size=self.batch_size)

    def val_dataloader(self) -> DataLoader[Any]:
        return DataLoader(self.mnist_val, batch_size=self.batch_size)

    def test_dataloader(self) -> DataLoader[Any]:
        return DataLoader(self.mnist_test, batch_size=self.batch_size)


class BoringModel(LightningModule):
    def __init__(self, fail: bool = False) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(32, 2)
        self.fail = fail

    def forward(self, x: Tensor) -> Tensor:  # pyright: ignore [reportIncompatibleMethodOverride]
        return self.layer(x)

    def loss(self, batch, prediction) -> Tensor:
        # An arbitrary loss to have a loss that updates the model weights during `Trainer.fit` calls
        return torch.nn.functional.mse_loss(prediction, torch.ones_like(prediction))

    def training_step(self, batch, batch_idx) -> dict[str, Tensor]:  # pyright: ignore [reportIncompatibleMethodOverride]
        output = self.layer(batch)
        loss = self.loss(batch, output)
        return {"loss": loss}

    def training_step_end(self, training_step_outputs) -> Any:
        return training_step_outputs

    def training_epoch_end(self, outputs) -> None:
        torch.stack([x["loss"] for x in outputs]).mean()

    def validation_step(self, batch, batch_idx) -> dict[str, Tensor]:  # pyright: ignore [reportIncompatibleMethodOverride]
        output = self.layer(batch)
        loss = self.loss(batch, output)
        return {"x": loss}

    def validation_epoch_end(self, outputs) -> None:
        if self.fail:
            raise MemoryError("Fake Error")
        torch.stack([x["x"] for x in outputs]).mean()

    def test_step(self, batch, batch_idx) -> dict[str, Tensor]:  # pyright: ignore [reportIncompatibleMethodOverride]
        output = self.layer(batch)
        loss = self.loss(batch, output)
        self.log("fake_test_acc", loss)
        return {"y": loss}

    def test_epoch_end(self, outputs) -> None:
        torch.stack([x["y"] for x in outputs]).mean()

    def configure_optimizers(self) -> tuple[list[Any], list[Any]]:
        optimizer = SGD(self.layer.parameters(), lr=0.1)
        lr_scheduler = StepLR(optimizer, step_size=1)
        return [optimizer], [lr_scheduler]


dm = RandomDataModule()

model = BoringModel(fail=True)

# Initialize a trainer
trainer = pl.Trainer(
    max_epochs=1,
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
