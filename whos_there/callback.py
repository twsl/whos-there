import socket
import textwrap
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks.base import Callback
from pytorch_lightning.trainer.states import TrainerFn

from whos_there.senders.base import Sender
from whos_there.senders.debug import DebugSender


class NotificationCallback(Callback):
    def __init__(self, senders: List[Sender] = [DebugSender()]) -> None:
        """Initialize the notification callback.

        Args:
            senders: List of instances of senders.
        """
        super().__init__()
        self.senders = senders
        self._current_stage: str = None

    def _send(self, text: str) -> None:
        for sender in self.senders:
            sender.send(text)

    def setup(self, trainer: Trainer, pl_module: LightningModule, stage: Optional[str] = None) -> None:
        """Called when fit, validate, test, predict, or tune begins.
        Args:
            trainer: The current :class:`~pytorch_lightning.trainer.Trainer` instance.
            pl_module: The current :class:`~pytorch_lightning.core.lightning.LightningModule` instance.
            stage: The stage the trainer is currently in.
        """
        if trainer.global_rank == 0:
            self._current_stage = stage

    def teardown(self, trainer: Trainer, pl_module: LightningModule, stage: Optional[str] = None) -> None:
        """Called when fit, validate, test, predict, or tune ends.
        Args:
            trainer: The current :class:`~pytorch_lightning.trainer.Trainer` instance.
            pl_module: The current :class:`~pytorch_lightning.core.lightning.LightningModule` instance.
            stage: The stage the trainer is currently in.
        """
        if trainer.global_rank == 0:
            if stage == TrainerFn.FITTING:
                contents = f"🎉 Your training of {pl_module._get_name()} on {socket.gethostname()} is complete."
                self._send(contents)
            if stage == TrainerFn.TESTING:
                contents = f"🧪 Your testing of {pl_module._get_name()} on {socket.gethostname()} is complete."
                self._send(contents)

    def on_exception(self, trainer: Trainer, pl_module: LightningModule, exception: BaseException) -> None:
        """Called when any trainer execution is interrupted by an exception.
        Args:
            trainer: The current :class:`~pytorch_lightning.trainer.Trainer` instance.
            pl_module: The current :class:`~pytorch_lightning.core.lightning.LightningModule` instance.
            exception: The exception raised.
        """
        contents = f"""💥 {exception} during {self._current_stage} of {pl_module._get_name()}.
        Stage failed on {socket.gethostname()} (global rank {trainer.global_rank}).
        """
        self._send(textwrap.dedent(contents))

    def on_save_checkpoint(self, trainer: Trainer, pl_module: LightningModule, checkpoint: Dict[str, Any]) -> dict:
        """Called when saving a model checkpoint, use to persist state.
        Args:
            trainer: the current :class:`~pytorch_lightning.trainer.Trainer` instance.
            pl_module: the current :class:`~pytorch_lightning.core.lightning.LightningModule` instance.
            checkpoint: the checkpoint dictionary that will be saved.
        Returns:
            The callback state.
        """
        return {"current_stage": self._current_stage}

    def on_load_checkpoint(self, trainer: Trainer, pl_module: LightningModule, callback_state: Dict[str, Any]) -> None:
        """Called when loading a model checkpoint, use to reload state.
        Args:
            trainer: the current :class:`~pytorch_lightning.trainer.Trainer` instance.
            pl_module: the current :class:`~pytorch_lightning.core.lightning.LightningModule` instance.
            callback_state: the callback state returned by ``on_save_checkpoint``.
        Note:
            The ``on_load_checkpoint`` won't be called with an undefined state.
            If your ``on_load_checkpoint`` hook behavior doesn't rely on a state,
            you will still need to override ``on_save_checkpoint`` to return a ``dummy state``.
        """
        self._current_stage = callback_state.get("current_stage", None)
