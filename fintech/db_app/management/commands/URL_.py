URL_TEMPLATE = "https://www.boi.org.il/_layouts/boi/handlers/WebPartHandler.aspx?wp=RestrictedAccountsSearch&lang=he-IL&Bank={}&Branch={}&Account={}&webUrl=/he/ConsumerInformation/RestrictedAccountsAndCustomers&isMobile=true"


class URL_:
    def __init__(self, account_info: dict):
        self.branch = "{:03}".format(account_info["branch"])
        self.account = account_info["account"]
        self.bank = "{:02}".format(account_info["bank"])

    def get_url(self):
        return URL_TEMPLATE.format(self.bank, self.branch, self.account)


if __name__ == "__main__":
    pass
