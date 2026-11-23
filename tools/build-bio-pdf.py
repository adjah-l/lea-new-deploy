from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak,
    KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = "assets/lawrence-adjah-bio.pdf"
INK = colors.HexColor("#0C0A09")
PAPER = colors.HexColor("#F4EEE4")
BODY = colors.HexColor("#3F3934")
MUTED = colors.HexColor("#746B62")
ACCENT = colors.HexColor("#C7433C")
LINE = colors.HexColor("#D9D0C5")

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="Eyebrow", parent=styles["Normal"], fontName="DejaVu-Bold",
    fontSize=7.5, leading=9, textColor=ACCENT, spaceAfter=8,
    tracking=1.4, uppercase=True,
))
styles.add(ParagraphStyle(
    name="Display", parent=styles["Heading1"], fontName="DejaVu-Bold",
    fontSize=31, leading=30, textColor=INK, spaceAfter=14,
))
styles.add(ParagraphStyle(
    name="Deck", parent=styles["Normal"], fontName="DejaVu",
    fontSize=12.5, leading=17, textColor=BODY, spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="BodyCopy", parent=styles["BodyText"], fontName="DejaVu",
    fontSize=9.4, leading=14.3, textColor=BODY, spaceAfter=11,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading2"], fontName="DejaVu-Bold",
    fontSize=13, leading=16, textColor=INK, spaceBefore=6, spaceAfter=9,
))
styles.add(ParagraphStyle(
    name="Small", parent=styles["Normal"], fontName="DejaVu",
    fontSize=7.8, leading=11.2, textColor=MUTED, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="Fact", parent=styles["Normal"], fontName="DejaVu-Bold",
    fontSize=9.2, leading=12, textColor=INK,
))
styles.add(ParagraphStyle(
    name="ShortBio", parent=styles["Normal"], fontName="DejaVu",
    fontSize=11.2, leading=16.2, textColor=BODY, spaceAfter=14,
))


def footer(canvas, doc):
    canvas.saveState()
    w, _ = LETTER
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(0.65 * inch, 0.55 * inch, w - 0.65 * inch, 0.55 * inch)
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.65 * inch, 0.34 * inch, "LAWRENCEADJAH.COM")
    canvas.drawRightString(w - 0.65 * inch, 0.34 * inch, f"BIOGRAPHY  |  {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    OUT, pagesize=LETTER, rightMargin=0.68 * inch, leftMargin=0.68 * inch,
    topMargin=0.62 * inch, bottomMargin=0.72 * inch,
    title="Lawrence E. Adjah - Biography",
    author="Lawrence E. Adjah",
    subject="Verified speaker and press biography",
)

story = []
headshot = Image("assets/headshot.jpg", width=1.62 * inch, height=2.02 * inch)
intro = [
    Paragraph("PASTOR  /  BUILDER  /  SPEAKER", styles["Eyebrow"]),
    Paragraph("Lawrence E. Adjah", styles["Display"]),
    Paragraph("Community leader, social entrepreneur, ordained minister, author, speaker and builder working at the intersection of relational health, social infrastructure, faith and community innovation.", styles["Deck"]),
    Paragraph("Dallas, Texas  |  la@lawrenceadjah.com  |  212.518.3324", styles["Small"]),
]
hero = Table([[headshot, intro]], colWidths=[1.85 * inch, 5.0 * inch], hAlign="LEFT")
hero.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (0, 0), 18),
    ("RIGHTPADDING", (1, 0), (1, 0), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
story += [hero, Spacer(1, 20), Paragraph("FULL BIOGRAPHY", styles["Eyebrow"])]

for text in [
    "Lawrence E. Adjah, MBA, M.Ed., M.Div., is a community leader, social entrepreneur and ordained minister whose work helps people and institutions establish and strengthen their most important relationships: with God, with other people and with themselves, mind, soul and body.",
    "He is the Founder and CEO of Family Dinner Foundation. Its Our Family Dinner initiative reports cumulative reach of approximately 50,000 people across roughly 40 cities and three continents through shared meals, small-group formation and mutual care. Lawrence created the 5C Mutual Care Framework - Commitment, Communication, Connection, Crisis and Celebration - as a practical language for building relationships and communities that can carry real life.",
    "A Presidential Leadership Scholar (2024), former McKinsey consultant and All-American track and field athlete, Lawrence brings together theological depth, strategy and cross-sector experience. He holds a B.A. from Harvard University, an MBA from Stanford Graduate School of Business, an M.Ed. from The University of Texas at Austin with distinction and an M.Div. from Gordon-Conwell Theological Seminary, where he received the Preaching Award and John D. Tate Award.",
    "Lawrence is a licensed and ordained minister and certified marriage counselor. He has counseled more than 100 couples, speaks and preaches across churches, universities, companies and conferences, and advises leaders designing healthier relational systems. He is the author of The 100 Marriage and narrator of Lawrence E. Adjah Reads the Bible: New International Version, the complete Old and New Testament.",
    "Through Watch God Work Studios, Lawrence builds Kingdom-honoring technology, including iToro, a Christian prayer platform for live audio prayer and replayable voice prayer. Across ministry, community, publishing and technology, his work is unified by one conviction: people are not built to do life alone.",
]:
    story.append(Paragraph(text, styles["BodyCopy"]))

story += [Spacer(1, 5), Paragraph("PUBLIC IMPACT NOTE", styles["Section"]),
          Paragraph("The approximately 50,000 people, roughly 40 cities and three continents figures describe cumulative program reach reported by Family Dinner Foundation. They are not a count of current members or independently audited unique participants. See lawrenceadjah.com/impact for definitions, sources and limitations.", styles["Small"]),
          PageBreak()]

story += [Paragraph("SHORT BIOGRAPHY", styles["Eyebrow"]),
          Paragraph("Lawrence E. Adjah", styles["Display"]),
          Paragraph("Lawrence E. Adjah, MBA, M.Ed., M.Div., is a Dallas-based pastor, social entrepreneur, author, speaker and builder focused on belonging, relationships, faith and social infrastructure. He is the Founder and CEO of Family Dinner Foundation, creator of the 5C Mutual Care Framework, a 2024 Presidential Leadership Scholar, former McKinsey consultant and All-American track and field athlete. Lawrence is the author of The 100 Marriage and narrator of the complete New International Version Bible audiobook. He holds degrees from Harvard, Stanford Graduate School of Business, The University of Texas at Austin and Gordon-Conwell Theological Seminary.", styles["ShortBio"])]

facts = [
    [Paragraph("EDUCATION", styles["Eyebrow"]), Paragraph("PRACTICE", styles["Eyebrow"])],
    [Paragraph("B.A., Harvard University<br/>MBA, Stanford Graduate School of Business<br/>M.Ed., The University of Texas at Austin, with distinction<br/>M.Div., Gordon-Conwell Theological Seminary", styles["BodyCopy"]),
     Paragraph("Licensed and ordained minister<br/>Certified marriage counselor<br/>Keynotes, preaching and facilitation<br/>Social infrastructure strategy<br/>Community and product building", styles["BodyCopy"])],
]
fact_table = Table(facts, colWidths=[3.45 * inch, 3.45 * inch])
fact_table.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (0, -1), 18),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LINEABOVE", (0, 0), (-1, 0), 0.6, LINE),
]))
story += [fact_table, Spacer(1, 10), Paragraph("SELECTED WORK", styles["Eyebrow"])]

selected = [
    ("Family Dinner Foundation", "Community-building work and the 5C Mutual Care Framework."),
    ("The 100 Marriage", "A book and assessment for surfacing the decisions and declarations people should address before marriage."),
    ("NIV complete Bible audiobook", "Lawrence E. Adjah Reads the Bible: New International Version, Old and New Testament."),
    ("iToro", "A Christian prayer platform for live audio prayer, replayable voice prayers, Prayer Trains and trusted communities."),
    ("Speaking and ministry", "Keynotes, sermons, workshops, counseling, chaplaincy, hosting and moderation."),
]
for name, desc in selected:
    story.append(KeepTogether([Paragraph(name, styles["Fact"]), Paragraph(desc, styles["Small"]), Spacer(1, 4)]))

story += [Spacer(1, 8), Paragraph("VERIFIED INDEPENDENT COVERAGE", styles["Eyebrow"]),
          Paragraph("George W. Bush Presidential Center  |  Black Enterprise  |  Chicago Tribune  |  Detroit Free Press  |  Presidential Leadership Scholars", styles["BodyCopy"]),
          Paragraph("Original publisher links and publication dates are maintained at lawrenceadjah.com/press. Impact definitions and supporting sources are maintained at lawrenceadjah.com/impact.", styles["Small"]),
          Spacer(1, 6), Paragraph("CONTACT", styles["Eyebrow"]),
          Paragraph("Speaking, ministry and partnership inquiries: la@lawrenceadjah.com  |  212.518.3324  |  lawrenceadjah.com/request", styles["BodyCopy"]),
          Paragraph("Last reviewed November 23, 2026.", styles["Small"])]

doc.build(story, onFirstPage=footer, onLaterPages=footer)
