
import sys
from termcolor import colored

tool_header = '''
____ ____    ___  ____ ____ _  _ _ _  _ ____ 
| __ | __ __ |  \ |  | |__/ |_/  | |\ | | __ 
|__] |__]    |__/ |__| |  \ | \_ | | \| |__] 
'''
tool_header2 = '''	   Coded By: Eslam Akl
	Blog: eslam3kl.medium.com
'''
site = sys.argv[1]
company = site.split(".")[0]
content = '''
*---------------------------------------------*
| GitHub Dorking (W/O TLD)     |   64 Link    |
| SQL Error messages & Leaks   |   216 Link   |
| Extensions & file types      |   221 Link   |
| Index of files               |   49 Link    |
| Vulnerabilities (SQLi & LFI) |   30 Link    |
| Others                       |   235 Link   | 
*---------------------------------------------*
'''
file = "Output file: %s.html" % company

error_file = "error_messages.txt"
ext_file = "file_extension.txt"
index_file = "index.txt"
other_file = "other.txt"
github_words = "github_words.txt"
vulnerabilities = "vulners.txt"
sql = "sql_error.txt"


def github_dorking(file,site,title):
	print('<button class="collapsible">%s</button>' %title)
	print('<div class="content">')
	with open(file, "r") as wordlist:
		for query in wordlist:
			query = query.strip()
			line = query.replace(' ', '%20')
			without_tld = site.split(".")[0].strip()
			link = "https://github.com/search?q=%22" + site + "%22+" + query + "&type=Code"
			link_without_tld = "https://github.com/search?q=%22" + without_tld + "%22+" + query + "&type=Code"
			print('<a>[+] %s</a>' %(query))
			print("</br>")
			print('<a href="%s" target="_blank">Full Domain</a>' %(link))
			print("</br>")
			print('<a href="%s" target="_blank">Without TLD</a>' %(link_without_tld))
			print("</br>")
	print('</div>')

def google_dorking(file,site,title):
	print('<button class="collapsible">%s</button>' %title)
	print('<div class="content">')
	with open(file, "r") as wordlist:
		i = 1
		for query in wordlist:
			query = query.strip()
			line = query.replace('"', "'")
			line2 = "site:" + site + " " + line + " -stackoverflow -wpbeginner -foro -forum -topic -blog -about -docs -articles"
			line_plus = line2.replace(" ", "+")
			link = "http://www.google.com/search?q=" + line_plus
			print('<a>[%d]</a>' %i)
			print('<a href="%s" target="_blank">%s</a>' %(link,query))
			print("</br>")
			i = i + 1
	print('</div>')


header = '''
<!DOCTYPE html>
<html>
<head>
   <title>GitHub & Google Dorking</title>
<h2 style="text-align: center;">GG Dorking</h2>
<h3 style="text-align: center;">Coded By Eslam Akl @eslam3kl</h3>
</br>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
  font-family: Arial;
  margin: 0;
}
.collapsible {
  background-color: #777;
  color: white;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

.header {
  padding: 10px;
  text-align: center;
  background: #1abc9c;
  color: white;
  font-size: 30px;
}

.active, .collapsible:hover {
  background-color: #555;
}

.collapsible:after {
  content: '\002B';
  color: white;
  font-weight: bold;
  float: right;
  margin-left: 5px;
}

.active:after {
  content: "\2212";
}

.content {
  padding: 0 18px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
  background-color: #f1f1f1;
}

<div class="header">
  <h1>Header</h1>
  <p>My supercool header</p>
</div>

</style>
</head>
<body>

'''

footer='''

<script>
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    } 
  });
}
</script>


</body>
</html>
'''

print(colored(tool_header, "red", attrs=['bold']))
print(colored(tool_header2, "yellow", attrs=['bold']))
print(colored(content, "green"))
print(colored(file, "white"))
print("\n")

output_file = "%s.html" %company
sys.stdout = open(output_file, "w+")
print(header)
github_dorking(github_words,site,"GitHub Dorking [64]")
google_dorking(sql,site,"SQL Leaks/Errors [216]")
google_dorking(ext_file,site,"Extensions [221]")
google_dorking(index_file,site,"Index of [49]")
google_dorking(vulnerabilities,site,"Vulnerabilities [30]")
google_dorking(other_file,site,"Others [235]")
print(footer)
sys.stdout.close()
