from multiprocessing import Process
import time


if __name__ == "__main__":
    # Staring falsk process    
    proc = Process(target=start_process, args=(x,))
    proc.start()
    