# XyygU.sty 宏包详解

> 本文档逐条解释 `XyygU.sty` 宏包中每个语句的意义和作用，并附用法示例。
> 该宏包是一个 Beamer 自定义主题，用于生成带有学校校徽、特定配色和排版风格的演示文稿。

---

## 目录

1. [模式控制与选项处理](#1-模式控制与选项处理)
2. [外部主题：smoothbars](#2-外部主题smoothbars)
3. [自定义页脚（footline）](#3-自定义页脚footline)
4. [内部主题：circles](#4-内部主题circles)
5. [顶栏修补（headline）](#5-顶栏修补headline)
6. [帧标题与校徽（frametitle）](#6-帧标题与校徽frametitle)
7. [三线表设置（booktabs）](#7-三线表设置booktabs)
8. [颜色定义](#8-颜色定义)
9. [Beamer 颜色与字体设置](#9-beamer-颜色与字体设置)
10. [Block 环境配色](#10-block-环境配色)
11. [Section 自动目录页](#11-section-自动目录页)
12. [其他设置](#12-其他设置)

---

## 1. 模式控制与选项处理

```latex
\mode<presentation>
\newif\ifbeamer@secheader
\beamer@secheaderfalse
\ProcessOptionsBeamer
```

| 语句 | 作用 |
|---|---|
| `\mode<presentation>` | 只在演示模式（即生成PDF时）生效，在article模式下不加载这些设置 |
| `\newif\ifbeamer@secheader` | 定义一个条件开关，控制是否在每个section前显示标题头 |
| `\beamer@secheaderfalse` | 默认关闭该开关 |
| `\ProcessOptionsBeamer` | 处理通过 `\usepackage[选项]{XyygU}` 传入的宏包选项 |

**示例**：如果以后想加选项，可以这样用：
```latex
\usepackage[secheader]{XyygU}  % 传入选项后 \ifbeamer@secheader 为真
```

---

## 2. 外部主题：smoothbars

```latex
\useoutertheme[subsection=false]{smoothbars}
```

| 语句 | 作用 |
|---|---|
| `\useoutertheme[subsection=false]{smoothbars}` | 使用 smoothbars 外部主题，顶部有彩色导航条，显示当前section和subsection；`subsection=false` 表示不显示subsection级别的导航 |

**效果**：页面顶部有一条彩色横条，显示当前章节名称，当前章节高亮，其他章节半透明。

---

## 3. 自定义页脚（footline）

```latex
\newcommand{\frameofframes}{/}
\newcommand{\setframeofframes}[1]{\renewcommand{\frameofframes}{#1}}
```

| 语句 | 作用 |
|---|---|
| `\newcommand{\frameofframes}{/}` | 定义帧号分隔符，默认显示为 "3 / 15" 中的 "/" |
| `\setframeofframes{#1}` | 允许用户自定义分隔符，比如改成 "·" 或 "of" |

**用法示例**：
```latex
\setframeofframes{·}  % 显示为 "3 · 15"
```

```latex
\setbeamertemplate{footline}{%
  \begin{beamercolorbox}[colsep=1.5pt]{upper separation line foot}
  \end{beamercolorbox}
  \begin{beamercolorbox}[ht=2.5ex,dp=1ex,
    leftskip=.3cm,rightskip=.3cm plus1fil]{author in head/foot}%
    {\usebeamerfont{author in head/foot}\insertshortauthor}%
    \hfill%
    {\usebeamerfont{title in head/foot}\insertshorttitle}%
    \hfill%
    {\usebeamerfont{frame number}\usebeamercolor[fg]{frame number}%
      \insertframenumber~\frameofframes~\inserttotalframenumber}
  \end{beamercolorbox}%
  \begin{beamercolorbox}[colsep=1.5pt]{lower separation line foot}
  \end{beamercolorbox}
}
```

| 语句 | 作用 |
|---|---|
| `upper separation line foot` | 页脚上方的分隔线（1.5pt间距） |
| `ht=2.5ex,dp=1ex` | 页脚高度和深度 |
| `leftskip=.3cm` | 左边距 |
| `rightskip=.3cm plus1fil` | 右边距，允许弹性拉伸 |
| `\insertshortauthor` | 显示短作者名 |
| `\hfill` | 左右弹性对齐 |
| `\insertshorttitle` | 显示短标题 |
| `\insertframenumber` / `\inserttotalframenumber` | 当前帧号 / 总帧号 |
| `lower separation line foot` | 页脚下方的分隔线 |

**效果**：页脚从左到右依次是：作者名、短标题、"当前帧/总帧"。

---

## 4. 内部主题：circles

```latex
\useinnertheme{circles}
```

| 语句 | 作用 |
|---|---|
| `\useinnertheme{circles}` | 使用圆形项目符号主题，itemize的每个条目前面显示小圆点 |

**可选的其他内部主题**（已注释掉）：
- `rectangles`：方形项目符号
- `rounded`：圆角矩形，带阴影

---

## 5. 顶栏修补（headline）

```latex
\newlength{\xyyg@headheight}
\newlength{\xyyg@titleht}
\newlength{\xyyg@titledp}
\newlength{\xyyg@logoheight}
\newlength{\xyyg@logowidth}
\newlength{\xyyg@logoyshift}
```

| 语句 | 作用 |
|---|---|
| `\newlength{...}` | 定义多个长度变量，用于存储顶栏高度、标题高度、校徽尺寸等 |

```latex
\setbeamercolor{section in head/foot}{bg=xyyg,fg=white}
\setbeamercolor{section in head/foot shaded}{bg=xyyg,fg=white!55!xyyg}
```

| 语句 | 作用 |
|---|---|
| `section in head/foot` | 顶栏中当前section的背景色（校红色）和前景色（白色） |
| `section in head/foot shaded` | 非当前section的颜色（55%白色混合校红） |

```latex
\AtBeginDocument{\global\xyyg@headheight=11.6pt}
\setbeamertemplate{headline}{%
  \begin{beamercolorbox}[wd=\paperwidth,colsep=0pt,
    ht=\xyyg@headheight,dp=0ex,vmode]{section in head/foot}%
    \vbox to \xyyg@headheight{%
      {\vskip0.52pt}%
      \insertnavigation{\paperwidth}%
      \vss}%
  \end{beamercolorbox}%
}
```

| 语句 | 作用 |
|---|---|
| `\AtBeginDocument{...}` | 文档开始时设置顶栏高度为11.6pt（像素校准值） |
| `\setbeamertemplate{headline}` | 自定义顶栏模板 |
| `wd=\paperwidth` | 顶栏宽度等于页面宽度 |
| `ht=\xyyg@headheight` | 顶栏高度固定为11.6pt |
| `\insertnavigation{\paperwidth}` | 插入导航条（显示章节名） |
| `\vskip0.52pt` | 顶部微调间距 |
| `\vss` | 弹性垂直居中 |

**为什么要修补？**
原版smoothbars主题：
1. 顶栏和标题条之间有模糊渐变过渡（不好看）
2. 无标题的section页顶栏会更高（不一致）
3. 颜色继承自更暗的palette quaternary（不统一）

修补后：顶栏高度固定11.6pt，颜色统一为校红色。

---

## 6. 帧标题与校徽（frametitle）

```latex
\setbeamertemplate{frametitle}{%
  \nointerlineskip
  \usebeamerfont*{frametitle}%
  \settoheight{\xyyg@titleht}{\insertframetitle}%
  \settodepth{\xyyg@titledp}{\insertframetitle}%
  \xyyg@logoheight=\dimexpr\xyyg@titleht+\xyyg@titledp\relax
  \settowidth{\xyyg@logowidth}{\includegraphics[height=\xyyg@logoheight]{Figures/xyyg-emblem-names.png}}%
  \begin{beamercolorbox}[wd=\paperwidth,sep=0.3cm,
    rightskip=\dimexpr\xyyg@logowidth+0.4cm\relax]{frametitle}%
    \strut\insertframetitle
    \ifx\insertframesubtitle\@empty\else
      \par{\usebeamerfont*{framesubtitle}\usebeamercolor[fg]{framesubtitle}%
        \strut\insertframesubtitle}%
    \fi
  \end{beamercolorbox}%
  ...
}
```

| 语句 | 作用 |
|---|---|
| `\nointerlineskip` | 标题上方不留额外间距 |
| `\settoheight{...}{\insertframetitle}` | 测量标题文字的高度 |
| `\settodepth{...}{\insertframetitle}` | 测量标题文字的深度（下伸部分） |
| `\xyyg@logoheight=\dimexpr...` | 校徽高度 = 标题高度 + 标题深度 |
| `\settowidth{...}` | 测量校徽图片的宽度 |
| `rightskip=...logowidth+0.4cm` | 标题右侧留出校徽宽度+0.4cm的间距，避免文字被校徽盖住 |
| `\strut\insertframetitle` | 插入标题文字（用strut保证基线一致） |
| `\ifx\insertframesubtitle\@empty\else` | 如果有副标题，换行显示副标题 |

```latex
\begin{tikzpicture}[remember picture,overlay]
  \node[anchor=north east,inner sep=0pt]
    at ([yshift=-\xyyg@logoyshift,xshift=-0.3cm]current page.north east)
    {\includegraphics[height=\xyyg@logoheight]{Figures/xyyg-emblem-names.png}};
\end{tikzpicture}
```

| 语句 | 作用 |
|---|---|
| `remember picture,overlay` | 记住页面坐标，覆盖模式绘制（不占版面空间） |
| `anchor=north east` | 校徽的右上角锚定 |
| `current page.north east` | 以页面右上角为基准点 |
| `yshift=-\xyyg@logoyshift` | 垂直偏移，使校徽与标题文字顶部对齐 |
| `xshift=-0.3cm` | 水平偏移，距右边0.3cm |

**效果**：右上角自动显示校徽，高度自动与标题文字一致，无需手动调整。

---

## 7. 三线表设置（booktabs）

```latex
\AtEndPreamble{\@ifpackageloaded{booktabs}{%
  \setlength{\heavyrulewidth}{1.2pt}%
  \setlength{\lightrulewidth}{0.5pt}%
}{}}
```

| 语句 | 作用 |
|---|---|
| `\AtEndPreamble` | 导言区末尾才执行（因为booktabs可能在后面才加载） |
| `\@ifpackageloaded{booktabs}` | 检查是否加载了booktabs包 |
| `\heavyrulewidth=1.2pt` | 三线表的顶线和底线（粗线）设为1.2pt |
| `\lightrulewidth=0.5pt` | 表头下方的中线（细线）设为0.5pt |

**效果**：表格的顶线、底线粗，表头线细，层次分明。

---

## 8. 颜色定义

```latex
\xdefinecolor{xyyg}{cmyk}{0,1,1,0.45}
\xdefinecolor{xyyg_gold}{cmyk}{0,0.35,0.75,0.05}
\xdefinecolor{xyyg_blue}{cmyk}{0.6,0.35,0.0,0.4}
\xdefinecolor{xyyg_darkblue}{cmyk}{1.0,0.6,0.0,0.5}
\xdefinecolor{xyyg_gray}{cmyk}{0.0,0.0,0.08,0.55}
\xdefinecolor{xyyg_dirt}{cmyk}{0.0,0.2,0.35,0.3}
\xdefinecolor{xyyg_orange}{cmyk}{0.0,0.7,1.0,0.0}
\xdefinecolor{xyyg_green}{cmyk}{0.2,0.0,1.0,0.15}
\xdefinecolor{xyyg_darkgreen}{cmyk}{0.6,0.5,1.0,0.45}
\xdefinecolor{pantone_gold}{RGB}{135,103,79}
\xdefinecolor{pantone_silver}{RGB}{138,141,143}
\xdefinecolor{WM_Gold}{cmyk}{0.09,0.29,0.66,0.24}
```

| 颜色名 | 用途 |
|---|---|
| `xyyg` | 主色（校红色），用于顶栏、页脚、标题、结构元素 |
| `xyyg_gold` | 金色，用于强调 |
| `xyyg_blue` | 蓝色，用于definition块的标题 |
| `xyyg_darkblue` | 深蓝色 |
| `xyyg_gray` | 灰色 |
| `xyyg_dirt` | 土黄色 |
| `xyyg_orange` | 橙色，用于theorem块的标题 |
| `xyyg_green` | 浅绿色 |
| `xyyg_darkgreen` | 深绿色 |
| `pantone_gold` | 潘通金色，用于example块 |
| `pantone_silver` | 潘通银色 |
| `WM_Gold` | 另一种金色 |

**用法示例**：
```latex
\textcolor{xyyg}{这段文字是校红色}
\colorbox{xyyg_gold!20}{这段文字背景是浅金色}
```

---

## 9. Beamer 颜色与字体设置

```latex
\setbeamercolor{footline}{bg=xyyg}
\setbeamercolor{frametitle}{bg=white,fg=xyyg}
\setbeamercolor{title}{bg=xyyg}
\setbeamerfont{frametitle}{series=\bfseries,size=\large}
\setbeamerfont{footline}{series=\bfseries}
```

| 语句 | 作用 |
|---|---|
| `footline bg=xyyg` | 页脚背景为校红色 |
| `frametitle bg=white, fg=xyyg` | 帧标题背景白色，文字校红色 |
| `title bg=xyyg` | 标题页背景校红色 |
| `frametitle series=\bfseries` | 帧标题加粗，字号large |
| `footline series=\bfseries` | 页脚文字加粗 |

```latex
\setbeamertemplate{bibliography item}[text]
\setbeamertemplate{caption}[numbered]
```

| 语句 | 作用 |
|---|---|
| `bibliography item [text]` | 参考文献条目用文本样式（不用图标） |
| `caption [numbered]` | 图表标题自动编号 |

```latex
\beamertemplateshadingbackground{white!5}{white}
```

| 语句 | 作用 |
|---|---|
| `shadingbackground` | 页面背景从上到下渐变：5%灰色 → 纯白 |

```latex
\setbeamercolor{palette primary}{use=structure,fg=white,bg=structure.fg}
\setbeamercolor{palette secondary}{use=structure,fg=white,bg=structure.fg!95!black}
\setbeamercolor{palette tertiary}{use=structure,fg=white,bg=structure.fg!90!black}
\setbeamercolor{palette quaternary}{fg=white,bg=structure.fg!85!black}
\setbeamercolor{titlelike}{parent=palette primary}
```

| 语句 | 作用 |
|---|---|
| `palette primary` | 主调色板（当前section、标题等）：白字校红底 |
| `palette secondary` | 次调色板：95%校红+5%黑（更深一点） |
| `palette tertiary` | 第三调色板：90%校红+10%黑 |
| `palette quaternary` | 第四调色板：85%校红+15%黑 |
| `titlelike` | 所有标题类元素继承palette primary的颜色 |

```latex
\setbeamercolor{structure}{fg=xyyg}
```

| 语句 | 作用 |
|---|---|
| `structure fg=xyyg` | 所有结构元素（项目符号、线段、图标等）的前景色设为校红色 |

---

## 10. Block 环境配色

```latex
\setbeamercolor{block title}{bg=xyyg_blue,fg=white}
\setbeamercolor{block body}{bg=xyyg_blue!10}
```

| 语句 | 作用 |
|---|---|
| `block title` | 普通block标题：蓝底白字 |
| `block body` | 普通block正文：10%浅蓝背景 |

```latex
\BeforeBeginEnvironment{definition}{%
  \setbeamercolor{block title}{bg=xyyg_blue,fg=white}
  \setbeamercolor{block body}{bg=xyyg_blue!10}
}
\AfterEndEnvironment{definition}{%
  \setbeamercolor{block title}{bg=xyyg_blue,fg=white}
  \setbeamercolor{block body}{bg=xyyg_blue!10}
}
```

| 语句 | 作用 |
|---|---|
| `BeforeBeginEnvironment{definition}` | definition环境开始前，强制设置为蓝色块 |
| `AfterEndEnvironment{definition}` | definition环境结束后，恢复为蓝色块 |

**效果**：`\begin{definition}...\end{definition}` 显示为蓝色标题块。

```latex
\BeforeBeginEnvironment{theorem}{%
  \setbeamercolor{block title}{bg=xyyg_orange,fg=white}
  \setbeamercolor{block body}{bg=xyyg_orange!10}
}
\AfterEndEnvironment{theorem}{%
  \setbeamercolor{block title}{bg=xyyg_blue,fg=white}
  \setbeamercolor{block body}{bg=xyyg_blue!10}
}
```

| 语句 | 作用 |
|---|---|
| `BeforeBeginEnvironment{theorem}` | theorem环境开始前，设置为橙色块 |
| `AfterEndEnvironment{theorem}` | theorem环境结束后，恢复为蓝色块 |

**效果**：定理用橙色块，定义用蓝色块，视觉上区分不同类型的内容。

**同样的逻辑也用于proposition环境**（命题也用橙色块）。

```latex
\setbeamercolor*{block title example}{use={normal text,example text},
  bg=white!70!pantone_gold,fg=xyyg}
```

| 语句 | 作用 |
|---|---|
| `block title example` | example环境的标题：70%白+30%金色背景，校红色文字 |

---

## 11. Section 自动目录页

```latex
\AtBeginSection[]{
  \begin{frame}
    \tableofcontents[sectionstyle=show/shaded,
      subsectionstyle=hide,subsubsectionstyle=hide]
  \end{frame}
}
```

| 语句 | 作用 |
|---|---|
| `\AtBeginSection[]{...}` | 每个新section开始前，自动插入一个frame |
| `sectionstyle=show/shaded` | 目录中当前section高亮显示，其他section半透明 |
| `subsectionstyle=hide` | 不显示subsection级别 |
| `subsubsectionstyle=hide` | 不显示subsubsection级别 |

**效果**：每开始一个新章节，自动显示目录页，当前章节高亮。

---

## 12. 其他设置

```latex
\setbeamercolor{fine separation line}{}
\setbeamercolor{item projected}{fg=white}
\setbeamercolor{palette sidebar primary}{use=normal text,fg=normal text.fg}
\setbeamercolor{palette sidebar quaternary}{use=structure,fg=structure.fg}
\setbeamercolor{palette sidebar secondary}{use=structure,fg=structure.fg}
\setbeamercolor{palette sidebar tertiary}{use=normal text,fg=normal text.fg}
\setbeamercolor{section in sidebar}{fg=brown}
\setbeamercolor{section in sidebar shaded}{fg=grey}
\setbeamercolor{separation line}{}
\setbeamercolor{sidebar}{bg=xyyg}
\setbeamercolor{sidebar}{parent=palette primary}
\setbeamercolor{subsection in sidebar}{fg=brown}
\setbeamercolor{subsection in sidebar shaded}{fg=grey}
```

| 语句 | 作用 |
|---|---|
| `fine separation line` | 精细分隔线（设为空，即不显示） |
| `item projected` | 投影模式下的item文字为白色 |
| `sidebar` 系列 | 侧边栏相关配色（如果用了带侧边栏的主题） |
| `section in sidebar` | 侧边栏中section标题为棕色 |
| `section in sidebar shaded` | 非当前section为灰色 |

```latex
\setbeamercolor{postgreen}{fg=black,bg=example text.fg!75!black!10!bg}
\setbeamercolor{postred}{fg=black,bg=white!70!pantone_gold}
\setbeamercolor{postblue}{fg=black,bg=xyyg_blue!10}
```

| 语句 | 作用 |
|---|---|
| `postgreen` | 自定义绿色块颜色 |
| `postred` | 自定义红色块颜色（金色背景） |
| `postblue` | 自定义蓝色块颜色（浅蓝背景） |

**用法示例**：
```latex
\begin{beamercolorbox}[colsep=2pt]{postblue}
这是一个蓝色背景的提示框
\end{beamercolorbox}
```

```latex
\mode<all>
```

| 语句 | 作用 |
|---|---|
| `\mode<all>` | 恢复所有模式（结束presentation模式限制） |

---

## 附：完整使用流程

```latex
\documentclass[10pt,aspectratio=169,serif]{beamer}

% 1. 加载宏包
\usepackage[fontset=none,scheme=plain]{ctex}
\usepackage{XyygU}

% 2. 标题信息
\title[短标题]{完整标题}
\subtitle{副标题}
\author[短作者名]{作者全名}
\institute{单位}
\date{\today}

\begin{document}

% 3. 标题页（自动使用校红色背景）
\begin{frame}
  \titlepage
\end{frame}

% 4. 正文帧（右上角自动显示校徽）
\begin{frame}{帧标题}
  正文内容
\end{frame}

\end{document}
```

---

## 附：需要准备的资源文件

| 文件 | 位置 | 用途 |
|---|---|---|
| `Figures/xyyg-emblem-names.png` | `Figures/` 目录下 | 右上角校徽图片 |

**注意**：如果没有校徽图片，需要注释掉 frametitle 中关于校徽的 tikzpicture 代码块，否则会编译报错。
