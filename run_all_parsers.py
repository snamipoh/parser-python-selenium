from subprocess import call

all_parsers = ["n26.py", "evolutiongaming.py", "smartlyio.py", "personio.py", "klarna.py"]

for i in all_parsers:
    call(["python", i])
