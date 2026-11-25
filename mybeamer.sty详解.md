# mybeamer.sty 宏包详解与修订建议

> 对象文件：`D:\beamer-math\必修一第二章课件\mybeamer.sty`（与 `D:\beamer-math\mybeamer.sty` 完全相同，SHA256 一致）
> 全文 140 行，本文逐段解释其作用、指出问题并给出修改方案；文末说明新版 `mybeamer2.sty` 的用法与迁移方法。
> 本文所有"实测"结论均来自 TeX Live 2026 + XeLaTeX 的实际编译与 PDF 坐标测量。

---

## 0. 一句话结论

这份文件本质上是把 `模板1.tex` 里第 3—127 行的导言区"固化"成了一个 Beamer 主题包：四套内置主题打底（smoothbars / serif / circles / spruce），再用校红色 `xyyg` 系列重新染色，另加自定义的页眉导航条、页脚三色带和帧标题条。

整体可用、观感稳定，主要问题不在"能不能用"，而在**健壮性与可维护性**：缺包元数据、字体没有回退、alert 块配色对比度极低、`caption`/`parskip` 与 beamer 自身机制重叠、页脚跟帧标题靠魔数与逐帧测量、主题设置之间互相覆盖。这些问题在换机器、换字号或改配色时就会暴露。

---

## 1. 文件定位与加载方式

| 项目 | 内容 |
|---|---|
| 文件类型 | Beamer 主题宏包（`\mode<presentation>` 包裹的自定义 theme） |
| 依赖文档类 | `ctexbeamer`（或 `beamer` + `ctex`）；必须 XeLaTeX，因为用了 `\setCJKmainfont` |
| 典型加载 | `\documentclass[10pt,aspectratio=169,t]{ctexbeamer}` 后 `\usepackage{mybeamer}` |
| 覆盖内容 | 外观主题、宏包依赖、中文字体、调色板、页眉、页脚、帧标题、块配色、列表符号 |
| 未做的事 | 没有 `\ProvidesPackage`、没有版本号、没有对外选项、没有对外接口命令 |

这份包与文件夹里的 `模板.tex`、`模板1.tex` 是"三胞胎"：`模板1.tex` 就是把本文件的内容内联写进了 `.tex`。改样式时若同时改这两处，很容易漏改一处。

---

## 2. 逐段详解

### 2.1 第 1—3 行：模式控制与选项处理

```latex
\mode<presentation>
\ProcessOptionsBeamer
```

| 语句 | 作用 |
|---|---|
| `\mode<presentation>` | 以下设置只在演示模式生效；配合文末 `\mode<all>` 构成一个"模式块" |
| `\ProcessOptionsBeamer` | 处理 `\usepackage[选项]{mybeamer}` 传进来的选项 |

**要点（两个坑）**

1. 全文**没有任何 `\DeclareOptionBeamer`**，所以 `\ProcessOptionsBeamer` 是空转，这行删掉功能上也不变。想加选项就必须补声明。
2. `\ProcessOptionsBeamer` 不是 LaTeX 的 `\ProcessOptions`：查看 `beamerbaseoptions.sty` 可见它只是 `\setkeys` + `\AtEndOfPackage{\let\@unprocessedoptions\relax}`，**不负责关闭 LaTeX 的"选项段"状态**。因此一旦在本包内混用 plain 的 `\DeclareOption*`，后面的 `\useoutertheme`（内部要 `\RequirePackage` 主题文件）就会报
   `! LaTeX Error: \RequirePackage or \LoadClass in Options Section.` —— 这个错误我在开发新版时实际踩过一次，值得记住。

另外缺 `\NeedsTeXFormat{LaTeX2e}` 和 `\ProvidesPackage{mybeamer}`，包没有身份与日期信息，出问题很难定位版本。

### 2.2 第 4—7 行：四套内置主题

```latex
\useoutertheme[subsection=false]{smoothbars}
\usefonttheme[stillsansseriflarge]{serif}
\useinnertheme{circles}
\usecolortheme{spruce}
```

| 语句 | 作用 | 备注 |
|---|---|---|
| `\useoutertheme[subsection=false]{smoothbars}` | 顶部章节导航条，只显示 section 不显示 subsection | 后面第 82 行又自写了一遍 `headline`，把它的导航条"接管"了 |
| `\usefonttheme[stillsansseriflarge]{serif}` | 正文用衬线体；`stillsansseriflarge` 让"大号字"（如帧标题）仍用无衬线 | 与思源宋体/黑体配合：正文宋、标题黑 |
| `\useinnertheme{circles}` | 项目符号与目录用圆环 | **被第 134—135 行覆盖**：itemize 改成 `ball`（立体小球）、enumerate 改成 `default`，所以 circles 的列表样式实际没有生效，只剩 toc/章节编号的圆 |
| `\usecolortheme{spruce}` | 墨绿系配色主题 | 随后第 114 行把 `structure` 改成校红，所以 spruce 只剩"骨架"作用 |

**要点**：`circles` 与后面的 `[ball]`、`[default]` 是自相矛盾的两种设计意图。实测旧版 PDF 的项目符号是立体小球（ball），并非圆环。

### 2.3 第 9—35 行：宏包依赖

| 行 | 宏包 | 用途 | 问题 |
|---|---|---|---|
| 9 | `hyperref` | 超链接 | beamer 文档类已自动加载，重复加载多余；要改链接样式应用 `\hypersetup` |
| 10 | `multicol` | 分栏 | frame 内建议改 `columns` 环境，multicol 与 beamer 的帧盒子配合脆弱 |
| 11 | `calligra` | 西文手写体 | 仅拉丁字母，注释写"手写体"容易误以为有中文手写体 |
| 12 | `tikz` | 绘图 | 正常 |
| 13 | `bm` | 数学粗体 | 正常 |
| 14 | `amsfonts` | 数学字体 | `amssymb` 已包含，重复 |
| 15 | `ragged2e` | 提供 `\justifying` | 正常（第 19 行要用） |
| 16 | `parskip` | 段间距、取消首行缩进 | **与 beamer 的段距机制冲突**，会让块、列表、帧内容的垂直节奏变松，且不随字号缩放 |
| 17 | `graphicx` | 插图 | 第 23 行又加载一次，重复 |
| 18 | `wrapfig` | 图文绕排 | frame 内需要 `\parshape`，极易错位，慎用 |
| 19 | `\apptocmd{\frame}{}{\justifying}{}` | 见 2.4 | 脆弱 |
| 20 | `amsmath,amssymb` | 数学 | 正常 |
| 21—25 | `tabularx,booktabs,multirow,colortbl` | 表格四件套 | 正常；`colortbl` 需与 `xcolor` 的 table 选项配合，目前能用 |
| 26—28 | `caption` + `\captionsetup[figure]{name=图}` + `\setbeamertemplate{caption}[numbered]` | 图注 | **`caption` 包与 beamer 自带的 caption 模板体系重叠**；而且 ctex 已把 `\figurename` 设为"图"，这行其实多余。真正需要的是 `\setbeamertemplate{caption}[numbered]` |
| 29 | `\linespread{1.2}` | 全文行距 | 正常；但在包里执行会强制所有使用者接受 1.2，无法按文档调整 |
| 30—31 | `pgfplots` + `compat=1.18` | 函数图象 | 正常 |
| 32 | `\setbeamertemplate{theorems}[numbered]` | 定理统一编号 | 编号是**全局连续**，不按节重置；若想"2.1、2.2"式编号需另配 |
| 33—34 | `xcolor`、`tcolorbox[most]` | 颜色、色框 | `most` 会连带加载 listings/raster 等一大堆库，编译略慢；按需加载更轻 |
| 35 | `\usetikzlibrary{arrows.meta,positioning,calc}` | TikZ 库 | 正常 |

### 2.4 第 19 行：两端对齐补丁

```latex
\apptocmd{\frame}{}{\justifying}{}
```

`\apptocmd` 把 `\justifying` 追加到 `\frame` 宏定义体的末尾。**这个补丁是有效的**——我用 `pdftotext -bbox-layout` 测量过：旧版正文每一行（除末行）行末 x 坐标完全一致（425.186pt），确实是两端对齐。

它之所以有效，靠的是 beamer 的一个实现细节：帧内段落不是在写入时断行，而是等到帧结束才统一断行，所以帧末追加的 `\justifying` 还来得及影响对齐方式。

**隐患**：

- 完全依赖 beamer 内部实现，beamer 若改动帧处理，这会静默失效（不报错，只是变回左对齐）；
- 对溢出/超宽内容（`\hbox` 溢出）不起作用；
- 与帧内自己写的 `\raggedright`、`\begin{columns}`、表格 `p{}` 列等会互相覆盖；
- 在 `beamerarticle` 讲义模式下 `\frame` 不存在，`\apptocmd` 会失败。

**更稳的做法**：直接把 beamer 用的对齐命令换掉，段落断行时就已是两端对齐，不依赖帧的收尾时机：

```latex
\renewcommand{\raggedright}{\justifying}
```

我实测这一行与原版补丁的排版结果**完全一致**（每行行末 x 都是 425.186pt，正文起点也相同），新版采用此法。

### 2.5 第 38—40 行：中文字体

```latex
\setCJKmainfont{Source Han Serif SC}[BoldFont={Source Han Serif SC Bold}]
\setCJKsansfont{Source Han Sans SC}[BoldFont={Source Han Sans SC Bold}]
```

| 语句 | 作用 |
|---|---|
| `\setCJKmainfont` | 正文（衬线）中文 = 思源宋体，粗体指定为 `Source Han Serif SC Bold` |
| `\setCJKsansfont` | 无衬线中文 = 思源黑体，供标题、块标题等使用 |

**要点**

1. 这两个命令由 `xeCJK` 提供（`ctex`/`ctexbeamer` 会自动加载）。若用纯 `beamer` 而又没 `\usepackage{ctex}`，这里会报 `Undefined control sequence`。
2. **没有存在性检查**：换到没装思源字体的机器（如学校的旧电脑、Overleaf）就是一行大红错误。建议用 `\IfFontExistsTF` 加回退，或在包内 `\PackageWarning` 提示。
3. 显式 `BoldFont=...Bold` 在 Windows 字体族下能解析（实测日志里有 `Font family 'SourceHanSerifSC(0)' created`），但斜体没有对应字形，日志会出现 "Could not resolve font ... /I" 的信息性提示，属正常现象。
4. 只设了 main 与 sans，没设 `\setCJKmonofont`；若课件里用等宽中文（如代码演示）会落到默认字体，字形不一致。

### 2.6 第 42—55 行：调色板

| 颜色 | 定义 | 是否被使用 |
|---|---|---|
| `xyyg` | cmyk(0,1,1,0.45) | **主色**，用于标题条、导航条、页脚、块标题、structure |
| `xyyg_gold` | cmyk(0,0.35,0.75,0.05) | 仅作备用色（模板示例页出现） |
| `xyyg_blue` | cmyk(0.6,0.35,0,0.4) | 仅示例/图形用 |
| `xyyg_darkblue` | cmyk(1,0.6,0,0.5) | 仅示例 |
| `xyyg_gray` | cmyk(0,0,0.08,0.55) | 仅示例 |
| `xyyg_dirt` | cmyk(0,0.2,0.35,0.3) | 仅示例 |
| `xyyg_orange` | cmyk(0,0.7,1,0) | 参与页脚中段 `xyyg!60!xyyg_orange` |
| `xyyg_green` | cmyk(0.2,0,1,0.15) | 示例/块备用 |
| `xyyg_darkgreen` | cmyk(0.6,0.5,1,0.45) | 模板里页脚中段曾用它，包内已改成 orange |
| `pantone_gold` / `pantone_silver` | RGB | 仅示例 |
| `WM_Gold` | cmyk | 仅示例 |
| `accent` | RGB(196,60,50) | 用于 `alerted text`（第 119 行），但块标题没用到 |
| `dotpink` | RGB(214,60,120) | **完全未被使用** |

（新版把这套 CMYK 值逐色换算成屏幕实测 RGB，并另存一份原始 CMYK 供 `print` 模式使用；对照表见 5.6 与附 A。）

**要点**

- CMYK 与 RGB 混用：`xyyg` 是印刷色 CMYK，`accent`/`dotpink` 是屏幕色 RGB。同一份 PPT 投屏与打印会看到两种红——而且因为 XeLaTeX 把 cmyk 原样写进 PDF、由播放器现算，屏幕上的红还会随播放器变化。建议统一到一种色空间：新版默认 RGB（屏幕）、`print` 选项切 CMYK（印刷），理由与实测数据见 5.6 节。
- 颜色定义写在了 `\mode<presentation>` **里面**，所以在 `beamerarticle`/article 讲义模式下这些颜色根本不存在，正文里一旦 `\textcolor{xyyg}{...}` 就会报 `Undefined color`（原版在 article 模式实测正是这个错）。

### 2.7 第 57—75 行：页脚 footline

```latex
\setbeamertemplate{footline}{%
  \leavevmode
  \hbox{%
    \begin{beamercolorbox}[wd=0.3\paperwidth,...]{footleft}  \insertshortauthor \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=0.5\paperwidth,...]{footmid}   \insertshorttitle \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=0.2\paperwidth,...]{footright} \insertframenumber~/~\inserttotalframenumber \end{beamercolorbox}%
  }%
  \vskip0pt
}
```

| 参数 | 作用 |
|---|---|
| `\leavevmode` | 强制进入水平模式，避免“垂直模式下起盒”报错 |
| `wd=0.3/0.5/0.2\paperwidth` | 左作者 / 中标题 / 右页码，三段宽度合计正好 1.0 |
| `ht=2.5ex, dp=1ex` | 页脚条高度与下伸量 |
| `leftskip=.3cm` / `rightskip=.3cm` / `center` / `right` | 三段内部的对齐与边距 |
| `\insertshortauthor` / `\insertshorttitle` | 取 `\author[短]{长}`、`\title[短]{长}` 的短版本 |
| `\insertframenumber~/~\inserttotalframenumber` | 当前页 / 总页数；总页数靠 `.aux` 传递，**必须编译两次** |
| `\vskip0pt` | 消除底部多余空白 |

**要点**

1. **总宽恰好 100%，没有余量**。三段都是定宽盒，TeX 里 0.3+0.5+0.2 的舍入误差可能让整体超出一个盒宽，触发 `Overfull \hbox` 并在页边露一条白缝。建议改成 `\hbox to\paperwidth{... \hss}`，末尾加零宽可收缩胶兜底，或把比例改成 0.30/0.45/0.25 留点余地（新版用后者 + `\hss`）。
2. 页脚颜色是后定义的（第 121—123 行），模板里先引用没问题，因为颜色在 shipout 时才求值；但"模板在前、颜色在后"的写法读起来很别扭。
3. **标题页也显示 `1 / 4`**。多数教师希望封面不出现页码，可以考虑加开关（新版默认隐藏，`firstpagenumber` 选项可恢复）。
4. `\insertshortauthor` 为空时（`\author[]{...}`）左侧是一条空色带，视觉上会显得"缺一块"。
5. **三段文字的对齐方式各不相同**：左边顶格（`leftskip=.3cm`）、中间居中、右边贴右（`rightskip=.3cm`），视觉重心偏斜；想统一成居中，做法见 4.5 与 5.7。
6. **字号偏小**：页脚文字只有 7pt 左右（`\scriptsize` 级别），投影到大屏上几乎看不清；放大到 `\small` 需要同时加高色条，见 4.5。

### 2.8 第 77—89 行：页眉 headline

```latex
\newlength{\beamerheadheight}
...
\AtBeginDocument{\global\beamerheadheight=11.6pt}
\setbeamertemplate{headline}{%
  \begin{beamercolorbox}[wd=\paperwidth,colsep=0pt,ht=\beamerheadheight,dp=0.5ex,vmode]{section in head/foot}%
    \vbox to \beamerheadheight{\vskip0.52pt \insertnavigation{\paperwidth}\vss}%
  \end{beamercolorbox}%
}
```

| 语句 | 作用 | 问题 |
|---|---|---|
| `\newlength{\beamerheadheight}` 等 | 定义长度变量 | 名字没有前缀，`\beamerheadheight` 很容易与别的包重名；`\beamertitleht`/`\beamertitledp` 在本文件里其实没被用到（见 2.9） |
| `\AtBeginDocument{\global\beamerheadheight=11.6pt}` | 文档开始时把导航条高度定死 11.6pt | `\global` 对长度赋值毫无意义；用不着 `\AtBeginDocument`；11.6pt 是"10pt 字号 + 16:9"下的校准魔数，换 12pt 或 4:3 就会错位 |
| `ht=\beamerheadheight, dp=0.5ex` | 色盒高度 = 11.6pt，再额外留 0.5ex 下伸 | 内层 `\vbox to \beamerheadheight` 已经把内容撑满，外面还多出 0.5ex 的**纯色空白**，导航条看起来比内容厚一点 |
| `\vskip0.52pt` + `\vss` | 顶部微调 + 底部弹性 | 0.52pt 又是魔数；上下不对称的微调在改字号时会露馅 |
| `\insertnavigation{\paperwidth}` | 画章节导航条 | 正常；无 `\section` 的文档里会是一条空红条 |

### 2.9 第 90—101 行：帧标题 frametitle

```latex
\setbeamertemplate{frametitle}{%
  \nointerlineskip
  \usebeamerfont*{frametitle}%
  \settoheight{\beamertitleht}{\insertframetitle}%
  \settodepth{\beamertitledp}{\insertframetitle}%
  \begin{beamercolorbox}[wd=\paperwidth,sep=0ex,ht=1em,
      dp=\dimexpr\beamertitledp+2pt,rightskip=2em,leftskip=0.5em\relax]{frametitle}%
    \usebeamercolor{frametitle}\strut\insertframetitle
  \end{beamercolorbox}%
}
```

| 语句 | 作用 | 问题 |
|---|---|---|
| `\nointerlineskip` | 标题条紧贴页眉，不留行距 | 正常 |
| `\usebeamerfont*{frametitle}` | 套用 frametitle 字体（随字号、`boldtitle` 等） | 正常 |
| `\settoheight{\beamertitleht}{...}` | 测量标题高度 | **测量结果从未被使用 → 死代码** |
| `\settodepth{\beamertitledp}{...}` | 测量标题深度 | 用于 dp，导致**每帧标题条高度随标题内容变化**：同一册课件里，标题含括号或字母 `g` 的那一帧，正文会比别的帧低 2—3pt，翻页时能看出来"跳一下" |
| `ht=1em` | 高度取标题字体的 1em | 合理（随字号缩放），但与上面测到的高度无关 |
| `dp=...\beamertitledp+2pt` | 深度 = 实测深度 + 2pt | 同上，逐帧变化 |
| `rightskip=2em, leftskip=0.5em` | 右侧留 2em 防止标题顶到边，左侧 0.5em 留白 | 正常；但标题若换行，色盒高度不增加，第二行会压到正文 |
| `\usebeamercolor{frametitle}` | 再次把颜色设为 frametitle 的颜色 | 盒内本来就是该颜色，**冗余** |

### 2.10 第 114—135 行：颜色绑定与块配色

| 语句 | 作用 | 备注 |
|---|---|---|
| `\setbeamercolor{structure}{fg=xyyg}` | 全局强调色（列表编号、圆球、定理标题等） | 覆盖了 spruce 的蓝色 |
| `\setbeamercolor{frametitle}{bg=white,fg=xyyg}` | 帧标题白底红字 | 正常 |
| `\setbeamercolor{title}{bg=xyyg,fg=white}` | 标题页主标题红底白字 | 正常 |
| `\setbeamercolor{section in head/foot}` / `...shaded` | 导航条当前节/其它节 | 两者背景色相同，只靠文字透明度区分，视觉上"当前节"不够突出 |
| `\setbeamercolor{alerted text}{fg=accent}` | `\alert{}` 文字用强调红 | 与主色的红接近，区分度有限 |
| `footleft/footmid/footright` | 页脚三段配色 | 中段 `xyyg!60!xyyg_orange` 偏亮，与左右两段深红形成"夹心" |
| `block title` / `block body` | 普通块：深红标题 + 10% 浅红底 | 正常 |
| `block title alerted` | `structure.fg!80` | 与普通块同色系，**alert 块看不出是 alert** |
| `block body alerted` | `fg=black, bg=structure!90` | **黑字压在 90% 深红底上，几乎看不清**（实测截图对比明显）；模板文件里写的是 `structure!10`，包内是 `structure!90`，两处不一致，包里的写法应是笔误 |
| `enumerate items[default]` / `itemize items[ball]` | 列表符号 | 在 `\AtBeginDocument` 里设置属多此一举，导言区直接设即可；且与 `circles` 主题冲突 |

---

## 3. 问题清单（按优先级）

| # | 位置 | 现象 | 原因 | 影响 | 处理 |
|---|---|---|---|---|---|
| 1 | 全文 | 无 `\NeedsTeXFormat`、无 `\ProvidesPackage` | 直接从 `.tex` 导言区整段搬来 | 无版本信息，报错难定位 | 补包头 |
| 2 | 38—40 | 缺字体时报错终止 | 无 `\IfFontExistsTF` 回退 | 换机器/Overleaf 直接编译失败 | 加回退 + 警告 |
| 3 | 130 | alert 块正文黑字压深红 | `bg=structure!90`（模板里是 `!10`） | 投屏几乎不可读 | 改 `accent!10` |
| 4 | 128 | alert 块标题与普通块同色 | 用 `structure.fg!80` | 学生分不清"注意"与"定义" | 用 `accent` |
| 5 | 26—27 | 加载 `caption` 并 `\captionsetup{name=图}` | 与 beamer caption 模板重叠；ctex 已设"图" | 潜在冲突、图注格式不统一 | 去掉 caption，保留 `\setbeamertemplate{caption}[numbered]` |
| 6 | 16 | `parskip` | 与 beamer 段距冲突 | 块/列表间距变松且不随字号缩放 | 改为可选 |
| 7 | 57—75 | 三段页脚宽度合计 100% | 定宽盒无余量 | 偶发 `Overfull \hbox` | `\hbox to\paperwidth` + `\hss`，比例 30/45/25 |
| 8 | 90—101 | 帧标题条高度逐帧变化 | `dp` 用实测标题深度 | 正文起点逐帧抖动 | `ht=1em, dp=2pt` 定死 |
| 9 | 96 | `\settoheight{\beamertitleht}` 结果未用 | 死代码 | 误导后续维护 | 删除 |
| 10 | 81—89 | 11.6pt / 0.52pt 魔数、`\global`、无前缀宏名 | 调参残留 | 换字号/比例即错位；宏名冲突风险 | 提为 `\newlength` + `\setnavheight`，去掉 `dp=0.5ex` |
| 11 | 17 & 23 | `graphicx` 加载两次 | 复制粘贴 | 无功能影响，只是脏 | 去重 |
| 12 | 14 & 20 | `amsfonts` 被 `amssymb` 包含 | 同上 | 同上 | 去重 |
| 13 | 9 | `hyperref` 重复加载 | beamer 已加载 | 可能覆盖 beamer 的链接设置 | 改用 `\hypersetup` |
| 14 | 6 & 133—135 | `circles` 主题被 `[ball]`、`[default]` 覆盖 | 设计意图不一致 | 主题白设，符号风格与"circles"名不符 | 二选一并注释 |
| 15 | 55 | `dotpink` 定义后从未使用 | 备用色遗留 | 调色板噪音 | 删除或标注"备用" |
| 16 | 42—55 | 颜色定义在 `\mode<presentation>` 内 | 整段搬入模式块 | article/讲义模式颜色未定义 | 移到模式块外（或明确"仅演示模式"） |
| 17 | 3 | `\ProcessOptionsBeamer` 空转 | 未声明任何选项 | 无实际作用 | 删掉，或补 `\DeclareOptionBeamer` |
| 18 | 19 | `\apptocmd{\frame}` 依赖 beamer 内部 | 民间补丁 | 失效时静默；与帧内对齐命令打架 | 改 `\renewcommand{\raggedright}{\justifying}` |
| 19 | 1—139 | 全部内容在模式块内 | — | `beamerarticle` 下整包无动作、且实测会留下待扫描状态 | 明确"仅面向演示模式" |
| 20 | 32 | 定理编号全局连续 | `[numbered]` 语义如此 | 与教材"2.1、2.2"编号不符 | 需要时改 `[numbered by section]` 或自建 `\newtheorem` |

---

## 4. 修改建议（可直接替换的代码）

### 4.1 补包头

```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{mybeamer}[2026/11/25 v1.0 Beamer theme for math courseware]
```

### 4.2 字体加回退（不再因缺字体而失败）

```latex
\providecommand{\IfFontExistsTF}[3]{#2}
\ifdefined\setCJKmainfont
  \IfFontExistsTF{Source Han Serif SC}
    {\setCJKmainfont{Source Han Serif SC}[BoldFont={Source Han Serif SC Bold}]}
    {\PackageWarningNoLine{mybeamer}{未找到思源宋体，回退 SimSun}%
     \IfFontExistsTF{SimSun}{\setCJKmainfont{SimSun}[AutoFakeBold=2.5]}{}}
\fi
```

### 4.3 图注：去掉 `caption`，只留 beamer 的模板

```latex
% 删除 \usepackage{caption} 与 \captionsetup[figure]{name=图}
\setbeamertemplate{caption}[numbered]
\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}
```

### 4.4 alert 块真正"红"起来

```latex
\setbeamercolor{block title alerted}{bg=accent,fg=white}
\setbeamercolor{block body alerted}{bg=accent!10,fg=black}   % 原来是 structure!90
```

### 4.5 页脚：留余量 + 三段文字双向居中 + 放大字号

```latex
\setlength{\mb@footheight}{16pt}      % 14pt 字号以下的单行文字，16pt 高度刚好留出上下白
  
% 字号：原主题这里是 7pt 左右（\scriptsize 级别），投影上几乎看不清
\setbeamerfont{author in head/foot}{size=\small}
\setbeamerfont{title in head/foot}{size=\small}
\setbeamerfont{frame number}{size=\small}

\setbeamertemplate{footline}{%
  \leavevmode
  \hbox to\paperwidth{%
    \begin{beamercolorbox}[wd=0.30\paperwidth,ht=\mb@footheight,dp=0pt,vmode]{footleft}%
      \vbox to\mb@footheight{\vfil
        \hbox to\hsize{\hss\usebeamerfont{author in head/foot}\insertshortauthor\hss}%
      \vfil}%
    \end{beamercolorbox}%
    ...（中、右两块同构，只换宽度、颜色名与 \insertshorttitle / \mb@frameinfo）...
    \hss
  }%
}
```

三个关键手法：

| 手法 | 为什么 |
|---|---|
| `ht=\mb@footheight, dp=0pt, vmode` | 把色条高度定死，文字不再靠 `ht/dp` 猜基线位置 |
| `\vbox to\mb@footheight{\vfil 文字 \vfil}` | 上下两个**等量** `\vfil` 把单行文字精确压到色条正中，垂直居中 |
| `\hbox to\hsize{\hss 文字 \hss}` | 左右两个 `\hss` 是无限伸缩胶，强制水平居中；比 beamercolorbox 的 `center` 选项可靠（在 `vmode` 下 `center` 只设 `leftskip/rightskip`，实测第一个盒子不生效，左边那段仍顶到页边） |

注意：放大字号后必须同步加高 `\mb@footheight`，否则文字会被色条上下裁掉（也可用 `\setfootheight{18pt}` 在导言区调）。

### 4.6 帧标题定高（消除正文抖动）

```latex
\setbeamertemplate{frametitle}{%
  \nointerlineskip
  \usebeamerfont*{frametitle}%
  \begin{beamercolorbox}[wd=\paperwidth,sep=0ex,ht=1em,dp=2pt,
                          leftskip=0.5em,rightskip=2em]{frametitle}%
    \strut\insertframetitle
  \end{beamercolorbox}%
}
```

### 4.7 对齐：换实现，不依赖帧收尾

```latex
\renewcommand{\raggedright}{\justifying}   % 比 \apptocmd{\frame}{}{\justifying}{} 稳
```

### 4.8 页眉：去掉魔数与多余下伸

```latex
\newlength{\mb@navheight}\setlength{\mb@navheight}{11.6pt}  % 10pt/16:9 校准值
\newcommand{\setnavheight}[1]{\setlength{\mb@navheight}{#1}}
\setbeamertemplate{headline}{%
  \begin{beamercolorbox}[wd=\paperwidth,colsep=0pt,ht=\mb@navheight,dp=0pt,vmode]{section in head/foot}%
    \vbox to \mb@navheight{\vskip0.5pt \insertnavigation{\paperwidth}\vss}%
  \end{beamercolorbox}%
}
```

---

## 5. 新版包：`mybeamer2.sty`

已创建：`D:\beamer-math\mybeamer2.sty`（**没有改动、没有覆盖原有的 `mybeamer.sty`**）。目标：**观感与原版一致**，同时把上表问题逐条修掉，并把常用参数做成开关。

### 5.1 用法

```latex
\documentclass[10pt,aspectratio=169,t]{ctexbeamer}
\usepackage{mybeamer2}                 % 默认：两端对齐、标题页不显页码
```

编译仍用 `xelatex`（推荐 `latexmk -xelatex main.tex`），**连续两次**以获得正确总页数。

### 5.2 选项

| 选项 | 默认 | 作用 |
|---|---|---|
| `justify` | 开 | 正文两端对齐（已实测与原版逐行行末坐标一致） |
| `ragged` | — | 正文左对齐（要"原汁原味"的 beamer 观感时用） |
| `boldtitle` | 关 | 帧标题加粗 |
| `firstpagenumber` | 关 | 标题页也显示"页码 / 总页数"（原版行为） |
| `parskip` | 关 | 加载 `parskip`（还原原版的松段距） |
| `nonav` | 关 | **隐藏**右下角导航符号；默认是显示（上课点它翻页），投影给观众时才关 |
| `print` | 关 | 调色板改用 CMYK（印发讲义／送印刷厂）；默认是 RGB（屏幕、投影） |

用法示例：

```latex
\usepackage[ragged,boldtitle]{mybeamer2}   % 左对齐 + 标题加粗
\usepackage[print]{mybeamer2}              % 印刷配色
```

### 5.3 可调命令

| 命令 | 作用 |
|---|---|
| `\setnavheight{12pt}` | 顶部导航条高度（默认 11.6pt） |
| `\setfootheight{16pt}` | 页脚条高度（默认 16pt；改页脚字号后要同步调，否则文字被裁） |
| `\setnavscale{2.3}` | 右下角箭头图标缩放倍数（默认 2.3，约 10pt 宽 × 7pt 高） |
| `\usecmykcolors` | 导言区内随时切到 CMYK 配色 |
| `\usergbcolors` | 导言区内随时切回 RGB 配色 |

### 5.4 与原版的差异对照

| 项目 | 原版 `mybeamer.sty` | 新版 `mybeamer2.sty` |
|---|---|---|
| 包元数据 | 无 | `\NeedsTeXFormat` + `\ProvidesPackage`（带日期版本） |
| 模式块 | 只包住主题部分 | 整体只在 presentation 模式生效（article 下不解包） |
| 依赖宏包 | 逐个 `\usepackage`，有重复 | 统一 `\RequirePackage`，去掉重复的 `graphicx`/`amsfonts`/`hyperref` |
| `caption` | 加载并 `\captionsetup` | 不加载，保留空壳 `\captionsetup` 兼容旧稿；用 `\figurename` |
| `parskip` | 强制加载 | 改为 `parskip` 选项 |
| 中文字体 | 无回退 | `\IfFontExistsTF` 检查，缺字体回退 SimSun/SimHei 并警告 |
| 对齐 | `\apptocmd{\frame}` | `\renewcommand{\raggedright}{\justifying}`（`ragged` 可关） |
| alert 块 | 标题同色、正文黑字深红（不可读） | 标题 `accent`、正文 `accent!10`（可读、可区分） |
| 页脚 | 30/50/20，无余量；三处分别左/中/右对齐，字号约 7pt | 30/45/25 + `\hbox to\paperwidth` + `\hss`；三处一律水平+垂直居中，字号 `\small`，条高 16pt |
| 页眉 | `dp=0.5ex` 多一条 0.5ex 色带，`\global`+魔数 | `dp=0pt`，长度提为 `\mb@navheight`，可 `\setnavheight` 调 |
| 帧标题 | 逐帧测深度，正文起点会抖 | `ht=1em, dp=2pt` 定死；删死代码与冗余 `\usebeamercolor` |
| 导航符号 | 未关（实测右下角出现一排小图标，压住页脚） | 默认显示，但换成自绘实心红色大箭头（◀◀ ◀ ▶ ▶▶ ｜ 首页），位于页脚色条上方不压字；`nonav` 可隐藏 |
| 链接 | 默认彩色框 | `\hypersetup{hidelinks,bookmarksnumbered}` |
| 标题页页码 | 显示 `1 / 4` | 默认隐藏，`firstpagenumber` 可恢复 |
| 内部宏名 | `\beamerheadheight` 等无前缀 | 统一 `\mb@...` 前缀，避免与他人宏包撞名 |
| 调色板 | 全部 CMYK + 少数 RGB，两种色空间混用 | RGB／CMYK 两套定义，`print` 选项或 `\usecmykcolors` 切换；默认 RGB |

### 5.5 实测验证

用 4 页样例（标题页 / 列表与长段落 / 三种块 + 图注 / pgfplots 图象）同时编译原版与新版，均 `xelatex` 两次通过、无错误：

| 检查项 | 原版 | 新版 |
|---|---|---|
| 编译 | 通过 | 通过（仅 ctex 自带的 xeCJK 字体族提示） |
| 正文对齐 | 两端对齐（行末 x=425.186pt） | 两端对齐（行末 x=425.186pt，完全一致） |
| 正文起点 | y=43.86pt | y=42.24pt（帧标题条矮 1.6pt，观感几乎无差） |
| 页脚比例 | 0.30 / 0.50 / 0.20（像素实测 207/346/139 px） | 0.30 / 0.45 / 0.25 |
| 页脚文字 | 左顶格 / 中居中 / 右贴右，字号 ≈7pt，条高 10.4pt | 三处均居中，字号 `\small`（≈9pt），条高 16pt |
| 右下导航符号 | 有（压在页脚色带上，3pt 高、40% 淡红） | 自绘实心主色大箭头（约 10×7pt），链接矩形实测 12×7.4pt / 22×7.4pt，整只箭头都可点；位于色条上方不压字 |
| alert 块 | 黑字压 90% 深红，不可读 | 浅粉底 + 黑字，标题用强调红 |
| 标题页页码 | `1 / 4` | 无 |
| 页脚三段居中 | 不一致 | 三段墨迹中心与色带中心偏差 ≤ 1px（200 dpi 实测 188/189、660.5/661.5、1102/1102.5） |

另外单独测试了 `\documentclass{beamer}` + `\usepackage[UTF8]{ctex}` + `mybeamer2` 的组合，同样通过。

### 5.6 关于色空间：为什么默认 RGB

XeLaTeX **不会**替你换算颜色：用 `\definecolor{...}{cmyk}` 定义的颜色会以 DeviceCMYK 原样写进 PDF（解压内容流能看到 `0 1 1 0.45 k`），屏幕上那个红由**播放器现算**，WPS、Adobe、手机、投影仪各算各的；而 `RGB` 定义则原样输出，所见即所得。

实测（把 14 个颜色画成色卡，150 dpi 取样）：

| 颜色 | 原定义 | 屏幕实际渲染 |
|---|---|---|
| `xyyg` | cmyk 0,1,1,0.45 | rgb(146,15,20) |
| `xyyg_blue` | cmyk 0.6,0.35,0,0.4 | rgb(71,92,135) |
| `xyyg_green` | cmyk 0.2,0,1,0.15 | rgb(177,196,14) |
| `xyyg_orange` | cmyk 0,0.7,1,0 | rgb(242,92,25) |
| `accent` | RGB 196,60,50 | rgb(196,60,50)，精确 |
| `dotpink` | RGB 214,60,120 | rgb(214,60,120)，精确 |
| 反面例子：cmyk 100% 黑 | cmyk 0,0,0,1 | rgb(35,31,32)，并非纯黑 |

所以原包里 `xyyg` 系（CMYK）与 `accent`（RGB）**在同一页上是两种红**。新版把 CMYK 值换算成它在屏幕上的实际观感值，再写成 RGB（`146,15,20` 等），于是：屏幕端颜色被钉死、跨播放器一致，且与 `accent` 同处一个色空间，`xyyg!60!xyyg_orange` 这类混色结果也变得可预测。

代价是印刷端：RGB 送印需由印厂转 CMYK，高饱和深红容易偏暗。因此保留 `print` 选项／`\usecmykcolors` 切回原 CMYK（`accent` 同时换成 cmyk 0,0.69,0.75,0.23 的近似），`xyyg` 总墨量 245%，常规胶印安全。

实测两版 PDF 的色空间分布：

| 版本 | 内容流中 CMYK 操作数 | RGB 操作数 |
|---|---|---|
| 原版 / `print` 模式 | 112—219 | 28 |
| 新版默认（RGB） | 0 | 166 |

切到 RGB 后，页面上主色块实测仍是 rgb(146,15,20) 与 rgb(196,60,50)，与原版一致；只有页脚中段这类"混色"从 rgb(184,40,23) 微调到 rgb(184,46,22)，肉眼不可辨。

### 5.7 页脚字号/高度怎么再调

字号与条高必须成对调整，否则要么文字被裁、要么条内空荡：

| 字号（`\setbeamerfont{... in head/foot}`） | 建议 `\mb@footheight` |
|---|---|
| `\scriptsize`（7pt，原版观感） | 12pt |
| `\footnotesize`（8pt） | 14pt |
| `\small`（9pt，**当前默认**） | 16pt |
| `\normalsize`（10pt） | 17—18pt |

导言区覆盖示例（想比现在再大一档）：

```latex
\usepackage{mybeamer2}
\setfootheight{17pt}
\setbeamerfont{author in head/foot}{size=\normalsize}
\setbeamerfont{title in head/foot}{size=\normalsize}
\setbeamerfont{frame number}{size=\normalsize}
```

代价：页脚从 10.4pt 加到 16pt，正文可用高度少 5.6pt（约 0.4 行）；如果某几页本来就排得满，记得再压缩一点行距或内容。

### 5.8 右下角导航箭头（上课用）

beamer 原生那排图标的两个毛病：只有 3pt 高、颜色是 40% 淡红（`structure.fg!40!bg`），投影上小且糊；而且颜色在主题载入时就画进 PDF 了，用 `\setbeamercolor{navigation symbols}` 改不动。新版直接重画了 `navigation symbols` 模板，换成实心主色的大三角：

| 按钮 | 作用 | 实测点击区域 |
|---|---|---|
| ◀◀ | 上一节（回到本节开头） | 22.2 × 7.4 pt |
| ◀ | 上一页 | 12.3 × 7.4 pt |
| ▶ | 下一页 | 12.3 × 7.4 pt |
| ▶▶ | 下一节 | 22.2 × 7.4 pt |
| 首页 | 回到演示文稿第一页 | 20.3 × 12.9 pt |

组与组之间插一条 0.4pt 的浅红竖线，六个三角不会看起来"等距"；整行贴在页脚色条上方约 3pt，不压字，随 4:3 / 16:9 自动靠右。

**实现要点（踩过的坑）**

1. **不要用 TikZ 画三角**：`\hyperlink{…}{\tikz…\fill}` 生成的链接矩形只有 2.8pt 高（XeLaTeX 只把基线以上部分算进去），箭头下半截点不到；换成"数学实心三角字形 + `\scalebox`"后，链接矩形跟着字形盒走，实测 7.4pt 高，整个箭头都可点。
2. 缩放在字形盒上做：`\scalebox{\mb@navscale}{$\blacktriangleleft$}`，默认 2.3 倍 ≈ 10pt 宽、7pt 高；`\setnavscale{2.0}` 可整体缩小。
3. 两侧各留 1.2pt 空白（`\mbox{\hspace{1.2pt}…\hspace{1.2pt}}`），点击目标比图形再大一圈。

**可调 / 可退**

```latex
\setnavscale{2.0}          % 图标整体缩小一圈（默认 2.3）
\usepackage[nonav]{mybeamer2}   % 整排不显示
\setbeamertemplate{navigation symbols}[default]  % 恢复 beamer 原版淡红小图标
```

只想留翻页、不要节跳转：把模板里 `\hyperlinksectionendprev{...}` 和 `\hyperlinksectionstartnext{...}` 两行删掉即可（行位置见 5.8 对应的样式文件 §5 段）。整行宽约 100pt（16:9 下约占页宽 22%），若某页右下角本来就有内容，建议把内容上移或按上面把图标缩小。

### 5.9 `mybeamer0.sty`：极简个人版

同一套版式的"减法版"，**没有选项、没有条件判断、所有数字写死**，现为 159 行 / 6.6 KB（末尾 9b 处附了一段可选的标题页窄色块居中的注释代码），适合自己上课用、以后想改就直接改文件里的数字。

```latex
\documentclass[10pt,aspectratio=169,t]{ctexbeamer}
\usepackage{mybeamer0}
```

和 `mybeamer2` 的关系：把默认值全部固化，删掉开关。

| 项目 | `mybeamer2`（正式版） | `mybeamer0`（极简版） |
|---|---|---|
| 选项 | `justify/ragged`、`boldtitle`、`firstpagenumber`、`parskip`、`print`、`nonav` | 无，全部取默认值 |
| 色空间 | RGB／CMYK 两套，`print` 切换 | 只有 RGB |
| 命令 | `\setnavheight`、`\setfootheight`、`\setnavscale`、`\usecmykcolors/\usergbcolors` | 无，改文件里的 `16pt`、`11.6pt`、`2.3` |
| 字体回退 | `\IfFontExistsTF` 检查，缺字体回退 SimSun/SimHei | 直接设思源字体，缺字体才报错 |
| 依赖 | 另加载 tabularx/multirow/colortbl/multicol/tcolorbox 等 | 只留 xcolor、amsmath、amssymb、graphicx、booktabs、ragged2e、tikz、pgfplots |
| 输出 | — | 与 `mybeamer2` 默认设置**逐页像素完全一致**（4 页样例 110 dpi 渲染差异为 0） |

取舍说明：讲义要用的表格、tcolorbox、分栏、`caption` 兼容空壳都没带；需要时在 `.tex` 里自己 `\usepackage{tcolorbox}` 即可，不影响样式。

要调节省一点的常用三处（都是文件里的裸数字）：

| 想改什么 | 改哪里 |
|---|---|
| 页脚高矮 | 页脚模板里的三处 `ht=16pt` 与 `\vbox to 16pt`（成组改，保持四个数字一致） |
| 页脚字号 | `size=\small` 三行（放大后必须同步加高上面的 16pt） |
| 顶部导航条高 | headline 里的 `ht=11.6pt` 与 `\vbox to 11.6pt` |
| 箭头大小 | `\scalebox{2.3}` 两处 |

**`mybeamer0t.sty`** 是把 9b 那段注释真正启用的产物（`t` = title）：除标题页外与 `mybeamer0` 逐字节相同。实测四页样例在 110 dpi 下渲染，第 2–4 页像素差异 `bbox = None`（完全一致），只有标题页变成 0.75 宽、圆角带阴影、左右各 124px 留白的居中红色块。

### 5.10 标题页的标题框怎么调

标题页看着是一个红条，其实是 beamer 的 `title page` 模板把 5 个色块竖着排起来的：`title`（标题＋副标题）、`author`、`institute`、`date`、`titlegraphic`，上下各一个 `\vfill` 把它们撑在页面中间。

红条本身来自内层模板 `title`：

```latex
% beamer 默认（beamerinnerthemedefault.sty 第 41 行）
\defbeamertemplate{title}{default}[1][]{%
  \begin{beamercolorbox}[sep=8pt,center,#1]{title}
    \usebeamerfont{title}\inserttitle\par
    \ifx\insertsubtitle\@empty\else
      \vskip0.25em
      {\usebeamerfont{subtitle}\usebeamercolor[fg]{subtitle}\insertsubtitle\par}
    \fi
  \end{beamercolorbox}}
```

所以三个层次分开调：

| 想改 | 命令 | 默认值 |
|---|---|---|
| 底色/字色 | `\setbeamercolor{title}{bg=xyyg,fg=white}`（本包已设） | spruce 主题的蓝 |
| 字号 | `\setbeamerfont{title}{size=\Large,series=\bfseries}`；副标题 `subtitle` 默认 `\normalsize` | `\Large`（14.4pt） |
| 框宽/内边距/圆角 | `\setbeamertemplate{title}[default][wd=…,sep=…,rounded=true,shadow=true]` | `wd=\textwidth`（实测 398.3pt，左右各留 1cm）、`sep=8pt` |

`beamercolorbox` 认这些键：`wd`、`ht`、`dp`、`sep`、`colsep`、`leftskip`/`rightskip`、`center`/`left`/`right`、`rounded`、`shadow`、`ignorebg`、`bgopacity`、`vmode`。

三个现成方案（均已编译验证）：

```latex
% ① 只换外观，不动模板：窄一点 + 圆角 + 阴影
\setbeamertemplate{title}[default][wd=0.75\textwidth,sep=14pt,rounded=true,shadow=true]

% ② 白底红字 + 上下细线（要 \makeatletter 才能用 \@empty 时改成 \empty）
\setbeamercolor{title}{bg=white,fg=xyyg}
\setbeamertemplate{title}{%
  {\color{xyyg}\rule{\textwidth}{1.2pt}}\par\vskip7pt
  \begin{beamercolorbox}[wd=\textwidth,sep=3pt,center,ignorebg]{title}%
    {\usebeamerfont{title}\inserttitle\par}%
    \ifx\insertsubtitle\empty\else
      \vskip0.25em{\usebeamerfont{subtitle}\usebeamercolor[fg]{subtitle}\insertsubtitle\par}%
    \fi
  \end{beamercolorbox}%
  \vskip3pt{\color{xyyg}\rule{\textwidth}{0.6pt}}\par}

% ③ 整页通栏（贴到左右纸边）：正文左右各有 1cm 边距，故加负 \hspace
\setbeamertemplate{title}{%
  \hspace*{-1cm}\begin{beamercolorbox}[wd=\paperwidth,sep=10pt,center]{title}
    {\usebeamerfont{title}\inserttitle\par}
  \end{beamercolorbox}}
```

#### 5.10.1 窄色块怎么让它居中

方案一的短写法 `\setbeamertemplate{title}[default][wd=0.75\textwidth,…]` **只能改宽，不能居中**：beamer 把色块当定宽 `\hbox` 直接丢进垂直列表，左边缘就压在正文左边界上。16:9 页在 120 dpi 下量出来的结果是 `left=41px`、`right=206px`，明显偏左。

试过但**无效**的两种：

| 写法 | 结果 | 原因 |
|---|---|---|
| `\begin{center}…\end{center}` | 仍 41/206 | 垂直模式下 `\centering` 只设 `\leftskip`/`\rightskip`，单个定宽盒的行上没有可拉伸的胶 |
| `\hspace*{\fill} 色块 \hspace*{\fill}` | 仍 41/206 | 行首的 fil 胶被当垃圾胶丢掉，撑不到右边 |

**有效**的三种（实测都是 `left=right=124px`，色块 508px、页宽 756px，完全对称）：

| 写法 | 代码骨架 | 备注 |
|---|---|---|
| A `\centerline` | `\centerline{\begin{beamercolorbox}[…]{title}…\end{beamercolorbox}}` | 最省事；内部就是 `\hbox to\hsize{\hss…\hss}` |
| B `\hbox to\textwidth` | `\noindent\hbox to\textwidth{\hss 色块 \hss}` | 与 A 等价，可塞别的东西 |
| C `\makebox`+`\parbox` | `\noindent\makebox[\textwidth][c]{\parbox{0.75\textwidth}{\begin{beamercolorbox}[wd=\linewidth]…}}` | 想在色块外加留白/装饰时用 |

推荐直接用 A，写成完整模板（**替换模板后副标题要自己补回来**，否则只出标题）：

```latex
% 方案一 + 居中：窄色块、圆角、阴影，水平居中
\setbeamertemplate{title}{%
  \centerline{%
    \begin{beamercolorbox}[wd=0.75\textwidth,sep=14pt,center,rounded=true,shadow=true]{title}%
      {\usebeamerfont{title}\inserttitle\par}%
      \ifx\insertsubtitle\empty\else
        \vskip0.25em{\usebeamerfont{subtitle}\usebeamercolor[fg]{subtitle}\insertsubtitle\par}%
      \fi
    \end{beamercolorbox}}}
```

三点细节：`sep=14pt` 是上下内边距，想让条更"瘦"就调到 8–10pt；`wd=0.75\textwidth` 改成 `0.66` 或 `0.8` 都行，只要留够左右对称的空白；`rounded`/`shadow` 靠 TikZ 画，关掉就是纯直角块。阴影会稍微探出色块右下方几个 pt，不影响排版。

这段已以注释形式放进 `mybeamer0.sty` 第 9b 处，取消注释即可用。

垂直位置：`\documentclass[t]{ctexbeamer}` 让标题页内容靠上（本工程默认如此）；想更精确就重定义 `title page`，把开头那个 `\vfill` 换成 `\vskip 2cm` 之类的固定量。

---

## 6. 迁移到新版（3 步）

1. 把 `mybeamer2.sty` 放到与 `.tex` 同一目录（或 `texmf` 可见路径）。目前它在 `D:\beamer-math\`，编译子目录里的课件时要么复制过去，要么设 `TEXINPUTS`，或干脆统一用 `\usepackage{../../mybeamer2}`。
2. 把课件里的 `\usepackage{mybeamer}` 改成 `\usepackage{mybeamer2}`，删掉 `.tex` 里重复的导言区设置（如果那份 `.tex` 之前把样式内联了一份）。
3. 原样式内容一行都不用改就能继续用；若想让封面显示页码，加 `firstpagenumber`；若想保留原来的松段距，加 `parskip`；要把同一份内容印发讲义，再加 `print`（CMYK）。

若暂时不想换包，只想修毛病：按第 4 节逐条替换即可，改动可以局部进行，不影响其他部分。

---

## 7. 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 页码显示 `1 / ??` 或总页数不对 | `\inserttotalframenumber` 靠 `.aux` 传递 | 再编译一次；或 `latexmk` |
| 换到别的电脑报 "fontspec Error: The font ... has not been found" | 没装思源字体 | 新版会自动回退；旧版需手动注释字体设置 |
| 图片绕排（`wrapfig`）位置乱飞 | frame 内 `\parshape` 与 beamer 帧盒子冲突 | 改用 `columns` + `\includegraphics`，或把图放小页 `minipage` |
| 表格里 `p{}` 列变成两端对齐 | `\renewcommand{\raggedright}{\justifying}` 是全局替换 | 表格列内加 `\raggedright` 恢复 |
| 块标题过长换行后压住正文 | 帧标题/块标题色盒高度固定 | 缩短标题；或给块标题设 `\setbeamercolor` 之外另建 `tcolorbox` |
| article/讲义模式报错 | 本包整段在 `\mode<presentation>` 内，且 beamer 的 `\mode` 在"直接 `\usepackage`"的包里于 article 模式表现不稳 | 讲义版另建一份 `.tex`，或在 article 下不要加载本包 |
| 想关掉右下角那排导航箭头 | 默认是开着的（上课点击用） | 加 `nonav` 选项：`\usepackage[nonav]{mybeamer2}` |
| 页脚文字被色条裁掉、或上下贴边 | 放大字号后没同步加高 `\mb@footheight` | 按 5.7 的表成对调整（`\setfootheight` + 字号） |
| 投影和打印出来的红不是一个色 | 原包 CMYK／RGB 混用，且 cmyk 由播放器现算 | 新版默认 RGB；印发讲义时用 `[print]`（见 5.6） |
| `Overfull \hbox` 提示但不影响输出 | 页脚/页眉的定宽盒与 `\paperwidth` 舍入 | 新版已用 `\hss`/`dp=0pt` 处理 |

---

## 附 A：主色速查

| 用途 | 颜色 | RGB（屏幕，默认） | CMYK（`print`） |
|---|---|---|---|
| 导航条、标题条、页脚、块标题、`structure` | `xyyg` | 146,15,20 | 0,1,1,0.45 |
| 页脚中段 | `xyyg!60!xyyg_orange` | — | — |
| 强调（`\alert`、alert 块） | `accent` | 196,60,50 | 0,0.69,0.75,0.23 |
| 块正文底 | `xyyg!10` / `accent!10` | — | — |
| 非当前节文字 | `white!55!xyyg` | — | — |

其余辅助色（`xyyg_gold` 238,159,60；`xyyg_blue` 71,92,135；`xyyg_darkblue` 14,52,99；`xyyg_gray` 134,131,122；`xyyg_dirt` 186,149,112；`xyyg_orange` 242,92,25；`xyyg_green` 177,196,14；`xyyg_darkgreen` 69,71,27；`WM_Gold` 181,138,67）的 RGB 值都是各自原 CMYK 定义在屏幕上的实测渲染值，`print` 模式下自动换回原 CMYK 定义。

## 附 B：原文件区块索引

| 行号 | 区块 |
|---|---|
| 1—3 | 模式控制、`\ProcessOptionsBeamer` |
| 4—7 | smoothbars / serif / circles / spruce |
| 9—35 | 宏包依赖与 TikZ 库 |
| 19 | 两端对齐补丁 |
| 27—28 | 图注设置 |
| 29—32 | 行距、pgfplots、定理编号 |
| 38—40 | 思源字体 |
| 42—55 | 调色板 |
| 57—75 | footline |
| 77—89 | headline |
| 90—101 | frametitle |
| 103—105 | 注释掉的字体设置 |
| 107—113 | 注释掉的 palette 设置 |
| 114—119 | 颜色绑定、foot 颜色 |
| 120—125 | 块颜色、列表模板、导航符号注释 |
| 126—135 | `\AtBeginDocument` 内块配色与列表模板 |
| 138—139 | `\mode<all>` |
