import streamlit as st
from groq import Groq

# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="Studio Desk",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dark, editorial UI — intentionally closer to a creator's workspace
# than a generic AI chatbot.
st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }
    .stApp {
        background: #101110;
        color: #f1f0e9;
    }
    [data-testid="stHeader"] {
        background: rgba(16, 17, 16, 0.92);
    }
    [data-testid="stSidebar"] {
        background: #171917;
        border-right: 1px solid #2b2e2a;
    }
    [data-testid="stSidebar"] * {
        color: #e9e9e2;
    }
    h1, h2, h3 {
        letter-spacing: -0.035em;
    }
    .eyebrow {
        color: #b4c7a1;
        text-transform: uppercase;
        letter-spacing: .16em;
        font-size: .72rem;
        font-weight: 700;
        margin-bottom: .45rem;
    }
    .hero-title {
        font-size: clamp(2.25rem, 5vw, 4.2rem);
        line-height: 1.02;
        letter-spacing: -.06em;
        font-weight: 760;
        margin: 0 0 .7rem 0;
    }
    .hero-copy {
        color: #a9ada5;
        font-size: 1.02rem;
        max-width: 720px;
        line-height: 1.65;
    }
    .rule {
        border-top: 1px solid #2b2e2a;
        margin: 1.35rem 0 1.6rem 0;
    }
    .section-label {
        color: #b4c7a1;
        text-transform: uppercase;
        letter-spacing: .12em;
        font-size: .72rem;
        font-weight: 700;
        margin-bottom: .65rem;
    }
    div[data-testid="stMetric"] {
        background: #191c19;
        border: 1px solid #2b2e2a;
        padding: 1rem;
        border-radius: 12px;
    }
    .stButton > button, .stDownloadButton > button {
        border-radius: 8px;
        border: 1px solid #b4c7a1;
        background: #b4c7a1;
        color: #151812;
        font-weight: 700;
        min-height: 2.8rem;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #c8d8b8;
        border-color: #c8d8b8;
        color: #151812;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"],
    .stNumberInput input {
        background: #191c19 !important;
        border-color: #363a34 !important;
        border-radius: 8px !important;
    }
    div[role="radiogroup"] {
        gap: .4rem;
    }
    .small-note {
        color: #92988f;
        font-size: .82rem;
        line-height: 1.5;
    }
    .output-heading {
        font-size: 1.45rem;
        font-weight: 700;
        letter-spacing: -.03em;
        margin-bottom: .25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def get_client():
    """Read the API key from Streamlit secrets or the environment."""
    api_key = None
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

    if not api_key:
        import os
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None
    return Groq(api_key=api_key)


def generate_content(client, system_prompt, user_prompt, model, temperature):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content or "No text was returned. Please try again."


def show_result(content, filename):
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="output-heading">Your draft</div>', unsafe_allow_html=True)
    st.markdown("Read through it, make it your own, then save a copy.")
    st.markdown(content)
    st.download_button(
        label="Download draft (.txt)",
        data=content,
        file_name=filename,
        mime="text/plain",
        use_container_width=False,
    )


# ------------------------------------------------------------
# Sidebar settings
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎬 Studio Desk")
    st.caption("A quiet workspace for video ideas and scripts.")
    st.markdown("---")

    st.markdown("**Workspace**")
    page = st.radio(
        "Choose a task",
        [
            "Video ideas",
            "Scene-by-scene script",
            "YouTube metadata",
            "Nursery rhyme & cartoon prompts",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**Writing settings**")
    model = st.selectbox(
        "Groq model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
        ],
        help="If a model is unavailable on your Groq account, choose another currently supported model.",
    )
    tone = st.selectbox(
        "Style",
        ["Warm and playful", "Natural and conversational", "Funny and energetic", "Calm and thoughtful", "Cinematic"],
    )
    audience = st.selectbox(
        "Audience",
        ["Kids / family", "Teens", "Adults", "General audience"],
    )
    language = st.selectbox(
        "Output language",
        ["English", "Roman Urdu", "Urdu", "Simple English"],
    )
    st.markdown("---")
    st.markdown(
        '<p class="small-note">Your API key should stay private. Add it in Streamlit Secrets or as an environment variable — never commit it to GitHub.</p>',
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# Main header
# ------------------------------------------------------------
st.markdown('<div class="eyebrow">Independent creator workspace</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Make something<br>worth watching.</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-copy">Find a direction, shape the story, and get the publishing details together. '
    'A practical writing desk for your next YouTube upload — without the clutter.</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

client = get_client()
if client is None:
    st.warning(
        "Add your Groq API key to use generation. In Streamlit Cloud, open "
        "your app's Settings → Secrets and add: GROQ_API_KEY = \"your_key_here\". "
        "For local use, set the GROQ_API_KEY environment variable."
    )

# ------------------------------------------------------------
# Task 1: Video ideas
# ------------------------------------------------------------
if page == "Video ideas":
    st.markdown('<div class="section-label">01 / Find the angle</div>', unsafe_allow_html=True)
    st.header("Video ideas")
    st.write("Start with a subject, a channel style, or a tiny spark of an idea.")

    with st.form("ideas_form"):
        topic = st.text_input(
            "What is the video about?",
            placeholder="e.g. a tiny cloud that changes the weather when it dances",
        )
        channel_style = st.text_input(
            "Channel or format (optional)",
            placeholder="e.g. 3D cartoons, educational shorts, cozy storytelling",
        )
        count = st.slider("How many ideas?", 3, 12, 6)
        submitted = st.form_submit_button("Find ideas", use_container_width=True)

    if submitted:
        if not topic.strip():
            st.error("Add a topic first so the ideas have somewhere to start.")
        elif client is None:
            st.error("Add your Groq API key in the sidebar instructions before generating.")
        else:
            prompt = f"""
Create {count} distinct YouTube video ideas about: {topic.strip()}.
Channel or format: {channel_style.strip() or "not specified"}.
Audience: {audience}. Language: {language}. Tone: {tone}.

For each idea include:
- A short, memorable working title
- The core premise in 2–3 sentences
- A strong opening hook
- A visual moment viewers will remember
- A realistic format suggestion (Short or long-form)

Make the ideas specific, varied, and filmable. Avoid generic clickbait, repeated concepts,
fake claims, and unnecessary intro fluff. Format with clear headings.
"""
            with st.spinner("Putting a few ideas on the table…"):
                try:
                    result = generate_content(
                        client,
                        "You are an experienced YouTube development editor. Give practical, original ideas in the requested language and tone.",
                        prompt,
                        model,
                        0.85,
                    )
                    show_result(result, "youtube-video-ideas.txt")
                except Exception as exc:
                    st.error(f"Generation failed: {exc}")
                    st.caption("Check your API key, model availability, and Groq usage limits.")

# ------------------------------------------------------------
# Task 2: Scene-by-scene script
# ------------------------------------------------------------
elif page == "Scene-by-scene script":
    st.markdown('<div class="section-label">02 / Shape the story</div>', unsafe_allow_html=True)
    st.header("Scene-by-scene script")
    st.write("Turn a premise into a sequence you can actually produce.")

    with st.form("script_form"):
        premise = st.text_area(
            "Story or video idea",
            placeholder="Describe what happens, who it is for, or the lesson you want to share…",
            height=120,
        )
        video_length = st.select_slider("Approximate length", options=["15 seconds", "30 seconds", "1 minute", "3 minutes", "5 minutes", "8 minutes"])
        scene_count = st.slider("Number of scenes", 3, 15, 6)
        include_voiceover = st.checkbox("Include voiceover / dialogue", value=True)
        include_visuals = st.checkbox("Include visual and animation directions", value=True)
        submitted = st.form_submit_button("Build the script", use_container_width=True)

    if submitted:
        if not premise.strip():
            st.error("Write a short premise first.")
        elif client is None:
            st.error("Add your Groq API key in the sidebar instructions before generating.")
        else:
            prompt = f"""
Write a production-friendly YouTube script based on this premise:
{premise.strip()}

Audience: {audience}. Language: {language}. Tone: {tone}.
Target length: {video_length}. Number of scenes: {scene_count}.
Include voiceover/dialogue: {include_voiceover}.
Include visual/animation directions: {include_visuals}.

Use this structure for every scene:
1. Scene number and estimated timestamp
2. What the viewer sees
3. Camera, movement, or animation direction (when relevant)
4. Voiceover/dialogue (if requested)
5. Sound or music cue (if useful)
6. Transition to the next scene

Keep continuity between scenes, make the opening engaging, and give the ending a clear payoff.
For kids' content, keep language age-appropriate and avoid frightening or unsafe instructions.
Finish with a short production checklist. Do not claim that visuals or audio have already been created.
"""
            with st.spinner("Laying out the scenes…"):
                try:
                    result = generate_content(
                        client,
                        "You are a thoughtful video writer and production planner. Write clear scripts that a small creator can produce.",
                        prompt,
                        model,
                        0.75,
                    )
                    show_result(result, "scene-by-scene-script.txt")
                except Exception as exc:
                    st.error(f"Generation failed: {exc}")
                    st.caption("Check your API key, model availability, and Groq usage limits.")

# ------------------------------------------------------------
# Task 3: YouTube metadata
# ------------------------------------------------------------
elif page == "YouTube metadata":
    st.markdown('<div class="section-label">03 / Get it ready to publish</div>', unsafe_allow_html=True)
    st.header("Titles, description & tags")
    st.write("Give the upload a clear promise and make it easy for the right viewers to find.")

    with st.form("metadata_form"):
        video_summary = st.text_area(
            "What happens in the video?",
            placeholder="Paste your script or summarize the video in a few sentences…",
            height=150,
        )
        title_count = st.slider("Title options", 3, 15, 8)
        include_chapters = st.checkbox("Suggest chapters (for longer videos)", value=False)
        submitted = st.form_submit_button("Prepare upload details", use_container_width=True)

    if submitted:
        if not video_summary.strip():
            st.error("Add a summary or script first.")
        elif client is None:
            st.error("Add your Groq API key in the sidebar instructions before generating.")
        else:
            prompt = f"""
Create YouTube publishing copy based on this video content:
{video_summary.strip()}

Audience: {audience}. Language: {language}. Tone: {tone}.
Provide:
1. {title_count} title options that are clear, appealing, and truthful
2. Your strongest title recommendation and one sentence explaining why
3. A natural description with the main value up front and a gentle call to action
4. Relevant search phrases
5. A concise comma-separated tag list
6. A pinned comment that invites genuine conversation
{"7. Suggested chapters with timestamps, clearly marked as estimates to verify" if include_chapters else ""}

Do not promise results the video does not deliver. Avoid keyword stuffing and misleading clickbait.
Do not invent links, credentials, or facts about the channel.
"""
            with st.spinner("Polishing the publishing details…"):
                try:
                    result = generate_content(
                        client,
                        "You are a YouTube channel editor focused on clear packaging, audience fit, and honest metadata.",
                        prompt,
                        model,
                        0.7,
                    )
                    show_result(result, "youtube-upload-details.txt")
                except Exception as exc:
                    st.error(f"Generation failed: {exc}")
                    st.caption("Check your API key, model availability, and Groq usage limits.")

# ------------------------------------------------------------
# Task 4: Nursery rhyme and cartoon prompts
# ------------------------------------------------------------
else:
    st.markdown('<div class="section-label">04 / Make it playful</div>', unsafe_allow_html=True)
    st.header("Nursery rhyme & cartoon prompts")
    st.write("Build a little world with a simple rhyme idea and scene prompts for your animation workflow.")

    with st.form("kids_form"):
        character = st.text_input(
            "Main character",
            placeholder="e.g. Bobo, a tiny dancing cloud",
        )
        lesson = st.text_input(
            "Theme or learning goal",
            placeholder="e.g. weather, colors, sharing, counting to five",
        )
        rhyme_style = st.selectbox(
            "Rhyme format",
            ["Catchy sing-along", "Gentle bedtime rhyme", "Call-and-response", "Learning song", "Funny action rhyme"],
        )
        scene_count = st.slider("Cartoon scenes", 3, 12, 6)
        duration = st.selectbox("Target video length", ["30 seconds", "1 minute", "2 minutes", "3 minutes"])
        submitted = st.form_submit_button("Create rhyme & scenes", use_container_width=True)

    if submitted:
        if not character.strip() or not lesson.strip():
            st.error("Add both a character and a theme so the rhyme has a clear direction.")
        elif client is None:
            st.error("Add your Groq API key in the sidebar instructions before generating.")
        else:
            prompt = f"""
Create a new nursery-rhyme concept and cartoon scene plan.

Main character: {character.strip()}.
Theme or learning goal: {lesson.strip()}.
Rhyme style: {rhyme_style}.
Audience: young children and families.
Language: {language}. Tone: {tone}.
Target duration: {duration}. Scene count: {scene_count}.

Return these sections:
A. A short original concept and the simple lesson
B. An original, child-friendly rhyme with a memorable repeated hook
C. A scene-by-scene plan. For each scene include estimated time, setting, character action,
   mood, and what changes visually
D. One separate image-generation prompt for each scene, describing character consistency,
   setting, framing, lighting, color palette, and 16:9 composition
E. A short continuity guide that repeats the character's defining visual details
F. A practical note for keeping cuts and movements aligned with the song

Keep the words easy to sing, lines short, and the visuals safe and age-appropriate.
Do not imitate a specific living artist or existing copyrighted character, song, or franchise.
The prompts are text only; do not claim images or videos have been generated.
"""
            with st.spinner("Dreaming up the little world…"):
                try:
                    result = generate_content(
                        client,
                        "You are a children's song concept writer and animation pre-production artist. Create original, gentle, memorable ideas.",
                        prompt,
                        model,
                        0.9,
                    )
                    show_result(result, "nursery-rhyme-cartoon-plan.txt")
                except Exception as exc:
                    st.error(f"Generation failed: {exc}")
                    st.caption("Check your API key, model availability, and Groq usage limits.")

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown(
    '<p class="small-note">Studio Desk is a writing helper. Review drafts for accuracy, age suitability, '
    'originality, and your channel voice before publishing.</p>',
    unsafe_allow_html=True,
)
