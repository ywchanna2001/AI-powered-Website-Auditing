import streamlit as st
import requests
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title="AI Website Auditor", page_icon="🔍", layout="wide")

# Backend URL (Use localhost for now, we will change this during deployment)
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/audit")

st.title("🔍 AI-Powered Website Auditor")
st.markdown("Enter a URL to get a comprehensive SEO and UX audit powered by AI.")

# Input Section
url_input = st.text_input("Website URL:", placeholder="https://example.com")
analyze_button = st.button("Run Audit", type="primary")

if analyze_button:
    if not url_input:
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Analyzing website... This may take a few seconds."):
            try:
                # Call FastAPI Backend
                response = requests.post(BACKEND_URL, json={"url": url_input})
                response.raise_for_status()
                data = response.json()
                
                metrics = data["factual_metrics"]
                analysis = data["ai_analysis"]

                # --- 1. FACTUAL METRICS SECTION ---
                st.header("📊 Factual Metrics")
                
                # Top Row Metrics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Word Count", metrics["total_word_count"])
                col2.metric("Total Images", metrics["total_images"])
                col3.metric("CTAs Found", metrics["cta_count"])
                col4.metric("Internal Links", metrics["internal_links"])

                # Heading Distribution
                st.subheader("Heading Structure")
                h_data = pd.DataFrame({
                    "Tag": ["H1", "H2", "H3"],
                    "Count": [metrics["h1_count"], metrics["h2_count"], metrics["h3_count"]]
                })
                st.bar_chart(h_data.set_index("Tag"))

                # Image/Meta Details
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**SEO Tags**")
                    st.write(f"- **Title:** {metrics['meta_title']}")
                    st.write(f"- **Description:** {metrics['meta_description'] or 'Missing'}")
                with c2:
                    st.write("**Image Health**")
                    st.write(f"- **Missing Alt Text:** {metrics['images_missing_alt']}")
                    st.write(f"- **Missing Alt %:** {metrics['images_missing_alt_percentage']}%")

                st.divider()

                # --- 2. AI INSIGHTS SECTION ---
                st.header("💡 AI Insights")
                
                with st.expander("SEO & Structure", expanded=True):
                    st.write(analysis["insights"]["seo_structure"])
                
                with st.expander("Messaging & Clarity", expanded=True):
                    st.write(analysis["insights"]["messaging_clarity"])
                
                with st.expander("CTA & UX Concerns"):
                    st.write(f"**CTA Usage:** {analysis['insights']['cta_usage']}")
                    st.write(f"**UX Concerns:** {analysis['insights']['ux_structural_concerns']}")
                
                with st.expander("Content Depth"):
                    st.write(analysis["insights"]["content_depth"])

                st.divider()

                # --- 3. RECOMMENDATIONS SECTION ---
                st.header("🚀 Prioritized Recommendations")
                
                for rec in analysis["recommendations"]:
                    # Color-code priority labels
                    priority_color = "red" if rec['priority'] == 1 else "orange" if rec['priority'] == 2 else "blue"
                    
                    st.markdown(f"### :{priority_color}[Priority {rec['priority']}]")
                    st.markdown(f"**Action:** {rec['recommendation']}")
                    st.info(f"**Reasoning (Data-Backed):** {rec['reasoning']}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("Make sure your FastAPI backend is running on http://127.0.0.1:8000")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Built for EIGHT25MEDIA AI-Native Assignment")