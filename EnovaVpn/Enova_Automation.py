# main.py

from wireguardtest import setup_driver, wireguard
from ipsectest import setup_driver,ipsec

def main():
    driver = setup_driver()

    ipsec(driver)
    wireguard(driver)


if __name__ == "__main__":
    main()
