# Facial-Exercises-Detector
L'obiettivo del progetto è quello di sperimentare l'utilizzo di **modelli di estrazione facciale** per misurare la capacità di un utente di svolgere correttamente alcuni _esercizi di riabilitazione facciale_.
I requisiti fondamentali del progetto sono i seguenti:
1. Costruire un dataset di video per ciascun esercizio contenente qualche esempio positivo (svolto bene) e qualche esempio negativo (svolto male);
2. Definire un metodo di rappresentazione dei landmark facciali che sia invariante a traslazione e rotazione del volto;
3. Applicare il metodo di metric learning per apprendere una metrica in grado di distinguere gli esempi positivi da quelli negativi.

## Implementazione
L'applicazione che ho realizato è un'applicazione che può essere utilizzata per svolgere esericizi di riabilitazione facciale. Infatti, attraverso la telecamera dell'utente l'applicaione è ingrado di individuare i movimenti del volto e dopo averli analizzati sarà in grado di definire se l'esercizio è stato svolto correttamente o viceversa.

### Funzionalità
Oltre alla funzionalità principale che è quella di individuare se un esercizio di riabilitazione facciale è stato svolto correttamente, questa applicazione presenta altre funzioni che riguardano principalmente la gestione degli esercizi. Presentiamo brevemente quali sono le altre funzinoalità del programma:
1. Permette di **gestire i video** per addestrare il metric learner: è possibile realizzare e rimuovere dal dataset sia video appartenti alla classe degli _esercizi svolti correttamente_ che alla classe degli _esercizi svolti in maniera errata_;
2. Permette di **modificare la descrizione di un esercizio**;
3. Permette di **addestrare il Metric Learner** individuando quindi una metrica di distanza tra le differenti posizioni del volto;
4. Al termine dell'esecuzione di un esercizio **mostra all'utente i risulati**, comprese le distanze minime tra i video del dataset.
5. **Permette di correggere un risulato errato** generando un nuovo video nel dataset in modo tale da poter riaddestrare il metric learner correggendo l'errore.

### La GUI
Quando eseguita l'applicazione si presenta all'utente con un'interfaccia molto semplice:
1. **Selettore di categoria**: attraverso questo pulsante è possibile selezionare la categoria degli esercizi presenti nel dataset;
2. **Selettore esercizio**: attraverso questo pulsante è possibile selezionare l'esercizio che vogliamo eseguire o gestire;
3. **Impostazioni esercizio**: permette di accedere ad un menu contenente diverse funzionalità per la modifica e la gestione dell'esercizio selezionato attraverso *1* e *2*;
4. **Descrizione esercizio**: breve descrizione dell'esercizio selezionato;
5. **Video esempio**: breve video dimostrativo su come dovrebbe essere svolto l'esercizio selezionato;
6. **Esecuzione esercizio**: permette di eseguire l'esercizio selezionato.

![Image GUI](https://github.com/cerullosalvatore/Facial-Exercises-Detector/blob/master/Immagini/0.png)

#### Impostazioni esercizio

![Image GUI](https://github.com/cerullosalvatore/Facial-Exercises-Detector/blob/master/Immagini/1.png)

Attraverso il pulsante *3* dell'interfaccia principale è possibile accedere al menu delle impostazioni. Andiamo a vedere brevemente le funzioni presentate all'utente:
##### 1. Nuovo Video
Permette all'utente di realizzare un nuovo video da inserire nel dataset. 
Dopo alcuni secondi dopo la pressione di questo bottone verrà attivata la telecamera del dispositivo e verrà presentata all'utente una nuova finestra spiegata nel dettaglio nella sezione dedicata all'_Esecuzione dell'esercizio_.

##### 2. Rimuovi Video
Mostra all'utente una finestra con la quale è possibile selezionare un video dal dataset e rimuoverlo definitivamente.

![Image GUI](https://github.com/cerullosalvatore/Facial-Exercises-Detector/blob/master/Immagini/2.png)

##### 3. Addestra
Attraverso la pressione di questo pulsante verrà addestrato il metric learner. 
**Attenzione**: Dopo la pressione di questo pulsante il programma potrebbe sembrare bloccato, ma dopo qualche secondo ritornerà a funzionare normalmente.  

##### 4. Modifica descrizione
Permette all'utente di modificare la descrizione dell'esercizio.

![Image GUI](https://github.com/cerullosalvatore/Facial-Exercises-Detector/blob/master/Immagini/5.png)

#### Esecuzione Esercizio
Dopo aver premuto il pulsante, come per la funzione _Nuovo Video_ verrà attivata la videocamera e verrà aperta una nuova finestra in cui ritroviamo 4 elementi fondamentali:
1. **Video normalizzato rispetto trasalzione, rotazione e scala**;
2. **Video originale con face detection e landmark facciali**;
3. **Landmark facciali invarianti a traslazione, rotazione e scala**;
4. **Progressbar che indica lo stato di esecuzione dell'esercizio**.
![Image GUI](https://github.com/cerullosalvatore/Facial-Exercises-Detector/blob/master/Immagini/3.png)

##### Risultati
Al termine dell'esecuzione dell'esercizio verrà presentata una nuova finestra che presenterà all'utente alcune informazioni sull'esito dell'esercizio:
1. Esito dell'esercizio;
2. Match più vicino con i video presenti nel dataset di video sbagliati e distanza calcolata;
3. Match più vicino con i video presenti nel dataset di video corretti e distanza calcolata;
4. Il pulsante correggi permetterà di effettuare un'operazione di correzione.

![Image GUI](https://github.com/cerullosalvatore/Facial-Exercises-Detector/blob/master/Immagini/4.png)

##### Correzione
Attraverso il pulsante CORREGGI si accede ad una nuova finestra in cui ritroviamo 4 elementi fodamentali:
1. Il frame che indica la posizione di riposo assunta dall'utente durante l'esecuzione dell'esercizio;
2. Il frame che indica la posizione finale assunta dall'utente durante l'esecuzione dell'esercizio;
3. Pulsante che permette il salvataggio del video come _VIDEO DI COMPARAZIONE_;
4. Pulsante che permette il salvatoaggio del video come _VIDEO DI TRAINING_.
![Image GUI](https://github.com/cerullosalvatore/Facial-Exercises-Detector/blob/master/Immagini/6.png)
### Approfondimenti
Diamo uno sguardo più da vicino ad alcuni aspetti fondamentali dell'applicazione.

#### Dataset
All'interno del progetto ritroviamo una cartella chiamata **Exercises**. Al suo interno sono contenuti tutti gli esercizi di riabilitazione facciale che il programma sarà in grado di svolgere. Se si vuole realizare un nuovo esercizio basterà creare una nuova cartella contente alcune informazioni fondamentali. Vediamo brevemente il contenuto della cartella **Exercises**:

* **[Exercises](Exercises)**: directory che contiente tutti gli esercizi di riabilitazione facciale implementati dall'applicazione. In questa cartella gli esercizi sono a loro volta suddivi in categorie (es.: *1-General*);
  * **N-Name_dir**: directory che rappresenta una categoria di esercizi. Al suo interno vengono inserite le cartelle rappresentati gli esercizi (es.: _0_).
     - _Number_Exercise_: Contiente tutti i file di un esercizio. Al suo interno troviamo 4 elementi:
       * _Bad_: Directory che contiene al suo interno tutti i video considerati non corretti per l'esecizio in esame;
        - _Training: Contiene i dati di training considerati errati necessari per addestrare il modello e quindi per apprendere la metrica;
       * _Correct_: Directory che contiene al suo interno tutti i video considerati corretti per l'esercizio in esame;
               - _Training: Contiene i dati di training considerati corretti necessari per addestrare il modello e quindi per apprendere la metrica;
       * _Description.txt_: File contenente la descrizione dell'esercizio;
       * _demo.wmv_: Demo in formato .wmv .

#### Dati di addestramento
Come visto nella GUI, l'applicazione permette di **addestrare il Metric Learner in modo da definire in maniera automatica la metrica adatta al problema**. A tale scopo abbiamo bisogno di un dataset di video. Questi, come visto precedentemente, possono essere realizzati attraverso l'apposita funzione oppure possono essere inseriti attraverso la funzione correggi dopo l'esecuzione di un determinato esercizio.
Quindi, attraverso queste 2 funzioni viene popolato il dataset prsentato sopra.

In particolare, possiamo distinguere due tipologie di video:
- **Video d'addestramento**: questi sono dei video dai quali possiamo estrarre i frame per addestrare il metric learner;
- **Video di comparazione**: sono i video che verranno passati al sistema **DTW** e con i quali saremo in grado di individuare, attraverso la metrica appresa, i video pià simili.

Quando verrà richiamata la funzione *Addestra*, il programma procederà ad addestrare il metric learner attraverso due set di dati:
- **Corretti/Training**: sono i frame presenti all'interno della cartella _Correct/Training_ dell'esercizio e rappresentano la posa corretta che verrà assunta dall'utente al termine dell'esercizio;
- **Sbagliati/Training**: verranno considerati i frame presenti nella cartella _Bad/Training_ degli altri esercizi.

In pratica, l'applicazione segue i seguenti passaggi:
1. Acquisisce un video;
2. Individua due frame fondamentali: quello della **Posa Iniziale** e quello della **Posa Finale**;
3. Calcola le differenze di posizione dei lendmark di tutti i frame rispetto a quello della Posa Iniziale;
4. Permette all'utente di visualizzare i due frame e di scegliere se è un Video d'addestramento o di comparazione.

#### Correzione esito
Come visto precedentemente, al termine dell'esecuzione di un esercizio verrà visualizzata all'utente una finestra contenente il risultato dell'esercizio.
A volte però il risultato non è quello che ci aspettiamo, infatti l'esito potrebbe essere negativo anche se dovrebbe essere positivo e viceversa. Questo problema potrebbe essere dovuto alla _scarsa quantità di video utilizzata per l'addestramento_ e/o per _la comparazione_. La soluzione potrebbbe essere quindi quella di realizzare altri video, ma non è sempre facile realizzarli.

Per facilitare quindi la realizzazione del dataset ho inserito il pulsante **CORREGGI**. Andiamo a vedere brevemente come lavora.

Al termine dell'esecuzione di un esercizio verranno generati dal video acquisito 5 file temporane: _temp.mp4_, _temp.npy_, _temp_init.png, _temp_fin.png_ e _temp_fin.npy_ .
Questi potranno essere eliminati se l'esercizio ha dato l'esito sperato, cliccando il pulsante *FINE*.
Altrimenti, cliccando il pulsante *CORREGGI* verra chiesto all'utente se stiamo salvando un video di comparazione, e quindi verranno salvati solo i primi due file temporanei, oppure se stiamo salvando un video di addestramento e quindi mantenendo tutti i file temporanei.

Nel caso in cui si è scelto di salvare un video di addestramento, per poter beneficiare delle correzioni applicate bisognerà andare ad addestrare nuovamente il metric learner dalle impostazioni.

## Metric Learner e DTW
In questa sezione andrò ad prrofondire l'approccio che viene utilizzato attraverso l'utilizzo dell'**Apprendimento Metrico** e del **Dynamic Time Warping**.

### Il Problema
La prima considerazione che ho fatto è che ogni esercizio consiste in una serie di movimenti che devono essere eseguti durante un intervallo temporale predefinito.
In pratica il soggetto partirà da una _posizione di riposo_ per arrivare, dopo un determinato periodo di tempo, in una _posizione finale_ e nel caso mantenerla per un periodo di tempo predefinito. Ovviamente bisogna considerare **come** il soggetto arriva alla posizione finale.

Da questa considerazione ho dedotto che l'esecuzione dell'esercizio non può essere valutato dalle sole posizioni di riposo e finale ma deve essere considerato l'intero movimento del volto durante tutto il periodo di durata dell'esercizio. Per tale motivo ho escluso l'utilizzo di soli due frame per determinare se l'esercizio è stato svolto in maniera corretta o errata.

### La soluzione
La soluzione che ho adottato è quella di sfruttare un approccio misto: **Metric Learner + Dynamic Time Warping**.
Questo approccio si divide in due fasi, che andremo ad analizzare di seguito.

#### FASE 1: Apprendimento metrico
In questa fase l'applicazione apprenderà una metrica e definirà un modello. In pratica vogliamo che la metrica appresa dovrà essere sfruttata successivamente da un DTW. A tale scopo, poichè il nostro DTW dovrà comparare delle sequenze di landmark quello che faremo è addestrare la metrica su **Pose Errate e Pose Corrette**.

#### FASE 2: Dynamic Time Warping
Il Dynamic time warping, o DTW, è un algoritmo che permette l'allineamento tra due sequenze, e che può portare ad una misura di distanza tra le due sequenze allineate.
Quindi, grazie alla metrica appresa precedentemente quello che possiamo fare attraverso l'utilizzo del time warping è individuare la minima distanza tra i video presenti all'inteno del dataset corrispondente all'esercizio. Il risultato andrà a definire se l'esito dell'esercizio è corretto o errato.

La mia soluzione è quindi quella di analizzare tutti i frame acquisiti dalla telecamera in un determinato periodo di tempo. In pratica ogni video avrà una lunghezza di **40 frame validi**, cioè frame contenenti landmark facciali. Per cui un video avrà una forma **(40,68,2)**, dove **40** è il numero dei frame, **68** è il numero dei landmark e **2** sono le coordinate che individuano un landmark all'interno dello spazio.

**N.B.:** I landmark considerati sono **normalizzati rispetto a rotazione, traslazione e scala**. Inoltre, al fine di rendere il sistema il **più invariante possibile rispetto alla conformazione facciale dei soggetti** verranno considerate le differenze di posizione rispetto alla posa iniziale di un video. 

### Training
Gli algoritmi di metric learning sono degli algoritmi in grado di individuare una metrica in base ad alcuni dati di input che chiameremo **dati di training**.
In pratica, la **funzione di training** del modello accetta in ingresso due vettori:
* **Dati**: è un vettore contente i dati sul quale addestrare il modello;
* **Labels**: è una lista di etichette che individuano il corrisponente elemento nei _Dati_ al fine di classificarlo in una categoria.

_Esempio:_
  Dati = np.array([[2.3, 3.6], [0.2, 0.5], [6.7, 2.1]])
  Labels = np.array(['dog', 'cat', 'dog'])

  In questo esempio "cani" e "gatti" vengono rappresentati come una coppia di numeri reali.

Nel caso in esame i _Dati_ sono un insieme di distanze da **(68x2)** elementi mentre i labels indicano se il frame corrisponde ad una posa sbagliata (**-1**) o corretta (**1**).

In questo caso quindi la metrica appresa non è una distanza tra due singoli frame.
Questo mi permetterà di andare ad individuare la metrica tra una coppia di frame. 
 

