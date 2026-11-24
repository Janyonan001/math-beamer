"""
教材截图 → Beamer 课件 生成器（图片嵌入版）

功能：
  1. 读取教材截图
  2. 把每张图片作为一页嵌入到 beamer 中
  3. 生成符合 Madrid + beaver 主题的 beamer tex 文件

用法：
  python tex_from_images.py --images img1.png img2.png --title "3.1.1函数的概念" --output output.tex
"""

import argparse
import os
from pathlib import Path


BEAMER_HEADER = r"""\documentclass[aspectratio=169,13pt,t] {beamer}
\mode<presentation>
{
  \usetheme{Madrid}
  \usecolortheme{beaver}
  \usefonttheme{serif}
  \setbeamertemplate{caption}[numbered]
  \setbeamertemplate{items}[default]
}

\usepackage[,UTF8,linespread=1.2]{ctex}
\usepackage{graphicx}
\usepackage{caption}
\captionsetup[figure]{name=图,labelsep=period}
\usepackage{tcolorbox}
\usepackage{xcolor}

\definecolor{xy_blue}{cmyk}{0.6,0.35,0.0,0.4}
\definecolor{xy_orange}{cmyk}{0.0,0.7,1.0,0.0}
\definecolor{xy_green}{cmyk}{0.2,0.0,1.0,0.15}
\xdefinecolor{xy_gold}{RGB}{135,103,79}

\setbeamercolor{section number projected}{fg=red,bg=red!20}
\setbeamercolor{item}{fg=xy_gold}

\usepackage{amsthm}
\newtheorem{question}{问题}
\newtheorem*{solve}{解:}
\newtheorem{exam}{例}

\newtcolorbox{summarybox}[1][]{
  colback=purple!10, colframe=purple!70!black,
  fonttitle=\bfseries, title=#1, arc=1mm,
  boxrule=0pt, drop shadow, left=2mm, right=2mm, top=2mm, bottom=2mm,
}

\AtBeginSection[]{
  \begin{frame}<beamer>
    \frametitle{本节主要内容}
    \tableofcontents[currentsection,currentsubsection]
  \end{frame}
}

\AtBeginDocument{
  \setlength{\abovedisplayskip}{3pt}
  \setlength{\belowdisplayskip}{3pt}
}
"""


def main():
    parser = argparse.ArgumentParser(description="教材截图 → Beamer 课件生成器（图片嵌入版）")
    parser.add_argument("--images", nargs="+", required=True, help="教材截图路径列表")
    parser.add_argument("--title", default="课堂教学课件", help="课件标题")
    parser.add_argument("--output", default="output.tex", help="输出 tex 文件路径")
    parser.add_argument("--scale", type=float, default=0.85, help="图片缩放比例（默认 0.85）")
    args = parser.parse_args()

    # 生成标题
    header = BEAMER_HEADER + f"\n\\title[{args.title}]{{{args.title}}}\n"
    header += r"\author[好好学习，努力向上]{}"
    header += r"\institute{}"
    header += r"\date{\today}"
    header += "\n"

    body = [
        r"\begin{document}",
        r"\begin{frame}{}",
        r"  \titlepage",
        r"\end{frame}",
        "",
        r"\begin{frame}{内容概览}",
        r"  \tableofcontents",
        r"\end{frame}",
        "",
        r"\section{教材内容}",
        "",
    ]

    for i, img_path in enumerate(args.images, 1):
        img_name = os.path.basename(img_path)
        # 复制图片到输出目录的 Figures 子目录
        output_dir = os.path.dirname(os.path.abspath(args.output))
        figures_dir = os.path.join(output_dir, "Figures")
        os.makedirs(figures_dir, exist_ok=True)

        dest_img = os.path.join(figures_dir, img_name)
        if not os.path.exists(dest_img):
            import shutil
            shutil.copy2(img_path, dest_img)

        # 用相对路径引用图片
        rel_path = f"Figures/{img_name}"

        body.append(rf"\begin{{frame}}{{教材截图 {i}}}")
        body.append(rf"  \begin{{figure}}")
        body.append(rf"    \centering")
        body.append(rf"    \includegraphics[scale={args.scale}]{{{rel_path}}}")
        body.append(rf"  \end{{figure}}")
        body.append(rf"\end{{frame}}")
        body.append("")

    body.append(r"\end{document}")

    tex_code = header + "\n".join(body)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(tex_code)

    print(f"[完成] 已生成: {args.output}")
    print(f"  共 {len(args.images)} 页教材图片")
    print(f"  用 xelatex 编译即可得到 PDF")


if __name__ == "__main__":
    main()
