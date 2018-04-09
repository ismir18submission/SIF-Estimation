class Annotation:
    string = 0
    fret = 0
    guitar_type = ""
    playing_type = ""
    filename = ""

    def __init__(self, g_s, g_f, g_t, p_t, fn):
        # type: (int, int, string, string) -> Annotation
        self.string = g_s
        self.fret = g_f
        self.guitar_type = g_t
        self.playing_type = p_t
        self.filename = fn


def annotations_to_labels(annotations):
    labels = []
    for annotation in annotations:
        labels.append(annotation.string)
    return labels


def from_indexlist(annotations, list):
    a = []
    for index in list:
        a.append(annotations[index])
    return a


def from_wav(filename):
    filename = filename[:-4]
    fn_split = filename.split("_")
    guitar_type = fn_split[0]
    playing_type = fn_split[1]
    guitar_string = int(fn_split[2])
    guitar_fret = int(fn_split[3])
    return Annotation(guitar_string, guitar_fret, guitar_type, playing_type, filename)


def from_xml(root):
    guitar_string = int(root[1][0][4].text)
    guitar_fret = int(root[1][0][3].text)
    guitar_type = root[0][1].text
    playing_type = "plucked"
    filename = root[0][0].text[:-4]
    return Annotation(guitar_string, guitar_fret, guitar_type, playing_type, filename)


def make_annotation(g_s, g_f, g_t, p_t, fn):
    annotation = Annotation(g_s, g_f, g_t, p_t, fn)
    return annotation
