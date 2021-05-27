import jsoncfg
import jinja2
from tldextract import extract
from urllib.parse import urlencode

config = jsoncfg.load_config("config.json")
sections = []
dirEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./templates"))

index_template = dirEnv.get_template("index.html")
target = "yahoo.com"

github_elements = list(
    map(
        lambda x: {
            "full": "https://github.com/search?"
            + urlencode({"q": f'"{target}"+{x}', "type": "Code"}),
            "no_tld": "https://github.com/search?"
            + urlencode({"q": f'"{extract(target).domain}"+{x}', "type": "Code"}),
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
    elems = google_elements(config[key].elements())
    sections.append(
        {"title": f"{config[key].title()} [{len(elems)}]", "elements": elems}
    )

out = index_template.render(sections=sections)

out_f = open("index.html", "w+")
print(out, file=out_f)
