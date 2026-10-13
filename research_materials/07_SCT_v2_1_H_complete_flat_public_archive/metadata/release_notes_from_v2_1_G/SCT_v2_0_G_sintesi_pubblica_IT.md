# SCT v2.0-G - Sintesi pubblica e addendum: cosa abbiamo fatto ora

## Cosa abbiamo fatto esattamente nel ramo v2.0

Dopo la review esterna, abbiamo corretto il target del progetto. Invece di continuare con survey e gate di fisicalizzazione completa, abbiamo costruito un test computazionale minimale e preregistrato su un solo oggetto: il transfer perturbativo T_R(k).

Sequenza operativa:

1. v1.9-R ha accettato la review esterna: v1.7-v1.9 sono stati riclassificati come requirements/survey/obstruction audit, non come risultati negativi computazionali.
2. v2.0-A ha preregistrato il primo test su a(y)=(1+y^2)^(alpha/2), con alpha primaria 0.20 e sensibilita 0.10/0.50.
3. v2.0-B ha eseguito quel protocollo senza modifiche: tutte le alpha hanno prodotto NON_GAUSSIAN_TRANSFER.
4. v2.0-C ha interpretato il risultato come negativo computazionale limitato, senza claim generale.
5. v2.0-D ha preregistrato una sola seconda famiglia indipendente, compact C2 matched power-law bounce, senza eseguirla prima.
6. v2.0-E ha eseguito la seconda famiglia: anche qui alpha primaria e sensibilita sono NON_GAUSSIAN_TRANSFER.
7. v2.0-F ha sintetizzato i due test e chiuso la route minimale T_R: niente terza famiglia scelta per recuperare gaussianita.
8. v2.0-G, questo pacchetto, trasforma il risultato in un addendum pubblico leggibile.

## Risultato scientifico limitato

I due background toy preregistrati non producono un damping gaussiano exp[-(k/k_c)^2]. Producono invece transfer bounded/plateau-like ad alto k.

Questa e una negativa computazionale vera, ma limitata: indebolisce l'ansatz gaussiano/diffusivo per le due famiglie testate, non falsifica tutti i background ciclici/bounce e non e un no-go theorem.

## Cosa non abbiamo fatto

Non abbiamo introdotto bath, noise, P_xi, Gamma_S, FDT/KMS, entropy map o claim osservativi. Non abbiamo scelto un terzo background per salvare la gaussianita. Non abbiamo fatto tuning post-hoc.
