from __future__ import annotations  # remove when dropping 3.8 support

import socket
import textwrap
from typing import Any

import lightning.pytorch as pl
from lightning.pytorch.callbacks import Callback
from lightning.pytorch.trainer.states import TrainerFn

from whos_there.senders.base import Sender
from whos_there.senders.debug import DebugSender
from whos_there.utils.logging import get_logger

logger = get_logger(__name__)


class NotificationCallback(Callback):
    """Notification callback."""

    def __init__(self, senders: list[Sender] | None = None) -> None:
        """Initialize the notification callback.

        Args:
            senders: List of instances of senders.
        """
        super().__init__()
        self.senders: list[Sender] = senders if senders else [DebugSender()]
        self._current_stage: str = ""

    def _send(self, text: str) -> None:
        for sender in self.senders:
            try:
                sender.send(text)
            except Exception:
                logger.exception(f"An exception using {sender} occurred.")

    def setup(self, trainer: pl.Trainer, pl_module: pl.LightningModule, stage: str) -> None:
        """Called when fit, validate, test, predict, or tune begins.

        Args:
            trainer: The current :class:`~lightning.pytorch.trainer.Trainer` instance.
            pl_module: The current :class:`~lightning.pytorch.core.lightning.LightningModule` instance.
            stage: The stage the trainer is currently in.
        """
        if trainer.global_rank == 0:
            self._current_stage = stage

    def teardown(self, trainer: pl.Trainer, pl_module: pl.LightningModule, stage: str) -> None:
        """Called when fit, validate, test, predict, or tune ends.

        Args:
            trainer: The current :class:`~lightning.pytorch.trainer.Trainer` instance.
            pl_module: The current :class:`~lightning.pytorch.core.lightning.LightningModule` instance.
            stage: The stage the trainer is currently in.
        """
        if trainer.global_rank == 0:
            icon = None
            if stage == "tune":
                icon = "🧪"
            if stage == TrainerFn.FITTING:
                icon = "✨"
            if stage == TrainerFn.TESTING:
                icon = "🎉"
            if icon is not None:
                name = pl_module._get_name()
                contents = f"{icon} {stage.capitalize()} stage of {name} on {socket.gethostname()} is complete."
                self._send(contents)

    def on_exception(self, trainer: pl.Trainer, pl_module: pl.LightningModule, exception: BaseException) -> None:
        """Called when any trainer execution is interrupted by an exception.

        Args:
            trainer: The current :class:`~lightning.pytorch.trainer.Trainer` instance.
            pl_module: The current :class:`~lightning.pytorch.core.lightning.LightningModule` instance.
            exception: The exception raised.
        """
        name = pl_module._get_name()
        contents = f"""💥 Failed during {self._current_stage.capitalize()} stage of {name} on {socket.gethostname()}.
        Exception (global rank {trainer.global_rank}): '{exception}'
        """
        self._send(textwrap.dedent(contents))

    def state_dict(self) -> dict[str, Any]:
        """Called when saving a checkpoint, implement to generate callback's ``state_dict``.

        Returns:
            A dictionary containing callback state.
        """
        return {"current_stage": self._current_stage}

    def on_load_checkpoint(
        self, trainer: pl.Trainer, pl_module: pl.LightningModule, checkpoint: dict[str, Any]
    ) -> None:
        r"""Called when loading a model checkpoint, use to reload state.

        Args:
            trainer: the current :class:`~lightning.pytorch.trainer.Trainer` instance.
            pl_module: the current :class:`~lightning.pytorch.core.module.LightningModule` instance.
            checkpoint: the full checkpoint dictionary that got loaded by the Trainer.
        """
        stage = checkpoint.get("current_stage")
        self._current_stage = stage if stage else ""
