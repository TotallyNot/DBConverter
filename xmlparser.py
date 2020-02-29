import xml.sax
from argparse import ArgumentParser
from datetime import datetime

from db import DB


def parse_datetime(time):
    if time == "1970-01-01T00:00:00":
        return None

    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S") if time else None


class XMLListHandler(xml.sax.ContentHandler):
    def __init__(self, tag):
        self.tag = tag
        self.current_tag = ""
        self.fields = {}

    def startElement(self, tag, _):
        self.current_tag = tag

    def characters(self, content):
        self.fields[self.current_tag] = (
            self.fields.get(self.current_tag, "") + content.strip()
        )

    def endElement(self, tag):
        if tag == self.tag:
            self.readEntry(self.fields)
            self.fields = {}

    def readEntry(self, fields):
        raise NotImplementedError


class AccountsHandler(XMLListHandler):
    def __init__(self, db):
        super().__init__("Accounts")
        self.db = db
        self.accounts = []
        self.counter = 0

    def readEntry(self, fields):
        self.accounts.append(
            {
                "id": fields.get("ID"),
                "player_id": fields.get("PlayerID"),
                "player_state": fields.get("PState"),
                "fed_reason": fields.get("PReason"),
                "last_update": parse_datetime(fields.get("Last_Update")),
            }
        )

        if len(self.accounts) >= 100000:
            with self.db.session() as sess:
                sess.insert_accounts(self.accounts)

            self.accounts = []
            self.counter += 1
            print(f"converted {self.counter * 1000000} rows.")


class OKHandler(XMLListHandler):
    def __init__(self, db):
        super().__init__("OK")
        self.db = db
        self.players = []
        self.counter = 0

    def readEntry(self, fields):
        self.players.append(
            {
                "id": fields.get("ID"),
                "player_id": fields.get("PlayerID"),
                "num_id": fields.get("NumId"),
                "name": fields.get("playername"),
                "age": fields.get("playerage"),
                "role": fields.get("UsrRole"),
                "initial_signup": parse_datetime(fields.get("InitSignUp")),
                "last_action": parse_datetime(fields.get("last_action")),
                "total_duration": fields.get("total_duration"),
                "total_units": fields.get("total_units"),
                "rank": fields.get("rank"),
                "level": fields.get("level"),
                "last_update": parse_datetime(fields.get("Last_Update")),
            }
        )

        if len(self.players) >= 100000:
            with self.db.session() as sess:
                sess.insert_player_infos(self.players)

            self.players = []
            self.counter += 1
            print(f"converted {self.counter * 100000} rows.")


def main():
    parser = ArgumentParser()
    parser.add_argument("--engine", type=str, default="sqlite:///accounts.db")

    args = parser.parse_args()
    db = DB(args.engine)

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    print("reading OK table...")
    handler = OKHandler(db)
    parser.setContentHandler(handler)
    parser.parse("./OK.xml")
    print("reading accounts table...")
    handler = AccountsHandler(db)
    parser.setContentHandler(handler)
    parser.parse("./Accounts.xml")


if __name__ == "__main__":
    main()
