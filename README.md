# Capstone

Setting up the Pi
* Enable SPI
  * Type `sudo raspi-config`
  * Select "Interfacing options"
  * Highlight the "SPI" option and activate "<Select>"
  * Reboot the Pi
* Run at boot
  * Open terminal
  * `sudo nano /home/pi/.bashrc`
  * Add to the end of the script:
    * `sudo python /home/pi/Capstone/main.py`
    * Save and exit nano
  * `sudo reboot`