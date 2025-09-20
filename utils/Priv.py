class PrivLevel:
    def __init__(self, _input):
        self.privileges = []
        self.reload(_input)

    def reload(self, _input):
        self.privileges = list(map(int, _input.split(",")))
        self.privileges.sort(reverse=1)

    def append(self, privilege):
        if privilege in self.privileges:
            return#raise Exception(f"Already has PRIV#{privilege}")
        self.privileges.append(privilege)
        self.privileges.sort(reverse=1)

    def remove(self, privilege):
        if not privilege in self.privileges:
            return#raise Exception("Not found")

        self.privileges.remove(privilege)
        self.privileges.sort(reverse=1)

    def output(self):
        return ",".join(map(str, self.privileges))

    def upper(self, privilege, equals=True):
        if equals:
            return self.uppermost() >= privilege
        else:
            return self.uppermost() > privilege

    def uppermost(self):
        return self.privileges[0]

    def lower(self, privilege, equals=True):
        if equals:
            return self.uppermost() <= privilege
        else:
            return self.uppermost() < privilege

    def lowest(self):
        return self.privileges[-1]

    def notin(self, privilege):
        return not privilege in self.privileges

    def only(self, privilege):
        return self.privlege == [privilege]

    def includes(self, *privileges):
        if len(privileges) == 1:
            return privileges[0] in self.privileges

        found = False
        for privilege in privileges:
            if privilege in self.privileges:
                found = True
                break
        return found
