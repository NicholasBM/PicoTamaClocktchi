# WiFi Configuration for PicoTamachibi Wireless Pet Visits
# Replace these values with your actual WiFi credentials

WIFI_SSID = "Cavalier Corner"  # Replace with your WiFi network name
WIFI_PASSWORD = "Monty2016$"  # Replace with your WiFi password

# Optional: Static IP configuration (leave as None for DHCP)
STATIC_IP = None  # e.g., "192.168.1.100"
SUBNET_MASK = None  # e.g., "255.255.255.0"
GATEWAY = None  # e.g., "192.168.1.1"
DNS = None  # e.g., "8.8.8.8"

# Pet visiting system configuration
VISIT_PORT = 8080  # Port for pet communication
DISCOVERY_PORT = 8081  # Port for pet discovery
VISIT_DURATION = 300  # Visit duration in seconds (5 minutes)
DISCOVERY_INTERVAL = 30  # How often to broadcast availability (seconds)
