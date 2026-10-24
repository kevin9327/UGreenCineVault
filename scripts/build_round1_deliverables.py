import os
import re
import zipfile
import subprocess
import json

os.makedirs("UGreenCineVault/dist", exist_ok=True)

# 10 Substantive Responses — strictly < 500 English words total (even including headings!)
QUESTIONS_AND_ANSWERS = [
    (
        "1. What does your Skill do? (one sentence)",
        "cinevault-roughcut-director orchestrates five UGREEN AI NAS experts to turn raw project photos, video footage, field audio, production scripts, and music stems into a timecoded rough-cut edit decision sheet and checksum-verified media vault."
    ),
    (
        "2. Who is your target user, and what is their problem?",
        "Filmmakers, video editors, and creative teams store terabytes of multi-camera shoots on NAS drives, but waste hours manually hunting across separate photo, video, audio, document, and file apps before editing can begin."
    ),
    (
        "3. What is your solution?",
        "An approval-gated Uliya orchestration Skill that discovers matching visual shots, subtitles, reference tracks, interview transcripts, and script clearances across NAS domains, compiles a Markdown Edit Decision Sheet, and consolidates non-duplicate selects."
    ),
    (
        "4. What is the main user flow?",
        "The user provides a project theme, date window, and workspace scope; reviews discovered media, transcripts, and duplicate reports; approves album creation and Markdown sheet saving; and confirms final tagging and vault consolidation."
    ),
    (
        "5. How is your idea different from existing tools or common AI solutions?",
        "Cloud AI editors require uploading massive raw footage off-device, whereas cinevault-roughcut-director runs locally on UGREEN AI NAS across five native domain experts with cryptographic deduplication, zero path fabrication, and strict approval gates."
    ),
    (
        "6. Which UGREEN AI NAS features does your Skill use, and at which step?",
        "Stage 1 uses Album search, EXIF, OCR, VLM, and conditional albums; Stage 2 uses Video/Music search and subtitles; Stage 3 uses Document reconciliation and Knowledge audio transcription; Stage 4 uses Filesystem/Filemgr deduplication, tagging, and batch move."
    ),
    (
        "7. What is your technical approach?",
        "Built on Uliya catalog v2.0.0, the parent Skill validates user scope and delegates sequentially to photo-agent (ug-photo), media-agent (ug-video, ug-music), document-agent (ug-document), knowledge-agent (ug-knowledge), and file-agent (ug-filesystem, ug-filemgr, file-workflow), enforcing waiting_user, waiting_approval, and empty-result abstention."
    ),
    (
        "8. What have you built so far? What is not built yet? What still needs testing on a NAS?",
        "We built the complete SKILL.md package passing check-skill.mjs (0 errors, 0 warnings) plus an interactive UGOS simulation workbench; live latency tuning and multi-gigabyte batch-move execution still require testing on physical NAS hardware."
    ),
    (
        "9. How will you test your Skill if you become a Finalist?",
        "Core Case 1: end-to-end 4K shoot discovery, transcription, and vault consolidation. Core Case 2: duplicate camera-card detection via scan-dedupe with partial approval cancellation. Edge Case: future date window returning zero matches without fabricated paths."
    ),
    (
        "10. What are the known limits, risks, or outside dependencies of your Skill?",
        "Transcription and VLM speed depend on local NAS model load; state-changing actions pause for user approval; and external cloud AI calls are optional, disabled for private files, and restricted to anonymized metadata."
    ),
]

def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9'-]+", text))

answers_only_words = sum(count_words(a) for _, a in QUESTIONS_AND_ANSWERS)
headers_and_answers_words = sum(count_words(q) + count_words(a) for q, a in QUESTIONS_AND_ANSWERS)

print(f"Word Count (10 Substantive Answers only): {answers_only_words} words (Limit: <= 500)")
print(f"Word Count (10 Headers + Answers combined): {headers_and_answers_words} words (Limit: <= 500)")
assert answers_only_words <= 450, f"Too many words in answers: {answers_only_words}"
assert headers_and_answers_words <= 495, f"Too many words including headers: {headers_and_answers_words}"

# Check Question 1 is strictly one sentence
q1_sentences = [s.strip() for s in re.split(r'[.!?]+', QUESTIONS_AND_ANSWERS[0][1]) if s.strip()]
assert len(q1_sentences) == 1, f"Q1 must be 1 sentence, got {len(q1_sentences)}"

def build_pdf(output_path: str):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    except ImportError:
        subprocess.check_call(["C:\\Users\\swsz9\\AppData\\Local\\Programs\\Python\\Python311\\python.exe", "-m", "pip", "install", "reportlab", "-q"])
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=42,
        rightMargin=42,
        topMargin=36,
        bottomMargin=36,
        title="CineVault Rough-Cut Director - UGREEN Hackathon 2026 Round 1 Proposal",
        author="Byungju Kim"
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    sub_style = ParagraphStyle(
        "DocSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569"),
        spaceAfter=8
    )
    q_style = ParagraphStyle(
        "QStyle",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=11.5,
        textColor=colors.HexColor("#047857"),
        spaceBefore=4,
        spaceAfter=1.5
    )
    a_style = ParagraphStyle(
        "AStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=11.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=3
    )
    sec_style = ParagraphStyle(
        "SecStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=8,
        spaceAfter=4
    )
    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#334155")
    )

    story = []
    story.append(Paragraph("UGREEN Hackathon 2026 on AI NAS — Round 1 Project Proposal", title_style))
    story.append(Paragraph(
        f"<b>Skill Name:</b> cinevault-roughcut-director &nbsp;|&nbsp; <b>Track:</b> Unleash Your Creativity &nbsp;|&nbsp; "
        f"<b>Substantive Response Word Count:</b> {answers_only_words} words (<= 500 words limit)",
        sub_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=6))

    for q, a in QUESTIONS_AND_ANSWERS:
        story.append(Paragraph(q, q_style))
        story.append(Paragraph(a, a_style))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=4))
    story.append(Paragraph("Excluded Disclosures: Third-Party Components, Open-Source Libraries & AI Tools", sec_style))

    table_data = [
        ["Component / Tool", "Version", "Source URL", "License", "Principal Use in Project"],
        ["uliya-skill-kit", "0.7.3-en (v2.0.0)", "https://ai.ugreen.com/pages/hackathon-starter-kit", "UGREEN Official Rules", "Capability catalog & static skill checker"],
        ["FastAPI & Pydantic", "0.115+ / 2.9+", "https://pypi.org/project/fastapi/", "MIT License", "Companion local simulator & MCP server"],
        ["Pytest", "8.3+", "https://pypi.org/project/pytest/", "MIT License", "Automated verification of skill contracts"],
        ["ReportLab", "4.2+", "https://pypi.org/project/reportlab/", "BSD License", "Generating Round 1 PDF proposal"],
        ["HeyGen HyperFrames", "0.8.192", "https://github.com/heygen-com/hyperframes", "Apache-2.0 / MIT", "Companion 1080p demo video rendering"],
        ["Gemini / Claude IDE", "2026.10", "https://aistudio.google.com/", "Commercial Terms", "Catalog schema validation & demo TTS voiceover"],
        ["FlowMusic", "2026.10", "https://flowmusic.app/", "Royalty-Free Commercial", "Demo background soundtrack stems"],
    ]
    t = Table(table_data, colWidths=[95, 68, 155, 82, 128])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.2),
        ("LEADING", (0, 0), (-1, -1), 9.0),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t)

    story.append(Spacer(1, 6))
    story.append(Paragraph("Team Consent Declaration, Member Information & Electronic Signature (Excluded from Word Limit)", sec_style))
    story.append(Paragraph(
        "<b>Entrant Type:</b> Individual (Solo Representative) &nbsp;|&nbsp; <b>Member Name:</b> Byungju Kim (kevin9327) &nbsp;|&nbsp; "
        "<b>Development Start Date:</b> 10-24-2026<br/>"
        "<b>Declaration:</b> I hereby declare that I am an Eligible Individual, that the submitted Skill (<i>cinevault-roughcut-director</i>) "
        "and its core workflow were newly developed during the Hackathon Period in compliance with the UGREEN Hackathon 2026 on AI NAS Official Rules, "
        "and that no real personal data, private NAS files, or secret credentials are included.<br/>"
        "<b>Electronic Signature:</b> <i>/s/ Byungju Kim</i> &nbsp;&nbsp;&nbsp; <b>Date Signed:</b> October 24, 2026",
        small_style
    ))

    doc.build(story)

pdf_path = "UGreenCineVault/dist/CineVault_UGREEN_Round1_Proposal.pdf"
build_pdf(pdf_path)
pdf_size = os.path.getsize(pdf_path)
print(f"Generated PDF: {pdf_path} ({pdf_size} bytes, limit <= 1,048,576 bytes)")
assert pdf_size < 1024 * 1024

# Build Pre-test Skill Package ZIP
skill_root = "UGreenCineVault/skill-package/cinevault-roughcut-director"
zip_path = "UGreenCineVault/dist/cinevault-roughcut-director.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(skill_root):
        dirs.sort()
        for f in sorted(files):
            abs_p = os.path.join(root, f)
            rel_p = os.path.relpath(abs_p, "UGreenCineVault/skill-package").replace("\\", "/")
            zf.write(abs_p, rel_p)

zip_size = os.path.getsize(zip_path)
print(f"Generated Pre-test Skill ZIP: {zip_path} ({zip_size} bytes, limit <= 10,485,760 bytes)")
with zipfile.ZipFile(zip_path, "r") as zf:
    print("ZIP Contents:", zf.namelist())
