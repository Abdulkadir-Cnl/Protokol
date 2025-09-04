import socket
import struct
import threading

# ---------- Paket oluşturma fonksiyonu ----------
def send_command(sock, cmd, x=0, y=0):
    packet = bytearray(16)
    packet[0] = 0xEB
    packet[1] = 0x90
    packet[2] = cmd

    struct.pack_into('<h', packet, 3, x)
    struct.pack_into('<h', packet, 5, y)
    for i in range(7, 15):
        packet[i] = 0x00

    checksum = sum(packet[0:15]) & 0xFF
    packet[15] = checksum
    
    sock.sendall(packet)


# ---------- Hareket Fonksiyonları ----------
def move_right(sock, speed=100):
    send_command(sock, 0x24, x=speed, y=0)

def move_left(sock, speed=100):
    send_command(sock, 0x24, x=-speed, y=0)

def move_up(sock, speed=100):
    send_command(sock, 0x24, x=0, y=speed)

def move_down(sock, speed=100):
    send_command(sock, 0x24, x=0, y=-speed)

def stop(sock):
    send_command(sock, 0x24, x=0, y=0)


# ---------- Komutları işleyen fonksiyon ----------
def handle_client(conn, gimbal_sock):
    with conn:
        print("Yeni istemci bağlandı:", conn.getpeername())
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode().strip().lower()
            print("İstemciden gelen komut:", command)

            # Komutu parse et
            if command.startswith("right"):
                _, val = command.split()
                move_right(gimbal_sock, int(val))
            elif command.startswith("left"):
                _, val = command.split()
                move_left(gimbal_sock, int(val))
            elif command.startswith("up"):
                _, val = command.split()
                move_up(gimbal_sock, int(val))
            elif command.startswith("down"):
                _, val = command.split()
                move_down(gimbal_sock, int(val))
            elif command == "stop":
                stop(gimbal_sock)
            else:
                print("Geçersiz komut:", command)


# ---------- Server döngüsü ----------
def server_loop(gimbal_host="192.168.1.100", gimbal_port=2000,
                server_host="0.0.0.0", server_port=5000):

    # Önce gimbal'a bağlan
    gimbal_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gimbal_sock.connect((gimbal_host, gimbal_port))
    print("Gimbal'a bağlandı:", (gimbal_host, gimbal_port))

    # Sonra bizim kontrol server'ını başlat
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen(5)
        print(f"Kontrol server'ı {server_port} portunda dinliyor...")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client,
                             args=(conn, gimbal_sock),
                             daemon=True).start()


if __name__ == "__main__":
    server_loop()
