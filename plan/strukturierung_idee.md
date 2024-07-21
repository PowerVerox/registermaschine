# Idee

## OOP-Timianisch

| Class Instruction       |
| ----------------------- |
| data : str              |

| Class Registermachine       |
| --------------------------- |
| instructions: Instruction[] |
| programcounter: int         |
| memory: bytearray           |
| --------------------------- |
| load(path: str)             |
| verify()                    |
| run()                       |

## Alternativen

### Maschine erhält Programm

| Class Instruction       |
| ----------------------- |
| data : str              |
| ----------------------- |
| toString() -> str       |

| Class Program               |
| --------------------------- |
| instructions: Instruction[] |
| --------------------------- |
| load(path: str) -> Program  |
| ~~verify()~~                |
| toString() -> str           |

| Class Registermachine       |
| --------------------------- |
| *program: Program*          |
| *programcounter: int*       |
| memory: bytearray           |
| --------------------------- |
| run(program) -> void        |
| toString() -> str           |

## Anmerkungen

In STP gibt es einen Context, der einen Ausdruck evaluiert.
Jeweils als Klassen/Interfaces implementiert.
Der Context entspricht einem Scope / Ausführungsblock in einer "richtigen" Sprache.
Der Kontext würde hier wohl der Registermaschine entsprechen.
Ich würde daher vorschlagen, dass run() die komplette Evaluierung übernimmt.
Statt Switch-Case nutze ich in STP benannte Lambdas.
Das ist hier nicht erforderlich, würde das ganze aber ohne Aufwand benutzerdefiniert erweiterbar machen.
