import sys

import jsoncfg
import jinja2
from termcolor import colored
from tldextract import extract
from urllib.parse import urlencode
import argparse

parser = argparse.ArgumentParser(description="Generate GitHub and Google dorking links")
parser.add_argument("target", help="Your target ex yahoo.com")
parser.add_argument(
    "--out",
    nargs="?",
    help="Output File name, defaults to {target}.html",
    required=False,
)
parser.add_argument("--config", nargs="?", help="Config file, defaults to config.json")
try:
    args = parser.parse_args()
except:
    parser.print_help()
    exit(1)

content = r"""
*---------------------------------------------*
| GitHub Dorking (W/O TLD)     |   64 Link    |
| SQL Error messages & Leaks   |   216 Link   |
| Extensions & file types      |   221 Link   |
| Index of files               |   49 Link    |
| Vulnerabilities (SQLi & LFI) |   30 Link    |
| Others                       |   235 Link   | 
*---------------------------------------------*
"""
tool_header = r"""
____ ____    ___  ____ ____ _  _ _ _  _ ____ 
| __ | __ __ |  \ |  | |__/ |_/  | |\ | | __ 
|__] |__]    |__/ |__| |  \ | \_ | | \| |__] 
"""
tool_header2 = """	   Coded By: Eslam Akl
	Blog: eslam3kl.gitbook.io
"""

sections = []
dirEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./templates"))
index_template = dirEnv.get_template("index.html")

print(colored(tool_header, "red", attrs=["bold"]))
print(colored(tool_header2, "yellow", attrs=["bold"]))
print(colored(content, "green"))

target = args.target
output = args.out if args.out else f"{target}.html"
config_file = args.config if args.config else "config.json"

try:
    config = jsoncfg.load_config(config_file)
except FileNotFoundError as e:
    print("File error: " + colored(f"No such file or directory '{config_file}'", "red", attrs=["bold"]))
    exit(1)
except jsoncfg.parser.JSONConfigParserException as e:
    print("JSON error: " + colored(f"{e}", "red"))
    exit(1)
except:
    print("Oops!", sys.exc_info()[0], "occurred.")
    exit(1)

github_elements = list(
    map(
        lambda x: {
            "full": "https://github.com/search?"
            + urlencode({"q": f'"{target}" {x}', "type": "Code"}),
            "no_tld": "https://github.com/search?"
            + urlencode({"q": f'"{extract(target).domain}" {x}', "type": "Code"}),
            "subtitle": x,
        },
        config["github"]["elements"](),
    )
)
sections.append(
    {
        "title": f"{config.github.title()} [{len(github_elements)}]",
        "elements": github_elements,
    }
)


def google_elements(elems):
    return list(
        map(
            lambda x: {
                "link": "http://www.google.com/search?"
                + urlencode(
                    {
                        "q": f"site:{target} -stackoverflow -wpbeginner -foro -forum -topic -blog -about -docs -articles {x}"
                    }
                ),
                "text": x,
            },
            elems,
        )
    )


for key in config._dict.keys():
    if key == "github":
        continue
    elems = google_elements(config[key].elements())
    sections.append(
        {"title": f"{config[key].title()} [{len(elems)}]", "elements": elems}
    )
print(colored(f'Writing output to file "{output}"', "white", attrs=["bold"]))
out = index_template.render(sections=sections)

out_f = open(output, "w+", encoding="utf-8")
print(out, file=out_f)
