Nume: Vlad Andra
Grupa: 331CC

# TEMA 1 

Organizare
-
1. Explicație pentru soluția aleasă:
* Am început implementarea temei prin parcurgerea laboratoarelor pentru a înțelege mai bine de ce folosim un ThreadPool. Eficiența acestuia constă în faptul că thread-urile din listă (TaskRunners) sunt create înaintea alocării task-ului, ceea ce este foarte util în aplicația noastră de request-uri la un server care trebuie să funcționeze rapid.
* Așadar, am început tema prin implementarea fișierului task_runners.py, unde am salvat în ThreadPool coada de task-uri (unde task-urile așteaptă prelucrarea de către thread-urile din lista de TaskRunners) și lista de TaskRunners. Pentru prelucrarea informațiilor, am făcut decizia nepotrivită de a le implementa în data_ingestor.py, fiind mai dificil să pasez informațiile mai departe către thread-uri. Task-urile mele sunt reprezentate sub formă de tuplu de tipul (job_id, numele funcției, argumentele funcției). 
* În routes.py, pattern-ul unui request este următorul: se primesc datele, se selectează întrebarea/statul necesare, se adaugă în coada din ThreadPool task-ul curent și se incrementează counter-ul global, după care se va returna răspuns de tip JSON. 
* După implementarea acestor funcții, pentru o gestioanre corectă a informațiilor, am citit/scris în fișier informațiile aferente unui job, pentru a nu accesa dicționarul intern pentru fiecare request.
* Pentru implementarea unittest-urilor, am creat o copie a fișierului data_ingestor.py unde procesez csv-ul și execut calculele necesare, pentru a nu crea mai multe import-uri. Am făcut un csv mock în care am adăugat câteva intrări verificate manual prin calcul, după care le-am verificat în unittest cu ajutorul funcțiilor de assert.
* Testarea, pe lângă cea realizată de checker, am făcut-o în două moduri. Prima oară, am testat că implementarea e corectă folosind un script care îmi rula în background mai multe teste în paralel ('make run_tests &' intr-un for). Apoi, pentru fiecare request neverificat de checker, am folosit extensia RapidAPI de la VSC pentru a testa request-urile.

Implementare
-
Pentru implementarea corectă a codului, am avut în vedere următoarele detalii:
* Am avut probleme inițial în cazul de graceful shutdown, deoarece request-ul nu ajungea niciodată să fie completat, deoarece thread-ul meu rămânea blocat pe self.task_queue.get()atunci când event-ul meu de shutdown era setat. Pentru rezolvarea problemei, am adăugat un timeout și am folosit funcția task_done corespunzător. Deoarece într-un scenariu obișnuit după graceful shutdown nu ar trebui să mai am nimic în coadă, am adăugat acest error handling în cod. 
* Pentru lucrul corect cu ThreadPool, fișiere csv și coada sincronizată în Python, am folosit resursele de la final, unele prezente și în scheletul de laborator.
* Inițial, folosisem în cod un Lock atât pentru job_counter-ul webserverului, cât și pentru dicționarul folosit pentru job-uri, deoarece le-am considerat pe ambele resurse comune pentru thread-uri. Cu toate acestea, am salvat un singur Lock pentru job counter doar, deoarece intrările din dicționarul meu de jobs au drept cheie job_id-ul. Dacă operația de incrementare a job-id-ul este corect efectuată cu Lock, atunci fiecare thread va avea o intrare unică în dicționar și nu mai este nevoie de Lock și pe această resursă.


Resurse utilizate
* [1] : https://docs.python.org/3/library/queue.html#Queue.Queue.task_done
* [2] : https://dev.to/epam_india_python/maximizing-python-concurrency-a-comparison-of-thread-pools-and-threads-5dl6 
* [3] : https://docs.python.org/3/library/csv.html

