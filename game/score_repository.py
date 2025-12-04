from __future__ import annotations
import csv
from dataclasses import dataclass, asdict
from datetime import datetime
import os
from pathlib import Path
import tempfile
import threading
from typing import List, Optional


class ScoreRepository:

    def __init__(self, path: Optional[str] = None, max_records: int = 10):
        self._path = Path(path) if path else Path("scores.csv")

        self.scores = []
        self.max_records = max_records
        self.load()

    def score_position(self, score: int) -> int:
        for index, record in enumerate(self.scores):
            if score > record["score"]:
                return index
        return len(self.scores)

    def add_score(self, player: str, score: int) -> None:
        self.scores.append({
            "player": player,
            "score": score,
        })
        self.scores.sort(key=lambda r: r["score"], reverse=True)
        if len(self.scores) > self.max_records:
            self.scores = self.scores[:self.max_records]
        self.save()

    def top_scores(self, n: int = 10) -> List[dict]:
        return self.scores[:n]

    def save(self) -> None:
        with self._path.absolute().open("w", newline='') as csvfile:
            fieldnames = ["player", "score"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for record in self.scores:
                writer.writerow({
                    "player": record["player"],
                    "score": record["score"],
                })

    def load(self) -> None:
        # default_path = f"{os.path.dirname(__file__)}/../data/default_scores.csv"
        # path = self._path if self._path.exists() else Path(default_path)
        if not self._path.exists():
            self.scores = []
            return

        with self._path.open("r", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.scores = []
            for row in reader:
                record = {
                    "player": row["player"],
                    "score": int(row["score"]),
                }
                self.scores.append(record)
            self.scores.sort(key=lambda r: r["score"], reverse=True)
