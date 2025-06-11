import streamlit as st
from PIL import ImageColor
from datetime import datetime

# タイトル
st.title("推し紹介カード作成")

# 過去のカードを保存するためのセッション状態を初期化
if "cards" not in st.session_state:
    st.session_state["cards"] = []

# フォームの作成
with st.form("profile_form"):
    st.header("情報を入力してください")
    
    # 名前入力
    name = st.text_input("推しの名前を入力してください")

    # 名前入力
    name2 = st.text_input("自分のニックネームを入力してください")
    
    # 画像アップロード
    uploaded_image = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
    
    # イメージカラー入力
    color = st.color_picker("イメージカラーを選択してください")
    
    # 誕生日入力
    birthday = st.date_input("誕生日を入力してください", min_value=None, max_value=None)
    
    # 自己紹介文入力
    bio = st.text_area("推しの紹介文を入力してください")
    
    # フォーム送信ボタン
    submitted = st.form_submit_button("カードを作成")

    now = datetime.now()
    
    if submitted:
        # 新しいカードをセッション状態に追加
        st.session_state["cards"].insert(0, {
            "name": name,
            "name2": name2,
            "image": uploaded_image,
            "color": color,
            "birthday": birthday,
            "bio": bio,
            "now": now
        }
        )
        st.success("カードが作成されました！")

# 過去のカードを表示
if st.session_state["cards"]:
    st.header("推し紹介カード一覧")
    for card in st.session_state["cards"]:
        # イメージカラーをRGB値に変換し、+120した色を計算 ← なしにした
        base_rgb = ImageColor.getrgb(card["color"])
        adjusted_rgb = tuple(min(255, value) for value in base_rgb)  #value+120
        adjusted_color = f"rgb{adjusted_rgb}"
        
        # カードの背景色を設定
        card_style = f"background-color: {adjusted_color}; padding: 20px; border-radius: 5px;"
        
        st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if card["image"] is not None:
                st.image(card["image"], caption="プロフィール画像", use_container_width=True)
            else:
                st.write("画像がアップロードされていません")
        
        with col2:
            st.write(f"**推し:** {card['name']}")
            st.write(f"**紹介者:** {card['name2']}")
            st.write(f"**誕生日:** {card['birthday']}")
            st.write(f"**紹介文:** {card['bio']}")
            st.write(f"**作成日時:** {now.strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
