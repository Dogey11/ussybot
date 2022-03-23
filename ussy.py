import praw
from dotenv import load_dotenv
from os import getenv as env
from time import sleep

load_dotenv()

reddit = praw.Reddit(
    user_agent=env("USSY_UA"),
    client_id=env("USSY_ID"),
    client_secret=env("USSY_SECRET"),
    username=env("USSY_USER"),
    password=env("USSY_PWD")
)

class string_manipulation:
    @staticmethod
    def tense(c):
        return c[-1] in "ds"

    @staticmethod
    def ends_in_vowel(c):
        return c[-1] in "aeiouyAEIOUY"

    @staticmethod
    def ends_in_punctuation(c):
        return c[-1] in ".,;:!?"


    @staticmethod
    def add_ussy(c):
        new_list = []

        splitC = c.split()
        for i in splitC:
            if i[-4:] != "ussy" or i[-4:] != "USSY":

                punc_type = None

                if len(str(i)) > 3:
                    if string_manipulation.ends_in_punctuation(i):
                        punc_type = i[-1]
                        i = i[:-1]
                    if string_manipulation.tense(i):
                        i = i[:-1]
                    if string_manipulation.ends_in_vowel(i):
                        i = i[:-1]

                if punc_type is not None:
                    new_list.append(i + f"ussy{punc_type} ")
                else:
                    new_list.append(i + "ussy ")
        return ' '.join(new_list)
            


def main():
    while True:
        sleep(10)
        try:
            for c in reddit.inbox.mentions(limit=None):

                if c.new:
                    cp = c.parent()
                    if "--ussynr" not in cp.body and cp.author != "ussybot":
                        ussy = string_manipulation.add_ussy(cp.body)
                        reply = None
                        if c.author != cp.author:
                            reply = f"{ussy}\n\n^Comment ^from u/{cp.author}, ^requested ^by u/{c.author}"
                        else:
                            reply = f"{ussy}\n\n^Requested ^by u/{c.author}"
                        if reply is not None:
                            c.reply(reply)
                            with open("log.txt", "a") as f:
                                f.write(f"{c.id}\n")
                                f.close()
                        c.mark_read()
                    else:
                        with open("ignored.txt", "a") as f:
                            f.write(f"{c.id}\n")
                            f.close()
                        c.mark_read()
        except:
            continue


if __name__ == "__main__":
    main()