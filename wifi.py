import network
import time
from machine import Timer

def setup_ap(ssid='ESP32-AP', password="lollollol", timeout_sec=10):
    """
    Set up ESP32 as an Access Point with timeout protection and debug prints
    Returns: True if AP setup successful, False if timeout occurred
    """
    print("\n=== Starting AP Setup ===")
    print(f"SSID: {ssid}")
    print(f"Timeout: {timeout_sec} seconds")

    ap = network.WLAN(network.AP_IF)  # Change to AP_IF for access point mode
    print('network.WLAN() complete')
    print(f"Initial AP state: {'active' if ap.active() else 'inactive'}")

    print('ap.active() complete ...')


    # Flag for timeout callback
    setup_complete = False

    def timeout_handler(timer):
        nonlocal setup_complete
        if not setup_complete:
            print("!!! Hardware timer timeout triggered !!!")
            ap.active(False)
            print("AP forcefully deactivated by timeout handler")

    # Set up timeout timer
    print("Initializing hardware timeout timer...")
    timer = Timer(0)
    timer.init(period=timeout_sec * 1000, mode=Timer.ONE_SHOT, callback=timeout_handler)
    print("Timer initialized successfully")
    
    try:
        print("\nActivating AP interface...")
        ap.active(True)
        print("AP interface activated")  # Add this line to confirm activation call

        print("Setting AP configuration...")
        ap.config(essid=ssid, password=password)
        print("Configuration set")
        
        # Wait for AP to become active
        print("\nWaiting for AP to become active...")
        start_time = time.time()
        attempt = 0
        
        while not ap.active():
            attempt += 1
            current_time = time.time()
            elapsed = current_time - start_time
            
            if elapsed > timeout_sec:
                print(f"\n!!! Software timeout after {elapsed:.1f} seconds !!!")
                print(f"Made {attempt} checks")
                ap.active(False)
                print("AP deactivated due to timeout")
                return False
                
            if attempt % 10 == 0:  # Print status every 10 attempts
                print(f"Still waiting... {elapsed:.1f}s elapsed, attempt {attempt}")
            time.sleep(0.1)
            
        setup_complete = True
        timer.deinit()  # Cancel timeout since setup succeeded
        
        print("\n=== AP Setup Successful ===")
        print("Network Configuration:")
        config = ap.ifconfig()
        print(f"IP Address: {config[0]}")
        print(f"Subnet Mask: {config[1]}")
        print(f"Gateway: {config[2]}")
        print(f"DNS Server: {config[3]}")
        
        # Print additional status information
        print("\nAP Status:")
        try:
            print(f"Channel: {ap.config('channel')}")
            print(f"Hidden: {ap.config('hidden')}")
            print(f"Security: {ap.config('security')}")
            print(f"Max Clients: {ap.config('max_clients')}")
        except Exception as e:
            print(f"Couldn't get some AP configs: {e}")
        
        return True
        
    except Exception as e:
        print(f"\n!!! Error during AP setup !!!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        print("Attempting to deactivate AP...")
        try:
            ap.active(False)
            print("AP deactivated successfully")
        except Exception as cleanup_error:
            print(f"Error during cleanup: {cleanup_error}")
        return False
