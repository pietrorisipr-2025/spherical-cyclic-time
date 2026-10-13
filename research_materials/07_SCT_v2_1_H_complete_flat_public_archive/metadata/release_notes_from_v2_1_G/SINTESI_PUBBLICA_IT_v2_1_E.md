# Sintesi pubblica italiana - SCT v2.1-E

Questo addendum aggiorna la posizione del progetto sul kernel di trasferimento `T_R(k)`. Dopo la review esterna e dopo due test computazionali preregistrati, il kernel gaussiano/diffusivo `exp[-(k/k_c)^2]` non viene piu' trattato come default della route closed-background.

La nuova formulazione conservativa e': `T_R(k)` e' un operatore di trasferimento dipendente dal modello. Il gaussiano resta ammesso solo come limite toy open-system/diffusivo, se il meccanismo dissipativo o di coarse-graining viene specificato indipendentemente.

I due background toy preregistrati della v2.0 hanno prodotto transfer non gaussiani con plateau high-k. La v2.1-A ha spiegato il meccanismo come trasparenza high-k del sistema chiuso piu' amplificazione low-k usata come riferimento di normalizzazione. La v2.1-B ha preregistrato un kernel plateau-like solo come ramo toy esplicativo, non come kernel fisico universale.

Non viene fatto alcun claim fisico, cosmologico o osservativo. Non viene dichiarato nessun no-go theorem generale per tutti i bounce o modelli ciclici. La route di matching piu' fisico resta bloccata finche' non esistono background/action, variabile gauge-invariant, `z(eta)` e condizioni di matching specificate indipendentemente.
