import sys
from sender import Sender
from receiver import Receiver

def main():
    print("Welcome to P2P Share over LAN")
    name = input("Enter your device name: ").strip()

    while True:
        print("\nSelect mode:")
        print("1. Send a file")
        print("2. Receive a file")
        print("3. Exit")

        choice = input("Your choice (1/2/3): ").strip()

        if choice == '1':
            sender = Sender(name)
            sender.start()

        elif choice == '2':
            receiver = Receiver(name)
            try:
                receiver.start()
            except KeyboardInterrupt:
                receiver.stop()
                print("Receiver stopped.")
                sys.exit(0)

        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
