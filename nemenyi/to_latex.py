import numpy as np
import math

def normalize_by_width(ranks, width):
    return ([x * width / len(ranks) for x in ranks])

def get_segments(ranks, cd):
    conected_points = []
    for i in range(len(ranks)):
        p2 = -1
        for j in range(i + 1, len(ranks)):
            if (ranks[j] - ranks[i] < cd):
                p2 = j
        if p2 != -1:
            conected_points.append([i, p2])

    found = True

    while found:
        point_to_remove = findInner(conected_points, ranks)
        if point_to_remove != -1:
            conected_points.remove(point_to_remove)
        else:
            found = False

    return conected_points


def findInner(segments, ranks):
    for i in segments:
        for j in segments:
            if i != j:
                if ranks[i[0]] >= ranks[j[0]] and ranks[i[1]] <= ranks[j[1]]:
                    return i
                if ranks[i[0]] <= ranks[j[0]] and ranks[i[1]] >= ranks[j[1]]:
                    return j
    return -1


def writeTex(names, ranks, cd, width=7, file_tex="output.tex"):

    names_sorted = [x for _, x in sorted(zip(ranks, names))]
    ranks_sorted = sorted(ranks)

    segments = get_segments(ranks_sorted, cd)

    ranks_normalized = normalize_by_width(ranks_sorted, width - 1)

    lineFormat = "decorate,decoration={snake,amplitude=.4mm,segment length=1.5mm,post length=0mm}, very thick, color = black";

    points = range(1, len(ranks) + 1)
    points = normalize_by_width(points, width - 1)

    normCd = cd * (width - 1.) / len(names)
    lastRank = len(names) - 1
    margin = 0.5
    leftLabelPosition = margin
    rightLabelPosition = margin + len(ranks) * (width - 1.) / len(ranks)

    text_script = "\\begin{figure} \\centering \\begin{tikzpicture}[xscale=2]\n"
    text_script = text_script + "\\node (Label) at ({},0.7)".format(points[0] + normCd / 2.) + "{\\tiny{CD=" + "{}".format(cd) + "}}; % the label\n"
    text_script = text_script + "\\draw[" + lineFormat + "] ({},0.5) -- ({},0.5);\n".format(points[0], points[0] + normCd)
    text_script = text_script + "\\foreach \\x in {" + "{},{}".format(points[0], points[0] + normCd) + "} \\draw[thick,color = black] (\\x, 0.4) -- (\\x, 0.6);\n \n"
    text_script = text_script + "\\draw[gray, thick]({},0) -- ({},0); \n".format(points[0], points[lastRank])
    text_script = text_script + "\\foreach \\x in {"
    text_script = text_script + ",".join(map(str, points)) + "} \\draw (\\x cm,1.5pt) -- (\\x cm, -1.5pt);\n"

    for idx, p in enumerate(points):
        text_script = text_script + "\\node (Label) at ({},0.2)".format(p)+ "{\\tiny{" + "{}".format(idx) + "}};\n"

    startY = -0.25
    deltaY = -0.15
    yaxe = []
    x1 = 0

    for idx in range(len(segments)):
        seg = segments[idx]
        x1 = ranks_normalized[seg[0]] - 0.05
        x2 = ranks_normalized[seg[1]] + 0.05
        if idx == 0:
            yaxe.append(startY)
        else:
            y = startY
            for prev in range(idx - 1, -1, -1):
                ant = segments[prev]
                previousX2 = ranks_normalized[ant[1]] + 0.5
                if x1 - previousX2 <= 0.1 and yaxe[prev] == y:
                    y = y + deltaY
            yaxe.append(y)
        text_script = text_script + "\\draw[" + lineFormat + "]({},{}) -- ({},{});\n".format(x1, yaxe[idx], x2, yaxe[idx])

    base = 0.25 + 0.2 * len(yaxe)
    x1 = 0.3

    for idx in range(int(len(names) / 2)):
        text_script = text_script + "\\node (Point) at ({}, 0)".format(ranks_normalized[idx]) + "{};" + "  \\node (Label) at ({},{})".format(leftLabelPosition, idx * x1 + base)
        text_script = text_script + "{\\scriptsize{" + "{}".format(names_sorted[idx]) + "}}; \\draw (Point) |- (Label);\n"
    for idx in range(len(names) - 1, int((len(names) / 2)) - 1, -1):
        text_script = text_script + "\\node (Point) at ({}, 0)".format(ranks_normalized[idx]) + "{};" + "  \\node (Label) at ({},{})".format(rightLabelPosition, (len(names) - (idx + 1)) * x1 + base)
        text_script = text_script + "{\\scriptsize{" + "{}".format(names_sorted[idx]) + "}}; \\draw (Point) |- (Label);\n"

    text_script = text_script + "\\end{tikzpicture}\n"
    text_script = text_script + "\\caption{Nemenyi post hoc test}\n"
    text_script = text_script + "\\label{fig:nemeny}\n"
    text_script = text_script + "\\end{figure}\n"

    text_file = open(file_tex, "w")
    text_file.write(text_script)
    text_file.close()
