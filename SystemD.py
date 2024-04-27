#!/usr/bin/python3

import os
import signal
import psutil
import time
import logging
import multiprocessing


def worker():
    while True:
        logging.info("Process count: {}".format(len(psutil.pids())))
        time.sleep(5)


def signal_handler(signum, frame):
    logging.info("Received signal {}".format(signum))
    exit(0)


if __name__ == "__main__":
    # отделение от терминала
    pid = os.fork()
    if pid != 0:
        exit(0)

    # создание новой сессии
    os.setsid()

    # запуск в фоновом режиме
    pid = os.fork()
    if pid != 0:
        exit(0)

    # установка обработчика сигналов
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # настройка журнала
    logging.basicConfig(filename='daemon.log', level=logging.INFO)

    # создание дочернего процесса
    process = multiprocessing.Process(target=worker)
    process.start()

    # основной цикл демона
    while True:
        time.sleep(1)
