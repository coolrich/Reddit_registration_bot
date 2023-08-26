import pprint

import jsonlines as jsonl
from data import Data
from sign_up_for_reddit import SignUpForReddit
from password_generator import generate_pswd


class RedditAccountsFactory:
    @staticmethod
    def create_accounts(number_of_acc: int = 1, delay_int_minutes: int = 0, use_proxy: bool = False):
        accounts = []
        for i in range(1, number_of_acc + 1):
            data = Data.email_pswd_list.pop()
            email = data['email']
            # pswd = data['pswd']
            pswd = generate_pswd()
            acc_details = SignUpForReddit(email=email, password=pswd, use_proxy=use_proxy).execute()
            # acc_details = {'email': email, 'password': pswd}
            accounts.append(acc_details)
            RedditAccountsFactory.__waiting(delay_int_minutes)
        # pprint.pp(accounts)
        RedditAccountsFactory.record_to_file(accounts)

    @staticmethod
    def record_to_file(accounts):
        with jsonl.open('creds.jsonl', 'w') as writer:
            for account in accounts:
                writer.write(account)

    @staticmethod
    def __waiting(delay_int_minutes):
        minutes = 60 * delay_int_minutes
        SignUpForReddit.wait(60 * minutes)


RedditAccountsFactory.create_accounts(1, use_proxy=False)
