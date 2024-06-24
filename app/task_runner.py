"""
Implementarea claselor ThreadPool si TaskRunner.
"""
from queue import Queue
from threading import Thread, Event
import os
import json

class ThreadPool:
    """
    Clasa ThreadPool ce se ocupa de executia concurenta a task-urilor din coada
    pe baza unei liste de thread-uri (TaskRunners).
    """
    def __init__(self):
        """
        Initializeaza o instanta ThreadPool.
        """
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        num_of_threads = os.environ.get("TP_NUM_OF_THREADS")
        if num_of_threads:
            self.num_of_threads = int(num_of_threads)
        else:
            self.num_of_threads = os.cpu_count()
        # Coada ce retine task-urile care trebuie executate de ThreadPool.
        # Noi vom salva task-urile ca fiind tupluri de tip
        # (job_id, metoda, argumente).
        self.task_queue = Queue()
        # Eveniment ce anunta ThreadPool sa se inchida corect
        self.shutdown_event = Event()
        #  Lista de thread-uri ce executa task-urile din coada.
        self.task_runners = []
        # Dictionar in care ne mapam job_id-urile cu job_status-urile.
        self.jobs = {}
        for _ in range(self.num_of_threads):
            task_runner = TaskRunner(self.task_queue, self.shutdown_event, self.jobs)
            self.task_runners.append(task_runner)
            task_runner.start()

    def submit_task(self, task):
        """
        Adaugam un task in coada si job-ul in dictionar.
        """
        job_id = task[0]
        if job_id not in self.jobs:
            self.jobs[job_id] = {}
        self.jobs[job_id]['status'] = 'running'
        self.task_queue.put(task)

    def graceful_shutdown(self):
        """
        Setam evenimentul de shutdown.
        """
        self.jobs = {}
        self.shutdown_event.set()
        self.task_queue.join()
        for task_runner in self.task_runners:
            task_runner.join()

    def get_job_status(self, job_id):
        """
        Returneaza statusul unui job pe baza id-ului din dictionar.
        """
        return self.jobs[job_id]

class TaskRunner(Thread):
    """
    Clasa TaskRunner ce extinde implementarea clasei Thread din Python.
    """
    def __init__(self, task_queue, shutdown_event, jobs):
        """
        Initializeaza o instanta TaskRunner.
        """
        super().__init__()
        self.task_queue = task_queue
        self.shutdown_event = shutdown_event
        self.jobs = jobs

    def run(self):
        while True:
            # Repetam pana cand ajungem la graceful shutdown, cu coada goala
            if self.task_queue.empty() and self.shutdown_event.is_set():
                break
            # Adaugam timeout-ul pentru a primi un raspuns pentru graceful shutdown.
            task = None
            try:
                task = self.task_queue.get(timeout = 1)
            except:
                if self.task_queue.empty():
                    continue
            # Extragem argumentele task-ului din coada.
            job_id, job_op, args = task
            # Execute the job and save the result to disk
            result = job_op(*args)
            if not os.path.exists('results'):
                os.makedirs('results')
            result_file = f"./results/job_id_{job_id}.json"
            # Scriem rezultatul in fisier
            with open(result_file, "w", encoding="utf-8") as file:
                json.dump(result, file)
            self.jobs[job_id]['status'] = 'done'
            self.jobs[job_id]['data'] = result
            # join() din graceful_shutdown va astepta pana cand pentru fiecare
            # element din coada va avea task_done().
            self.task_queue.task_done()
