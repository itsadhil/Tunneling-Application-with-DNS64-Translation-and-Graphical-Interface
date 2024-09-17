# Tunneling Application with DNS64 Translation and Graphical Interface

This project is a Python-based tunneling application that leverages DNS64 to translate IPv4 addresses into IPv6. It includes both client and server components, with a graphical interface (Tkinter) for sending and receiving packages, logging activities, and visualizing packet transfer progress in real-time.

## Features
- **DNS64 Translation**: Converts IPv4 addresses to IPv6 addresses.
- **Client-Server Communication**: The client sends packets, and the server translates and responds using DNS64.
- **Graphical Interface**: A Tkinter UI for packet sending/receiving and logging.
- **Real-Time Graphing**: Packet transfer progress is plotted dynamically using `matplotlib`.
- **Multithreading**: Both sending and receiving processes run on separate threads, ensuring the UI remains responsive.

## Dependencies
- Python 3.x
- `socket` (standard library)
- `ipaddress` (standard library)
- `tkinter` (standard library)
- `matplotlib`
- `threading` (standard library)

### Installing Dependencies
If you don't have `matplotlib` installed, you can install it using `pip`:

```bash
pip install matplotlib
