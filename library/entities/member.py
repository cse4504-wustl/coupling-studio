class FinePolicy:
    def __init__(self, daily_rate):
        self._daily_rate = daily_rate

    def get_daily_rate(self):
        return self._daily_rate


class Account:
    def __init__(self, balance, fine_policy):
        self._balance = balance
        self._fine_policy = fine_policy

    def get_balance(self):
        return self._balance

    def set_balance(self, balance):
        self._balance = balance

    def get_fine_policy(self):
        return self._fine_policy


class Member:
    def __init__(self, member_id, name, member_type, account):
        self.member_id = member_id
        self.name = name
        self.member_type = member_type  # "student" or "faculty"
        self._account = account

    def get_account(self):
        return self._account
