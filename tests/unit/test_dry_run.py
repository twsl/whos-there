from pathlib import Path
import types
from typing import Any

import lightning.pytorch as pl
import torch
from torch import Tensor
from torch.utils.data import DataLoader, Dataset

from whos_there.callback import NotificationCallback
from whos_there.senders.base import Sender


class RandomDataset(Dataset):
    def __init__(self, size: int, length: int) -> None:
        self.len = length
        self.data = torch.randn(length, size)

    def __getitem__(self, index: int) -> Tensor:
        return self.data[index]

    def __len__(self) -> int:
        return self.len


class BoringModel(pl.LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(16, 2)

    def forward(self, x: Tensor, *args: Any, **kwargs: Any) -> Tensor:  # pyright: ignore [reportIncompatibleMethodOverride]
        return self.layer(x)

    def training_step(self, batch: Any, batch_idx: int) -> dict[str, Any]:  # pyright: ignore [reportIncompatibleMethodOverride]
        loss = self(batch).sum()
        self.log("train_loss", loss)
        return {"loss": loss}

    def validation_step(self, batch: Any, batch_idx: int) -> None:  # pyright: ignore [reportIncompatibleMethodOverride]
        loss = self(batch).sum()
        self.log("valid_loss", loss)

    def test_step(self, batch: Any, batch_idx: int) -> None:  # pyright: ignore [reportIncompatibleMethodOverride]
        loss = self(batch).sum()
        self.log("test_loss", loss)

    def configure_optimizers(self) -> Any:
        return torch.optim.SGD(self.layer.parameters(), lr=0.1)  # type: ignore [reportPrivateImportUsage]


class TestSender(Sender):
    def __init__(self) -> None:
        """Initialize the Test sender."""
        super().__init__()
        self.logs = []

    def send(self, text: str) -> None:
        self.logs.append(text)


def get_trainer(sender: Sender) -> pl.Trainer:
    return pl.Trainer(
        accelerator="cpu",
        default_root_dir=Path.cwd(),
        limit_train_batches=1,
        limit_val_batches=1,
        limit_test_batches=1,
        num_sanity_val_steps=0,
        max_epochs=1,
        enable_model_summary=False,
        callbacks=[NotificationCallback([sender])],
    )


def test_dry_run() -> None:
    train_data = DataLoader(RandomDataset(16, 8), batch_size=2)
    val_data = DataLoader(RandomDataset(16, 8), batch_size=2)
    test_data = DataLoader(RandomDataset(16, 8), batch_size=2)

    sender = TestSender()
    model = BoringModel()
    trainer = get_trainer(sender)
    trainer.fit(model, train_dataloaders=train_data, val_dataloaders=val_data)
    trainer.test(model, dataloaders=test_data)

    assert "Fit" in sender.logs[0]
    assert "Test" in sender.logs[1]


class TrainingError(Exception):
    pass


def test_dry_run_failed() -> None:
    train_data = DataLoader(RandomDataset(16, 8), batch_size=2)
    val_data = DataLoader(RandomDataset(16, 8), batch_size=2)

    def training_step_fail(self, batch, batch_idx) -> None:
        raise TrainingError("failed")

    sender = TestSender()
    model = BoringModel()

    model.training_step = types.MethodType(training_step_fail, model)

    trainer = get_trainer(sender)
    try:
        trainer.fit(model, train_dataloaders=train_data, val_dataloaders=val_data)
    except Exception as e:
        assert e.args[0] == "failed"

    assert "Fit" in sender.logs[0]
    assert "Failed" in sender.logs[0]
