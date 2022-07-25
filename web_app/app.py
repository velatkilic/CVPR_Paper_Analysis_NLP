import utils
import streamlit as st

# load and precompute stuff
utils.init_model()

# st app
st.title("CVPR Text Analysis and Recommendation")

with st.form(key="topic-search"):
    c1, c2= st.columns(2)
    with c1:
        text_input = st.text_input("Enter title or any other text here")
    with c2:
        n_paper = st.number_input("Number of papers", 1, 100, 5)
    
    c1_opt, c2_opt = st.columns(2)
    
    with c1_opt:
        sopt = st.radio("Sort by", ("citation", "year", "author"), index=1)
    with c2_opt:
        check_box = st.checkbox('Include Preview URLs')
    

    sopt_dict = {"citation": "citation_count" , "year":"year" ,"author":"authors"}

    rec_paper = st.form_submit_button(label = 'Recommend Papers')

    if rec_paper:
        out = utils.get_relevant_papers(text_input, n_paper)
        if out is not None:
            # sort
            if sopt_dict[sopt] in ["citation_count", "year"]:
                out = out.sort_values(by=[sopt_dict[sopt]], ascending=False)
            else:
                out = out.sort_values(by=[sopt_dict[sopt]])

            # show data
            if check_box:
                out['link'] = out['link'].apply(utils.make_clickable, args = ('PDF Link',))
                st.write(out[["authors", "title", "year", "abstract", "link", "citation_count"]].to_html(escape = False), unsafe_allow_html = True)
            else:
                st.dataframe(out[["authors", "title", "year", "abstract", "link", "citation_count"]])
        else:
            st.write("Text not in the vocabulary")



with st.form(key="topics"):
    c1, c2 = st.columns(2)
    with c1:
        option = st.selectbox("Which topics would you like to see?", ("hot", "top", "rising"))
    with c2:
        n = st.number_input("Select number of keywords in each topic", 1, 30, 5)

    show_topics = st.form_submit_button(label = 'Show Topics')

    if show_topics:
        top_count = utils.get_top_by_count(n)
        top_citation = utils.get_top_by_citation(n)
        top_rising = utils.get_top_rising(n)

        if option == "hot":
            st.json(str(top_count))
        elif option == "top":
            st.json(str(top_citation))
        elif option == "rising":
            st.json(str(top_rising))

with st.form(key="language-model"):
    c1_lm, c2_lm = st.columns((5,1))
    with c1_lm:
        abs_input = st.text_area("Enter text for word suggestions")
    with c2_lm:
        n_words = st.number_input("Number of suggestions", 1, 100, 10)
    
    rec_word = st.form_submit_button(label = "Recommend Words")
    
    if rec_word:
        rec = utils.get_word_suggestions(abs_input, top_k=n_words)
        st.write(rec)
