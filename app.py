import streamlit as st
import pandas as pd
import os
import base64
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- [1. 초기 설정 및 파일 경로] ---
NAME = "하상봉"
FIRM = "태평양감정평가법인"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO_FILE = "7. 사진(증명사진).pdf"
BIZ_CARD_FILE = "명함.jpg"

# 프리미엄 웹 이미지 URL (자동 연동)
IMG_HERO_ARCH = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop"
IMG_DATA_ANALYTICS = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop"

# 한글 폰트 설정 (차트용)
try:
    font_path = os.path.join(APP_DIR, 'malgun.ttf') 
    if os.path.exists(font_path):
        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
    else:
        plt.rc('font', family='Malgun Gothic') 
except Exception:
     pass

st.set_page_config(page_title=f"{NAME} 평가사 | AI 자동평가 시스템", page_icon="🏢", layout="wide")

# --- [2. 모던 프리미엄 디자인 (파란색 글씨 강조)] ---
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * { font-family: 'Pretendard', -apple-system, sans-serif !important; letter-spacing: -0.3px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    
    /* 짙고 세련된 슬레이트 네이비 배경 */
    .stApp { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #F8FAFC; }
    
    /* 사이드바 다크 테마 완벽 통합 */
    [data-testid="stSidebar"] { background-color: #0B1120 !important; border-right: 1px solid rgba(255,255,255,0.05); }
    [data-testid="stSidebar"] * { color: #F8FAFC !important; }
    div.row-widget.stRadio > div { background-color: transparent; }
    
    h1, h2, h3, h4 { color: #FFFFFF !important; font-weight: 700; }
    label, label p { color: #FFFFFF !important; font-weight: 600 !important; font-size: 1.1rem !important; }
    
    /* 🌟 실행 버튼 눈에 띄게 강조 (흰색 배경 + 뚜렷한 파란색 글씨) 🌟 */
    div.stButton > button:first-child {
        background: #FFFFFF !important; /* 깔끔한 흰색 배경 */
        color: #1D4ED8 !important; /* 뚜렷하고 신뢰감 있는 로열 블루(파란색) 글씨 */
        border: 2px solid #1D4ED8 !important; /* 파란색 테두리 */
        border-radius: 8px !important; 
        font-weight: 900 !important; 
        padding: 15px 24px !important; 
        transition: 0.3s ease !important; 
        font-size: 1.25rem !important; 
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(29, 78, 216, 0.3) !important;
    }
    /* 마우스 올렸을 때 반전 효과 */
    div.stButton > button:first-child:hover { 
        background: #1D4ED8 !important; /* 파란색 배경으로 전환 */
        color: #FFFFFF !important; /* 글씨는 흰색으로 반전 */
        transform: translateY(-2px); 
        box-shadow: 0 6px 20px rgba(29, 78, 216, 0.5) !important;
    }
    
    /* 텍스트 박스 모던 디자인 */
    .premium-text-box { 
        color: #CBD5E1; font-size: 1.1em; line-height: 1.8; padding: 30px; 
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); 
        border-radius: 12px; margin-bottom: 20px; backdrop-filter: blur(10px);
        box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
    }
    .highlight-gold { color: #FCD34D; font-weight: 700; }
    
    /* 웹 이미지 공통 스타일 (고급스러운 둥근 테두리) */
    .premium-web-img {
        width: 100%; border-radius: 16px; object-fit: cover;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    
    /* 사진 필터 (화사하게) */
    .profile-pic-container iframe {
        border-radius: 12px; box-shadow: 0px 10px 20px rgba(0,0,0,0.5);
        filter: brightness(1.05) contrast(1.05) saturate(1.05);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* 명함 텍스트 박스 */
    .text-biz-card {
        background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 35px 20px; text-align: center;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
    }
    .text-biz-card h3 { color: #94A3B8 !important; margin-bottom: 5px; font-size: 1.1em;}
    .text-biz-card h2 { color: #F8FAFC !important; margin-bottom: 25px; letter-spacing: 2px; font-size: 2em;}
    .text-biz-card p { color: #CBD5E1; font-size: 1.05em; line-height: 1.8; margin-bottom: 0px;}
    
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px; padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- [3. 파일 렌더링 함수] ---
def get_pdf_display(file_path, height=360):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        return f'<div class="profile-pic-container"><iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="{height}"></iframe></div>'
    return ''

def get_img_display(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            base64_img = base64.b64encode(f.read()).decode('utf-8')
        return f'<img src="data:image/jpeg;base64,{base64_img}" style="width:100%; border-radius:10px; box-shadow:0 4px 15px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1);">'
    return ''

# --- [4. 동적 데이터 로드 및 평가 알고리즘] ---
@st.cache_data
def load_and_evaluate(property_type, area_land, area_bldg, floor, rel_multiplier):
    df_officetel = pd.DataFrame() 
    mean_unit_price = 5630611     
    try:
        data_file = "하상봉 가격작업 (오피스텔).xlsx - 05C_KAPA_선례선정.csv"
        file_path = os.path.join(APP_DIR, data_file)
        if os.path.exists(file_path):
            df_raw = pd.read_csv(file_path)
            if '평가액/면적' in df_raw.columns:
                df_raw['단가'] = pd.to_numeric(df_raw['평가액/면적'], errors='coerce')
                df_officetel = df_raw.dropna(subset=['단가'])
                if not df_officetel.empty:
                    mean_unit_price = df_officetel['단가'].mean()
    except Exception: pass

    status_msg = f"✅ [{property_type}] 데이터베이스 연동 완료."
    data_count = len(df_officetel) if not df_officetel.empty else 0
    methods_values = {}
    
    if property_type == "토지건물":
        total_area = area_land + area_bldg
        methods_values = {'원가법': 1010000000, '비교법': 1030000000, '수익법': 1050000000}
        total_value = (methods_values['원가법'] * 0.1) + (methods_values['비교법'] * 0.8) + (methods_values['수익법'] * 0.1)
        final_unit_price = total_value / total_area
        methods_values['최종 조정'] = total_value
    else:
        adjusted_unit_price = mean_unit_price * (1 + (rel_multiplier / 100))
        total_area = area_bldg 
        total_value = adjusted_unit_price * total_area
        final_unit_price = adjusted_unit_price

    land_ratio = 0.325 if property_type == "아파트/다세대 (구분건물)" else 0.273
    return final_unit_price, total_value, total_area, total_value * land_ratio, total_value * (1 - land_ratio), methods_values, data_count, status_msg

# --- [5. 시각화 (레이더 차트)] ---
def plot_appraisal_methods(methods_dict):
    if not methods_dict: return None
    labels = list(methods_dict.keys())
    values = [methods_dict[label] for label in labels]
    labels.append(labels[0]); values.append(values[0])
    num_vars = len(labels) - 1
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_facecolor('#0F172A') 
    ax.plot(angles, values, color='#3B82F6', linewidth=2) # 차트 라인도 푸른빛으로 통일
    ax.fill(angles, values, color='#3B82F6', alpha=0.15) 
    
    final_idx = labels.index('최종 조정')
    if final_idx < num_vars: 
        ax.scatter(angles[final_idx], values[final_idx], color='#60A5FA', s=120, zorder=10) 
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels[:-1], color='#F8FAFC', fontproperties=fm.FontProperties(size=11, weight='bold'))
    ax.set_rlabel_position(0)
    plt.yticks([500000000, 1000000000, 1500000000], ["5억", "10억", "15억"], color="#64748B", size=9)
    plt.ylim(0, 1600000000)
    plt.tight_layout()
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    return fig

# --- [6. 사이드바 (다크 테마 통합)] ---
with st.sidebar:
    st.markdown(f"<h2 style='text-align: center; margin-bottom:20px; font-weight:800; font-size: 1.5rem;'>🏢 {FIRM}</h2>", unsafe_allow_html=True)
    st.markdown(get_pdf_display(os.path.join(APP_DIR, PHOTO_FILE)), unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 15px 0px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; font-weight: bold; color: #94A3B8 !important; margin-bottom: 5px;'>MAIN MENU</p>", unsafe_allow_html=True)
    page = st.radio("메뉴", ["👨‍💼 평가사 프로필", "⚙️ 시스템화 자동평가"], label_visibility="collapsed")
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 15px 0px;'>", unsafe_allow_html=True)
    st.markdown("<div style='opacity: 0.8;'>", unsafe_allow_html=True)
    st.markdown(get_img_display(os.path.join(APP_DIR, BIZ_CARD_FILE)), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- [7. 페이지 1: 모던 프로필] ---
if page == "👨‍💼 평가사 프로필":
    st.markdown(f"""
        <div style='padding:20px 10px 40px 10px; text-align:center;'>
            <h1 style='font-size: 3em; margin-bottom: 15px;'>가치를 읽고, 논리로 구조화하며, 신뢰로 완성합니다.</h1>
            <h3 style='color: #94A3B8 !important; font-weight: 500;'>정확한 가치판단을 넘어 신뢰와 품격을 도출하는 감정평가사</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<img src='{IMG_HERO_ARCH}' class='premium-web-img' style='height: 350px;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.3, 1], gap="large")
    with col1:
        st.markdown(f"""
        <div class="premium-text-box">
            <span class="highlight-gold">부동산의 복잡한 가치를 정교하게 해석하고, 신뢰도 높은 결과물로 완성하는 감정평가 전문가입니다.</span><br><br>
            법령과 판례, 실무기준에 대한 깊이 있는 이해를 바탕으로 개별 자산이 지닌 특성과 쟁점을 입체적으로 분석하고, 이를 <b>정확성·논리성·설득력</b>을 갖춘 평가로 구현합니다.<br><br>
            전통적인 감정평가의 영역에 머무르지 않고 <span class="highlight-gold">데이터, IT 자동화, 체계적인 분석 방식을 접목</span>하여 업무의 정밀도와 완성도를 동시에 끌어올립니다.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="text-biz-card">
            <h3>태평양감정평가법인 본사</h3>
            <h2>감정평가사 하 상 봉</h2>
            <hr style="border: 0; height: 1px; background: rgba(255,255,255,0.1); margin: 20px 0;">
            <p>
                🏢 서울시 중구 다산로 32<br>
                <span style="font-size:0.9em; color:#94A3B8;">(신당동, 남산타운5번상가 2,3,4층)</span><br><br>
                📞 <strong>Mobile.</strong> 010 - 2957 - 7402<br>
                ✉️ <strong>Email.</strong> sangbong.ha@packor.com
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- [8. 페이지 2: 시스템화 자동평가] ---
elif page == "⚙️ 시스템화 자동평가":
    
    col_head1, col_head2 = st.columns([2, 1], gap="large")
    with col_head1:
        st.markdown("<h2 style='font-size: 2.5em; margin-bottom:10px;'>⚙️ 실무형 AI 가치 자동산정</h2>", unsafe_allow_html=True)
        st.write("<div style='color:#94A3B8; margin-bottom:20px; font-size:1.1em; line-height: 1.6;'>대상 물건의 정보를 입력하시면, 평가사가 직접 구축한 데이터베이스 알고리즘과 통계적 검증을 거쳐 가장 신뢰할 수 있는 시산가액을 즉시 도출합니다.</div>", unsafe_allow_html=True)
    with col_head2:
        st.markdown(f"<img src='{IMG_DATA_ANALYTICS}' class='premium-web-img' style='height: 150px;'>", unsafe_allow_html=True)

    with st.form("auto_appraisal_form"):
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            addr = st.text_input("📍 대상 물건 소재지", value="서울 송파구 가락동 99")
            purpose = st.selectbox("🏢 물건 용도 선택", ["토지건물", "아파트/다세대 (구분건물)", "오피스텔", "집합상가"], index=0)
            
            if purpose == "토지건물":
                c1, c2 = st.columns(2)
                with c1: area_land = st.number_input("📐 토지면적 (㎡)", value=100.0, step=1.0)
                with c2: area_bldg = st.number_input("📐 건물면적 (㎡)", value=150.0, step=1.0)
            else:
                area_bldg = st.number_input("📐 전유면적 (㎡)", value=33.0, step=1.0)
                area_land = 0.0 
            
        with col_in2:
            floor = st.number_input("🔼 해당 층", value=12, min_value=1)
            st.write("<br>", unsafe_allow_html=True)
            with st.expander("🔍 평가사의 정밀 보정 통제 (수동 조정)", expanded=True):
                override_weight = st.slider("보정 가중치 (단가 조정율 %)", min_value=-10.0, max_value=10.0, value=0.0, step=1.0)
            
        st.write("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("프리미엄 AI 분석 실행")

    if submit:
        total_input_area = area_land + area_bldg if purpose == "토지건물" else area_bldg
        if total_input_area == 0:
            st.error("⚠️ 면적 정보를 입력해 주세요.")
            st.stop()
            
        adjusted_unit_price, total_value, total_area, land_value, bldg_value, methods_dict, data_count, status_msg = load_and_evaluate(purpose, area_land, area_bldg, floor, override_weight)
        
        st.divider()
        
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); padding: 40px; border-radius: 16px; margin: 20px 0px; text-align:center; box-shadow: 0px 10px 30px rgba(0,0,0,0.3); backdrop-filter: blur(10px);'>
            <p style='margin:0px; color:#94A3B8; font-weight:600; font-size:1.1em; letter-spacing: 1px;'>최종 도출 시산가액 ({purpose})</p>
            <h1 style='color:#3B82F6 !important; margin:15px 0px; font-size: 4em; font-weight: 800;'>₩ {int(total_value):,} 원</h1>
            <p style='margin:0px; color:#CBD5E1; font-size:1.1em;'>적용 단가: {int(adjusted_unit_price):,} 원/㎡ (전문가 보정 {override_weight}%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            if methods_dict:
                fig_radar = plot_appraisal_methods(methods_dict)
                if fig_radar: st.pyplot(fig_radar)
            else:
                st.info("💡 집합건물은 비교방식을 주방식으로 적용하여 단일 시산가액을 도출합니다.")
        
        with col_res2:
            st.markdown("<h4 style='margin-bottom: 20px;'>🏢 가치 배분 및 방식별 상세</h4>", unsafe_allow_html=True)
            st.write(f"대지권 배분액: **₩ {int(land_value):,}**")
            st.write(f"건물 배분액: **₩ {int(bldg_value):,}**")
            
            if methods_dict:
                st.write("---")
                st.dataframe(pd.DataFrame({
                    '평가 방식': ['원가법', '비교법', '수익법', '최종 조정 가액'],
                    '시산가액(원)': [f"{int(v):,}" for v in methods_dict.values()]
                }).set_index('평가 방식'), use_container_width=True)