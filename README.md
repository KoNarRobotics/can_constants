# Baza danych wiadomości na magistrali CAN

## Budowa bazy danych

```
can_messages
├── abstract				<--- warstwa abstrakcji upraszczająca definicje wiadomości
│   ├── message.py
│   ├── modules.py
│   └── signals.py
├── generator.py			<--- skrypt generatora, łączy wiadomości w plik DBC i generuje z niego pliki C
├── messages				<--- zbiór skryptów definiujących wiadomości
│   ├── actuators.py
│   ├── battery.py
│   ├── buzzer.py
│   ├── control_mode.py
│   ├── gps.py
│   ├── imu.py
│   ├── metal_detector.py
│   ├── odrive.py
│   └── temperature.py
└── output					<--- pliki wygenerowane przez generator
    ├── can_messages.c
    ├── can_messages.dbc
    └── can_messages.h
```

## Generowanie plików C

### Prosty sposób

1. Wywołaj skrypt i odpręż się:

```bash
./generate-files.sh
# lub dla wirtualnego środowiska
./generate-files.sh -v
```

- flaga `-v` pobierze pakiety pathona w środowisku wirtualnym

### Ręczne wywołanie

Będąc w katalogu `can_messages` należy wywołać:

```bash
python3 generator.py
```

Jeśli nie istniał, zostanie utworzony katalog `output`, w który pojawią się pliki.

Operację tą należy wykonać gdy:

- klonujemy repo
- `git pull`
- program nie działa

## Dodanie do projektu

Najprostszym sposobem dodania do projektu dodanie bazy jako biblioteki statyczniej do projektu.

```cmake

add_subdirectory(can_constants) # or other path to the submodule

target_link_libraries(${PROJECT_NAME}
  can_constants
  # and other libs ...
)
```

## Zastosowanie

Przykład zakodowania danych:

```c
struct can_example_t example_data;
uint8_t example_buffer[8];

// encode
example_data.foo = can_example_foo_encode(21.37f);
example_data.bar = can_example_bar_encode(0x1337);

// pack
can_example_pack(example_buffer, &example_data, sizeof(example_buffer));

// send
send(CAN_EXAMPLE_FRAME_ID, frame_buffer, CAN_EXAMPLE_LENGTH);
```

Przykład odkodowania danych:

```c
message_t message;
struct can_example_t example_data;
float foo;
uint16_t bar;

// unpack
can_example_unpack(&example_data, message.buffer, message.size);

// decode
foo = can_example_foo_decode(example_data.foo);
bar = can_example_bar_decode(example_data.bar);

// check range
if(!can_example_foo_is_in_range(foo))
	// error
if(!can_example_bar_is_in_range(bar))
	// error
```

## Format bazy danych

Przykładowy format zapisu grupy wiadomości:

```python
db = [

	Message(0x701, 'buzzer_beep', 0, senders=[Module.JETSON], receivers=[Module.POWER], signals=[]),

	Message(0x702, 'buzzer_play_note', 4, senders=[Module.JETSON], receivers=[Module.POWER], signals=[
		Unsigned('frequency', 0, 16, unit='Hz'),
		Unsigned('duration', 16, 16, unit='ms')
	])

]
```

## Wiadomości

Obiekt wiadomości `Message` zawiera w sobie:

- ID ramki (musi być unikatowe)
- nazwa w stringu (musi być unikatowa)
- ilość bajtów danych (max 8)
- lista nadawców
- lista odbiorców
- lista sygnałów

## Sygnały

Sygnały mogą być pakowane w wiadomości w dowolnej kolejności i ilości pod warunkiem, że nie będą na siebie nachodzić oraz że ich łączny rozmiar nie przekroczy 8 bajtów.

`Enum` - typ wyliczeniowy używany do przesyłu ograniczonej liczby opcji. Wartości moga przyjmować liczby całkowite.

`Unsigned` - liczba całkowita o zdefiniowanej ilości bitów. Wariant bez znaku.

`Signed` - liczba całkowita o zdefiniowanej ilości bitów. Wariant z znakiem.

`Float` - 32-bitowy typ zmiennopozycyjny. Możliwość użycia podwójnej precyzji.

`Bool` - jednobitowa zmienna logiczna, do wysyłania zero-jedynkowych wiadomości.
