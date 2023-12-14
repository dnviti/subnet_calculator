Certo, posso aiutarti a creare un `README.md` per il tuo script di calcolo delle sottoreti IP. Ecco un esempio di come potrebbe essere strutturato, completo di spiegazioni teoriche su FLSM (Fixed Length Subnet Mask) e VLSM (Variable Length Subnet Mask), e degli esempi di calcoli per entrambi gli approcci:


# Calcolo Sottoreti IP

Questo script Python fornisce una soluzione per il calcolo delle sottoreti IP utilizzando sia l'approccio FLSM (Fixed Length Subnet Mask) che VLSM (Variable Length Subnet Mask).

## Funzionalità

- Calcolo delle sottoreti con FLSM o VLSM.
- Supporto per indirizzi IPv4.
- Gestione di più sottoreti e host.
- Output dettagliato con indirizzi di rete, primo e ultimo host, indirizzo di broadcast e subnet mask.

## Utilizzo

Per utilizzare lo script, è necessario specificare l'indirizzo IP di base, il numero di host richiesti per ogni sottorete e il numero di sottoreti. Lo script può essere eseguito direttamente da linea di comando.

## Esempio di Comando per FLSM

```bash
python main.py --ip 192.168.0.0 --hosts 40 --subnets 4
```

### Esempio di Config per FLSM

```json
{
    "ip": "192.168.0.0",
    "hosts": [ 10, 50, 2030 ]
}
```

### Esempio di Config per VLSM

```json
{
    "ip": "192.168.0.0",
    "hosts": 40
}
```

Se nel JSON viene inserito il parametro `"subnets": n`, il sistema mostrerà i risultati per soltanto le prime n subnet.

```json
{
    "ip": "192.168.0.0",
    "hosts": 40,
    "subnets": 4
}
```

## Teoria

### FLSM (Fixed Length Subnet Mask)

FLSM è un approccio in cui tutte le sottoreti hanno la stessa dimensione. Questo significa che ogni sottorete ha lo stesso numero di indirizzi disponibili, indipendentemente dal numero effettivo di host necessari in quella sottorete.

#### Esempio di Calcolo FLSM

- Indirizzo IP di base: `192.168.0.0`
- Numero di host per sottorete: 30
- Subnet Mask: /27 (32 - 5 = 27, poiché 2^5 = 32 indirizzi per sottorete)

In FLSM, ogni sottorete avrà 32 indirizzi, indipendentemente dal fatto che ci siano meno di 30 host per sottorete.

### VLSM (Variable Length Subnet Mask)

VLSM permette di assegnare subnet mask di diverse lunghezze in base al numero di host richiesti in ogni sottorete. Ciò consente un utilizzo più efficiente degli indirizzi IP, riducendo gli sprechi.

#### Esempio di Calcolo VLSM

- Indirizzo IP di base: `192.168.0.0`
- Numero di hosts richiesto per sottorete: [10, 50, 200]
  - Sottorete 1: 10 host -> Subnet Mask /28
  - Sottorete 2: 50 host -> Subnet Mask /26
  - Sottorete 3: 200 host -> Subnet Mask /24

In VLSM, le sottoreti possono avere dimensioni diverse, ottimizzando l'allocazione degli indirizzi in base alle esigenze specifiche.

## Contribuire

I contributi al progetto sono benvenuti! Si prega di aprire una pull request o un issue per suggerimenti o miglioramenti.

## Licenza

[Inserire la licenza qui]
