"""
Shiksha Radar - Streamlit Dashboard Entry Point
"""
import streamlit as st

st.set_page_config(
    page_title="Shiksha Radar",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .gap-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .gap-high { background: #fef2f2; color: #dc2626; }
    .gap-medium { background: #fffbeb; color: #d97706; }
    .gap-low { background: #f0fdf4; color: #16a34a; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 1.5rem;
        background: white;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    .stTabs [aria-selected="true"] {
        background: #3b82f6 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="main-header">📊 Shiksha Radar</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered learning gap detection for teachers</p>', unsafe_allow_html=True)
    
    # Sidebar: Data upload
    with st.sidebar:
        st.header("📁 Data Upload")
        
        uploaded_files = st.file_uploader(
            "Upload assessment CSV files",
            type=["csv"],
            accept_multiple_files=True,
            help="Upload student responses, questions, and concept map CSVs"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        
        st.divider()
        
        # Quick stats if data loaded
        if "data_loaded" in st.session_state:
            students = st.session_state.get("students")
            responses = st.session_state.get("responses")
            if students is not None:
                st.metric("Students", len(students))
            if responses is not None:
                st.metric("Responses", len(responses))
                st.metric("Assessments", responses["assessment_id"].nunique())
        
        st.divider()
        st.caption("Shiksha Radar v0.1.0")
        st.caption("Privacy-first • Deterministic core • Evidence-based")

    # Main content area
    if "data_loaded" not in st.session_state:
        # Landing page with demo data option
        st.info("👋 Welcome! Upload your assessment data or try the demo.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Load Demo Data (Synthetic Class 5 Math)", type="primary", use_container_width=True):
                load_demo_data()
                st.rerun()
        
        with col2:
            st.markdown("""
            **Demo data includes:**
            - 50 students across 4 sections
            - 6 assessments over 18 weeks
            - 189 NCERT-aligned math questions
            - 6,000 student responses
            - 6 student archetypes for testing
            """)
        
        st.divider()
        st.subheader("How it works")
        st.markdown("""
        1. **Upload** CSV files (responses, questions, concept map)
        2. **Detect** learning gaps using mistake fingerprinting
        3. **Visualize** class heatmaps and student profiles
        4. **Intervene** with targeted recommendations
        5. **Reassess** and close the feedback loop
        """)
        
        with st.expander("📋 Expected CSV formats"):
            st.markdown("""
            **students.csv**: `student_id`, `grade`, `section`
            
            **questions.csv**: `question_id`, `text`, `concept`, `sub_concept`, `difficulty`, `expected_answer`
            
            **concept_map.csv**: `question_id`, `concept`, `sub_concept`
            
            **responses.csv**: `response_id`, `student_id`, `assessment_id`, `question_id`, `student_answer`, `is_correct`, `error_type`, `created_at`
            """)
    else:
        # Render dashboard tabs
        render_dashboard()


def load_demo_data():
    """Load synthetic demo data into session state."""
    from app.data.loader import load_all_synthetic
    from app.analytics.profiler import build_concept_profiles, detect_learning_gaps
    
    with st.spinner("Loading demo data..."):
        students, questions, concept_map, responses = load_all_synthetic()
        profiles = build_concept_profiles(responses, questions)
        gaps = detect_learning_gaps(profiles)
        
        st.session_state.students = students
        st.session_state.questions = questions
        st.session_state.concept_map = concept_map
        st.session_state.responses = responses
        st.session_state.profiles = profiles
        st.session_state.gaps = gaps
        st.session_state.data_loaded = True


def render_dashboard():
    """Render the main dashboard with tabs."""
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Class Overview", 
        "🔥 Student × Concept Heatmap", 
        "👤 Student Profile", 
        "📋 Class Insights"
    ])
    
    with tab1:
        render_overview_tab()
    
    with tab2:
        render_heatmap_tab()
    
    with tab3:
        render_student_profile_tab()
    
    with tab4:
        render_class_insights_tab()


def render_overview_tab():
    """Class Overview tab - KPIs and concept difficulty."""
    from app.analytics.profiler import get_concept_difficulty
    
    students = st.session_state.students
    responses = st.session_state.responses
    profiles = st.session_state.profiles
    gaps = st.session_state.gaps
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Students</div>
            <div class="metric-value">{len(students)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Assessments</div>
            <div class="metric-value">{responses['assessment_id'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        concepts_covered = responses.merge(
            st.session_state.questions[["question_id", "concept"]], 
            on="question_id"
        )["concept"].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Concepts</div>
            <div class="metric-value">{concepts_covered}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        students_needing_support = len(set(g.student_id for g in gaps))
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Needing Support</div>
            <div class="metric-value" style="color: #dc2626;">{students_needing_support}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Concept Difficulty Bars
    st.subheader("📊 Concept Difficulty (Class Error Rate)")
    
    difficulty = get_concept_difficulty(profiles)
    difficulty_df = pd.DataFrame([
        {"Concept": k, "Error Rate": v} for k, v in sorted(difficulty.items(), key=lambda x: -x[1])
    ])
    
    import plotly.express as px
    fig = px.bar(
        difficulty_df, 
        x="Error Rate", 
        y="Concept",
        orientation="h",
        color="Error Rate",
        color_continuous_scale="Reds",
        range_color=[0, difficulty_df["Error Rate"].max() * 1.1],
        height=400
    )
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_tickformat=".0%",
        showlegend=False,
        margin=dict(l=150, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Assessments timeline
    st.subheader("📅 Assessment Timeline")
    assessments = responses.groupby("assessment_id").agg(
        date=("created_at", "min"),
        students=("student_id", "nunique"),
        questions=("question_id", "nunique"),
        accuracy=("is_correct", "mean")
    ).reset_index().sort_values("date")
    assessments["date"] = pd.to_datetime(assessments["date"]).dt.strftime("%b %d")
    st.dataframe(assessments, use_container_width=True, hide_index=True)


def render_heatmap_tab():
    """Student × Concept Heatmap tab."""
    import plotly.graph_objects as go
    
    profiles = st.session_state.profiles
    gaps = st.session_state.gaps
    
    # Create gap lookup
    gap_lookup = {}
    for g in gaps:
        key = (g.student_id, g.concept)
        if key not in gap_lookup or g.confidence > gap_lookup[key].confidence:
            gap_lookup[key] = g
    
    # Get unique students and concepts
    student_ids = sorted(set(p.student_id for p in profiles))
    concepts = sorted(set(p.concept for p in profiles))
    
    # Build heatmap data
    z_data = []
    hover_text = []
    
    for student_id in student_ids:
        row_z = []
        row_hover = []
        for concept in concepts:
            # Find profile
            profile = next((p for p in profiles if p.student_id == student_id and p.concept == concept), None)
            gap = gap_lookup.get((student_id, concept))
            
            if profile is None:
                row_z.append(0)
                row_hover.append("No data")
            elif gap:
                row_z.append(2)  # High confidence gap
                row_hover.append(
                    f"<b>{student_id}</b> - {concept}<br>"
                    f"Errors: {gap.evidence_count} across {gap.assessments_count} assessments<br>"
                    f"Dominant: {gap.dominant_error}<br>"
                    f"Confidence: {gap.confidence:.0%}<br>"
                    f"Trend: {gap.trend}"
                )
            elif profile.total_errors > 0:
                row_z.append(1)  # Emerging
                row_hover.append(
                    f"<b>{student_id}</b> - {concept}<br>"
                    f"Errors: {profile.total_errors}/{profile.total_attempts}<br>"
                    f"Error rate: {profile.error_rate:.0%}<br>"
                    f"Trend: {profile.trend}"
                )
            else:
                row_z.append(0)  # On track
                row_hover.append(f"<b>{student_id}</b> - {concept}<br>No errors")
        
        z_data.append(row_z)
        hover_text.append(row_hover)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=concepts,
        y=student_ids,
        colorscale=[
            [0, "#16a34a"],    # Green - on track
            [0.5, "#d97706"],  # Yellow - emerging
            [1, "#dc2626"]     # Red - high confidence gap
        ],
        showscale=False,
        hoverongaps=False,
        hovertemplate="%{hovertext}<extra></extra>",
        text=hover_text,
    ))
    
    fig.update_layout(
        height=600,
        xaxis_title="Concept",
        yaxis_title="Student",
        margin=dict(l=100, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("🟢 On track | 🟡 Emerging errors | 🔴 High-confidence learning gap")
    
    # Legend
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<span class="gap-badge gap-low">🟢 On Track</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="gap-badge gap-medium">🟡 Emerging</span>', unsafe_allow_html=True)
    with col3:
        st.markdown('<span class="gap-badge gap-high">🔴 Gap Detected</span>', unsafe_allow_html=True)


def render_student_profile_tab():
    """Student Profile deep-dive tab."""
    gaps = st.session_state.gaps
    profiles = st.session_state.profiles
    
    # Student selector
    students_with_gaps = sorted(set(g.student_id for g in gaps))
    all_students = sorted(set(p.student_id for p in profiles))
    
    selected_student = st.selectbox(
        "Select Student",
        all_students,
        index=0 if all_students else None,
        format_func=lambda x: f"{x} {'🔴' if x in students_with_gaps else '🟢'}"
    )
    
    if not selected_student:
        return
    
    student_gaps = [g for g in gaps if g.student_id == selected_student]
    student_profiles = [p for p in profiles if p.student_id == selected_student]
    
    # Overall stats
    total_errors = sum(p.total_errors for p in student_profiles)
    total_attempts = sum(p.total_attempts for p in student_profiles)
    total_gaps = len(student_gaps)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attempts", total_attempts)
    with col2:
        st.metric("Total Errors", total_errors, f"{(total_errors/total_attempts*100):.1f}%" if total_attempts > 0 else "0%")
    with col3:
        st.metric("Learning Gaps", total_gaps, "🔴" if total_gaps > 0 else "🟢")
    
    st.divider()
    
    if student_gaps:
        st.subheader("🔴 Detected Learning Gaps")
        
        for gap in sorted(student_gaps, key=lambda x: -x.confidence):
            with st.expander(f"{gap.concept} — {gap.confidence:.0%} confidence ({gap.trend} trend)"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **Evidence:** {gap.evidence_count} errors across {gap.assessments_count} assessments  
                    **Dominant Error Type:** {gap.dominant_error}  
                    **Trend:** {gap.trend}  
                    **Detected:** {gap.detected_at[:10]}
                    """)
                
                with col2:
                    st.metric("Confidence", f"{gap.confidence:.0%}")
                    st.metric("Assessments", gap.assessments_count)
                
                # Error breakdown
                profile = next((p for p in student_profiles if p.concept == gap.concept), None)
                if profile and profile.error_breakdown:
                    st.markdown("**Error Breakdown:**")
                    for err_type, count in sorted(profile.error_breakdown.items(), key=lambda x: -x[1]):
                        st.write(f"  • {err_type}: {count}")
    
    else:
        st.success("🎉 No learning gaps detected for this student!")
    
    st.divider()
    
    # Progress timeline
    st.subheader("📈 Progress Timeline")
    
    # Get student responses
    student_responses = st.session_state.responses[
        st.session_state.responses["student_id"] == selected_student
    ].copy()
    
    if len(student_responses) > 0:
        student_responses["created_at"] = pd.to_datetime(student_responses["created_at"])
        
        # Merge with questions to get concepts
        student_responses = student_responses.merge(
            st.session_state.questions[["question_id", "concept"]], 
            on="question_id", how="left"
        )
        
        # Group by assessment and concept
        timeline = student_responses.groupby(["assessment_id", "concept", "created_at"]).agg(
            total=("is_correct", "count"),
            correct=("is_correct", "sum")
        ).reset_index()
        timeline["error_rate"] = 1 - timeline["correct"] / timeline["total"]
        
        import plotly.express as px
        fig = px.line(
            timeline, 
            x="created_at", 
            y="error_rate", 
            color="concept",
            markers=True,
            labels={"error_rate": "Error Rate", "created_at": "Assessment Date"},
            height=400
        )
        fig.update_layout(yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)


def render_class_insights_tab():
    """Class Insights tab - common gaps and trends."""
    from app.analytics.profiler import get_class_gaps, get_concept_difficulty
    
    gaps = st.session_state.gaps
    profiles = st.session_state.profiles
    
    st.subheader("🎯 Common Gaps (Affecting Multiple Students)")
    
    class_gaps = get_class_gaps(gaps, min_students=1)
    
    if class_gaps:
        gap_data = []
        for concept, count in sorted(class_gaps.items(), key=lambda x: -x[1]):
            # Get dominant error for this concept
            concept_gaps = [g for g in gaps if g.concept == concept]
            dominant = max(
                (err for g in concept_gaps for err in [g.dominant_error]), 
                key=lambda e: sum(1 for g in concept_gaps if g.dominant_error == e),
                default="unknown"
            )
            avg_conf = sum(g.confidence for g in concept_gaps) / len(concept_gaps)
            
            gap_data.append({
                "Concept": concept,
                "Students Affected": count,
                "Dominant Error": dominant,
                "Avg Confidence": f"{avg_conf:.0%}",
            })
        
        st.dataframe(pd.DataFrame(gap_data), use_container_width=True, hide_index=True)
    else:
        st.info("No common gaps detected.")
    
    st.divider()
    
    # Assessment trends
    st.subheader("📈 Assessment Trends (Class Average)")
    
    responses = st.session_state.responses.copy()
    responses["created_at"] = pd.to_datetime(responses["created_at"])
    responses = responses.merge(
        st.session_state.questions[["question_id", "concept"]], 
        on="question_id", how="left"
    )
    
    # Class average error rate per concept per assessment
    trend_data = responses.groupby(["assessment_id", "concept", "created_at"]).agg(
        total=("is_correct", "count"),
        correct=("is_correct", "sum")
    ).reset_index()
    trend_data["error_rate"] = 1 - trend_data["correct"] / trend_data["total"]
    trend_data = trend_data.sort_values("created_at")
    
    import plotly.express as px
    fig = px.line(
        trend_data,
        x="created_at",
        y="error_rate",
        color="concept",
        markers=True,
        facet_col="concept",
        facet_col_wrap=3,
        height=500,
        labels={"error_rate": "Class Error Rate", "created_at": "Date"}
    )
    fig.update_layout(yaxis_tickformat=".0%", showlegend=False)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Intervention tracking (placeholder)
    st.subheader("📝 Intervention Tracking")
    st.info("Intervention tracking will be available after generating recommendations.")
    
    if st.button("Generate Interventions for Gaps"):
        st.session_state.show_interventions = True
        st.rerun()


if __name__ == "__main__":
    import pandas as pd
    main()