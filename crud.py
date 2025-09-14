import pandas as pd

class Crud():
    
    file = "/instances/locker.csv"
    
    def __init__(self) -> None:
        with open(self.file, "w") as locker:
            locker.write("site,user,password")

    def create(self, site, user, password):
        with open(self.file, "a") as locker:
            locker.write("\n" + site + "," + user + "," + password)

    def read(self, site):
        df = pd.read_csv(self.file)
        result = df[df["site"] == site]
        return result if not result.empty else None

    def update(self, site, new_user=None, new_password=None):
        df = pd.read_csv(self.file)
        if site in df["site"].values:
            if new_user:
                df.loc[df["site"] == site, "user"] = new_user
            if new_password:
                df.loc[df["site"] == site, "password"] = new_password
            df.to_csv(self.file, index=False)
            return True
        return False

    def delete(self, site):
        df = pd.read_csv(self.file)
        if site in df["site"].values:
            df = df[df["site"] != site]
            df.to_csv(self.file, index=False)
            return True
        return False
        