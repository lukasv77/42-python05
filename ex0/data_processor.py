#!/usr/bin/env python3

from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[tuple[int, str]] = []
        self.rank = 0

    def output(self) -> tuple[int, str]:
        if not self.items:
            raise IndexError("No index 0")
        return self.items.pop(0)

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass


class NumericProcessor(DataProcessor):
    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, (int, float)):
            self.items.append((self.rank, str(data)))
            self.rank += 1
        else:
            for chunk in data:
                self.items.append((self.rank, str(chunk)))
                self.rank += 1

    @staticmethod
    def is_number(data: Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        else:
            return False

    def validate(self, data: Any) -> bool:
        if (
            isinstance(data, list)
            and all(self.is_number(chunk) for chunk in data)
        ):
            return True
        elif self.is_number(data):
            return True
        else:
            return False


class TextProcessor(DataProcessor):
    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, str):
            self.items.append((self.rank, data))
            self.rank += 1
        else:
            for chunk in data:
                self.items.append((self.rank, chunk))
                self.rank += 1

    def validate(self, data: Any) -> bool:
        if isinstance(data, list) and all(isinstance(x, str)
                                          for x in data):
            return True
        elif isinstance(data, str):
            return True
        else:
            return False


class LogProcessor(DataProcessor):
    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, dict):
            self.items.append((self.rank,
                               f"{data['log_level']}: {data['log_message']}"))
            self.rank += 1
        else:
            for chunk in data:
                self.items.append((self.rank, f"{chunk['log_level']}: "
                                              f"{chunk['log_message']}"))
                self.rank += 1

    @staticmethod
    def is_proper_dict(data: Any) -> bool:
        if (
            isinstance(data, dict)
            and all(isinstance(key, str)
                    and isinstance(val, str) for key, val in data.items())
            and 'log_level' in data
            and 'log_message' in data
        ):
            return True
        else:
            return False

    def validate(self, data: Any) -> bool:
        if isinstance(data, list) and all(self.is_proper_dict(chunk)
                                          for chunk in data):
            return True
        elif self.is_proper_dict(data):
            return True
        else:
            return False


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    numeric = NumericProcessor()
    print(f" Trying to validate input '42': {numeric.validate(42)}")
    print(f" Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")
    except Exception as error:
        print(f" Got exception: {error}")
    numeric_data: list[int | float] = [1, 2, 3, 4, 5]
    print(f" Processing data: {numeric_data}")
    numeric.ingest(numeric_data)
    print(" Extracting 3 values...")
    for _ in range(3):
        try:
            rank, value = numeric.output()
            print(f" Numeric value {rank}: {value}")
        except IndexError as error:
            print(f" List is empty: {error}")

    print("\nTesting Text Processor...")
    text = TextProcessor()
    print(f" Trying to validate input '42': {text.validate(42)}")
    print(f" Trying to validate input 'Hello': {text.validate('Hello')}")
    text_data = ["Hello", "Nexus", "World"]
    print(f" Processing data: {text_data}")
    text.ingest(text_data)
    print(" Extracting 1 value...")
    rank, value = text.output()
    print(f" Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f" Trying to validate input 'Hello': {log.validate('Hello')}")
    log_data = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f" Trying to validate the log list: {log.validate(log_data)}")
    print(f" Processing data: {log_data}")
    log.ingest(log_data)
    print(" Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f" Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
