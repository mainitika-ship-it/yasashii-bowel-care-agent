"""Rebuild the submission PNG from project-owned text and shapes; requires Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def render(output: Path = ROOT / "docs/architecture.png") -> None:
    image = Image.new("RGB", (1600, 1500), "#f4f7f5")
    draw = ImageDraw.Draw(image)
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    def font(size, bold=False):
        path = font_dir / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
        return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default(size=size)
    def label(x, y, value, size=23, bold=False, color="#19392d", anchor=None):
        draw.text((x, y), value, font=font(size, bold), fill=color, anchor=anchor)
    def box(rect, title, lines, color="#ffffff", border="#81968b"):
        x1,y1,x2,y2=rect
        draw.rounded_rectangle(rect, radius=18, fill=color, outline=border, width=3)
        label((x1+x2)/2,y1+20,title,25,True,anchor="mt")
        for i,line in enumerate(lines): label((x1+x2)/2,y1+60+i*27,line,20,anchor="mt")
    def arrow(points, color="#476356", dashed=False):
        for (x1,y1),(x2,y2) in zip(points,points[1:]):
            if dashed:
                length=max(abs(x2-x1),abs(y2-y1))
                for t in range(0,int(length),20):
                    end=min(t+10,length)
                    draw.line((x1+(x2-x1)*t/length,y1+(y2-y1)*t/length,
                               x1+(x2-x1)*end/length,y1+(y2-y1)*end/length),fill=color,width=4)
            else: draw.line((x1,y1,x2,y2),fill=color,width=4)
        (x1,y1),(x2,y2)=points[-2:]
        if y2>y1: tip=[(x2,y2),(x2-10,y2-16),(x2+10,y2-16)]
        elif x2>x1: tip=[(x2,y2),(x2-16,y2-10),(x2-16,y2+10)]
        else: tip=[(x2,y2),(x2+16,y2-10),(x2+16,y2+10)]
        draw.polygon(tip,fill=color)

    label(65,38,"Yasashii Bowel Care Agent",42,True)
    label(65,103,"Agents for Humans Hackathon  |  Observation, safe actions, and handoff",25)
    box((65,165,715,290),"CURRENT DEMO",["Synthetic structured observations","No patient images or identifying free text"],"#e8f3eb")
    box((885,165,1535,290),"PRE-EXISTING VISION PROTOTYPE",["Separate camera / ROI work, disclosed","Integration with this build is not yet verified"],"#eef0f2")
    arrow([(390,290),(390,322),(800,322),(800,350)])
    arrow([(1210,290),(1210,322),(800,322),(800,350)],dashed=True)
    box((475,350,1125,465),"1  VALIDATE INPUT",["Known fields, ranges, source and timestamp","Reject malformed or extra free-text fields"])
    arrow([(800,465),(800,505)])
    box((475,505,1125,620),"2  DETERMINISTIC QC",["PASS / HOLD / STOP with reason codes","Privacy flag, signal health and confidence"])
    arrow([(800,620),(800,700)])
    label(816,642,"non-identifying live input",20)
    box((475,700,1125,850),"3  STRANDS AGENTS SDK",["Bedrock (paid opt-in) OR local Ollama","Local model must advertise tool calling","Fresh agent; at most two model cycles"],"#e8eef9")
    arrow([(800,850),(800,930)])
    box((475,930,1125,1055),"4  LOCAL ACTION GUARD",["Exactly one matching action per event run","Trusted values; no model-supplied arguments"])
    arrow([(475,563),(320,563),(320,990),(475,990)],"#68746e")
    label(65,745,"Offline rehearsal",20,True)
    label(65,779,"No model call",19)
    arrow([(1125,563),(1510,563),(1510,990),(1125,990)],"#ad4541")
    label(1190,745,"Privacy-flagged STOP",20,True,"#9b322f")
    label(1190,779,"No model call",19,color="#9b322f")
    for x in (270,800,1330): arrow([(800,1055),(800,1100),(x,1100),(x,1140)])
    box((65,1140,475,1255),"PASS  /  RECORD",["event_log.jsonl","Observation recorded"],"#e8f3eb", "#2a8251")
    box((595,1140,1005,1255),"HOLD  /  HUMAN REVIEW",["confirmation_queue.jsonl","Pending; not a confirmed fact"],"#fff3da","#af7912")
    box((1125,1140,1535,1255),"STOP  /  SAFETY ALERT",["system_alerts.jsonl","No care observation recorded"],"#fff0ef","#ad4541")
    arrow([(270,1255),(270,1290)])
    box((65,1290,475,1395),"DAILY HANDOFF",["Counts recorded observations only"],"#e8f3eb")
    label(585,1295,"Each demo run: fresh logs + JSON report + bilingual result screen",23,True)
    label(585,1338,"Offline, live Bedrock and live local-model results are labelled separately.",21)
    label(65,1433,"Prototype limits: pending-review UI is not implemented; no diagnosis; no clinical accuracy claim.",21)
    label(65,1465,"Duplicate-write protection is per event run, not across restarts. No automatic paid fallback.",21)
    output.parent.mkdir(parents=True,exist_ok=True)
    image.quantize(colors=96).save(output,optimize=True)


if __name__ == "__main__":
    render()
