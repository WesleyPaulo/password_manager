import pandas as pd
import os

class Crud():
    
    file = ""
    
    def __init__(self, file="locker.csv",base_dir="lockers") -> None:
        # Cria a pasta se não existir
        os.makedirs(base_dir, exist_ok=True)
        
        # Caminho completo para o arquivo
        self.file = os.path.join(base_dir, file)
        
        if not os.path.exists(self.file):
            with open(self.file, "w") as locker:
                locker.write("site,user,password\n")

    def create(self, site, user, password):
        df = pd.read_csv(self.file)
        df.loc[len(df)] = [site, user, password]
        df.to_csv(self.file, index=False)

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
    
    def list_all(self):
        df = pd.read_csv(self.file)
        return df
        