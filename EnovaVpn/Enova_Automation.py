
import time

from wireguardtest import setup_driver, wireguard
from ipsectest import setup_driver,ipsec
from shadowsockstest import setup_driver,shadowsocks

def main():
    driver = setup_driver()
    shadowsocks(driver)
    time.sleep(10)
    #
    # driver = setup_driver()
    # ipsec(driver)
    # time.sleep(10)

    # driver = setup_driver()
    # wireguard(driver)
    # time.sleep(10)





if __name__ == "__main__":
    main()
