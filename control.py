import sys

def main():
    sys.argv.pop(0)
    args = [arg.strip() for arg in sys.argv]

    if len(args) == 0:
        print("Usage: python control.py [basic|facetrack|console]")
        return

    mode = args[0]
    if mode == 'facetrack':
        import controllers.face_tracking
    elif mode == 'console':
        import controllers.console
    else:
        print(f"Unknown argument: {mode}")

if __name__ == '__main__':
    main()
