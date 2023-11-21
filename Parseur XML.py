from os.path import getsize


class XmlBalise:
    def __init__(self,name,content,attrs,childs):
        self.name = name
        self.content = content
        for k,v in attrs.items():
            setattr(self,k,v)
        
        child_names = [child.name for child in childs]
        doubles = []
        for child in childs:
            if child_names.count(child.name) > 1:
                doubles.append(child.name)
                setattr(self,child.name+str(doubles.count(child.name)),child)
            else:
                setattr(self,child.name,child)
    def __str__(self):
        return "balise"+" "+self.name

class XmlDoc:
    def __init__(self,path):
        with open(path) as xml_file:
            xml_text = ""
            for line in xml_file.readlines():
                xml_text += line.strip()
        tree = parse(xml_text)
        setattr(self,tree.name,tree)

        self.path = path

        if "/" in self.path:
            self.name = self.path.split("/")[-1]
        elif "\\" in self.path: 
            self.name = self.path.split("\\")[-1]
        else:
            self.name = self.path
        self.byte_size = getsize(self.path)
        self.bit_size = self.byte_size*8


 

def format_balise(balise):
    new_balise = ""

    for i,c in enumerate(balise):

        if c == " " and (balise[i+1] in(" ","=",">") or balise[i-1] in ("=","<")):
            continue

        new_balise += c

    return new_balise

def parse_balise(balise):
    balise = format_balise(balise)
    body = balise[1:-1].split()

    nom,*attributs = body

    for i in range(len(attributs)):
        attributs[i] = attributs[i].split("=")

    close_balise = "</"+nom+">"
    attributs = dict(attributs)
    return balise,close_balise,nom,attributs

def get_balise(xml,i=0):
    end = xml[i:].index(">") + len(xml[:i])
    return xml[i:end+1]


def get_full_balise(xml,start,start_balise,end_balise):
    len_start = len(start_balise)
    len_end = len(end_balise)
    i = start
    nb_open = 0
    nb_close = 0
    while nb_open != nb_close or nb_open == 0:
        if xml[i:i+len_start] == start_balise:
            nb_open += 1
        elif xml[i:i+len_end] == end_balise:
            nb_close += 1
        i += 1

    
    return xml[start:i+len_end-1]

def get_content(xml,start):
    i = start
    while not xml[i] in "<":
        if xml[i] == ">":
            raise ValueError("getting content inside a balise")
        i += 1
    return xml[start:i]
    


def parse(xml):

    balise = get_balise(xml)
    start,end,name,attrs = parse_balise(balise)

    i = 0

    body = xml[len(balise):len(xml)-len(end)]
    childs = []

    if not "<" in body:
        return XmlBalise(name,body,attrs,[])

    content = ""
    while i < len(body):
        if body[i] == "<":
            nested_start = get_balise(body,i)
            _,nested_end,*_ = parse_balise(nested_start)
            nested_balise = get_full_balise(body,i,nested_start,nested_end)
            childs.append(parse(nested_balise))
            i += len(nested_balise)

        else:
            txt = get_content(body,i)
            content += txt
            i += len(txt)
    return XmlBalise(name,content,attrs,childs)

xml = XmlDoc("my_xml.xml")
print(xml.html)
print(xml.byte_size)


