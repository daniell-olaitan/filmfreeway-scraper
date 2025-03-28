import sys
import logging


class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level: int):
        super().__init__()
        self._max_level = max_level

    def filter(self, log_record: logging.LogRecord) -> bool:
        return log_record.levelno <= self._max_level


class Logger:
    def __init__(self, name: str, log_level='INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "[%(asctime)s] %(name)s: %(levelname)s - %(message)s"
        )

        # Configure logger to log info and debug messages to stdout
        self._stdout_handler = logging.StreamHandler(sys.stdout)
        self._stdout_handler.addFilter(MaxLevelFilter(logging.INFO))
        self._stdout_handler.setFormatter(formatter)

        # Configure logger to log warning and error messages to stderr
        self._stderr_handler = logging.StreamHandler(sys.stderr)
        self._stderr_handler.setLevel(logging.WARNING)
        self._stderr_handler.setFormatter(formatter)

        self.logger.addHandler(self._stderr_handler)
        self.set_log_level(log_level)

    def set_log_level(self, log_level: str):
        log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if log_level not in log_levels:
            self.logger.error(
                f"Invalid log level: {log_level}. "
                f"Choose from {', '.join(log_levels)}."
            )

        else:
            if log_level in log_levels[:2]:
                self._stdout_handler.setLevel(getattr(logging, log_level))
                self._stderr_handler.setLevel(logging.WARNING)
                if self._stdout_handler not in self.logger.handlers:
                    self.logger.addHandler(self._stdout_handler)

            elif log_level in log_levels[2:]:
                self._stderr_handler.setLevel(getattr(logging, log_level))
                if self._stdout_handler in self.logger.handlers:
                    self.logger.removeHandler(self._stdout_handler)
